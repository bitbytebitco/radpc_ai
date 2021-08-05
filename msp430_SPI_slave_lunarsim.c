#include <msp430.h> 

unsigned int Rx_Data;
//char packet[128] = "Montana State Univ-RadPC";
char packet[128] = "\x4d\x6f\x6e\x74\x61\x6e\x61\x20\x53\x74\x61\x74\x65\x20\x52\x61\x64\x50\x43\x20\x46\x50\x47\x41\x00\x63\x05\x06\x69\x0b\x9e\x0b\x9f\x0b\xd8\x08\x10\x05\x6e\x0a\xa8\x01\x38\x08\x0d\x06\xc4\x02\x98\x03\x1f\x05\x3f\x03\xb9\xcc\xcc\x8c\x00\x01\x47\x00\x00\x00\x04\x00\x00\x00\x85\x00\x00\x00\x00\x00\x00\x00\x00\x00\x86\x01\x47\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x85\x00\x00\x08\xe9\x01\x48\x00\x00\x00\x00\x00\x04\x22\x00\x00\x00\x00\x00\x00\x14\x92\x00\x00";
unsigned int packet_i;
unsigned int sending_packet=0;
int RESET_BYTE = 0x0022;
int PACKET_BYTE = 0x0025;
int ACK_BYTE = 0x00EE;

int command_to_call = 0x0022;


int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;   // stop watchdog timer
    
    // -- Setup Ports
    P1DIR |= BIT0;      // P1.0 as OUTPUT
    P1OUT &= ~BIT0;      // default LOW

    P6DIR |= BIT6;      // P1.0 as OUTPUT
    P6OUT &= ~BIT6;     // P1.0 default LOW

    P2DIR &= ~BIT3;     // P2.3 as INPUT
    P2REN |= BIT3;      // enable pull up/down resistors
    P2OUT |= BIT3;      // pull UP resistor
    P2IES |= BIT3;      // HIGH-to-LOW edge sensitivity

    P4DIR &= ~BIT1;     // P4.1 as INPUT
    P4REN |= BIT1;      // enable pull up/down resistors
    P4OUT |= BIT1;      // pull UP resistor
    P4IES |= BIT1;      // HIGH-to-LOW edge sensitivity

    // -- SPI

    // configure eUSCI_A0
    UCA0CTLW0 |= UCSWRST;           // put eUSCI_A0 into RESET mode
    UCA0CTLW0 |= UCSYNC;            // SPI mode
    UCA0CTLW0 &= ~UCMST;            // SPI SLAVE mode
    UCA0CTLW0 |= UCMSB;             //  MSB first
    UCA0CTLW0 |= UCCKPH;            // capture on rising edge

    UCA0CTLW0 |= UCMODE1;           // 4-wire SPI with STE active LOW
    UCA0CTLW0 &= ~UCMODE0;
    UCA0CTLW0 |= UCSTEM;            // STE pin used for 4-wire SPI

    P1SEL1 &= ~BIT5;                // P1.5 SMCLK
    P1SEL0 |= BIT5;

    P1SEL1 &= ~BIT6;                // P1.6 SOMI
    P1SEL0 |= BIT6;

    P1SEL1 &= ~BIT7;                // P1.7 SIMO
    P1SEL0 |= BIT7;

    P1SEL1 &= ~BIT4;                // STE pin setup
    P1SEL0 |= BIT4;

    P2IE |= BIT3;                   // enable P2.3 IRQ
    P2IFG &= ~BIT3;                 // clear flag

    P4IE |= BIT1;                   // enable P1.1 IRQ
    P4IFG &= ~BIT1;                 // clear flag

    PM5CTL0 &= ~LOCKLPM5;

    UCA0CTLW0 &= ~UCSWRST;          // take eUSCI_A0 out of RESET mode

    __enable_interrupt();

    UCA0IE |= UCRXIE;               // enable A0 Rx IRQ
    UCA0IFG &= ~UCRXIFG;            // clear flag

//    UCA0IE |= UCTXIE;               // enable A0 Tx IRQ
//    UCA0IFG &= ~UCTXIFG;            // clear flag

    int i;
    while(1){
//      for(i=0; i<20000;i=i+1){}
//      P1OUT ^= BIT0;
    }

    return 0;
}

/**
 * ISR set PACKET_BYTE
 */
#pragma vector=PORT2_VECTOR
__interrupt void ISR_PORT2_S2(void){
//    P6OUT ^= BIT6;      // toggle LED2
    command_to_call = PACKET_BYTE;
    P2IFG &= ~BIT3;     // clear flag
}

/**
 * ISR set RESET_BYTE
 */
#pragma vector=PORT4_VECTOR
__interrupt void ISR_PORT4_S1(void){
//    P6OUT ^= BIT6;      // toggle LED2
    command_to_call = RESET_BYTE;
    P4IFG &= ~BIT1;     // clear flag
}

/**
 * ISR for when SPI Rx occurs
 */
#pragma vector = EUSCI_A0_VECTOR
__interrupt void ISR_EUSCI_A0(void){
    if(sending_packet == 0){            // if in `receive mode`
        Rx_Data = UCA0RXBUF;            // receive byte from buffer

        P1OUT &= ~BIT0;
        P6OUT &= ~BIT6;

        if(Rx_Data == ACK_BYTE){
            UCA0IE |= UCRXIE;               // enable A0 Rx IRQ

            UCA0IE |= UCTXIE;               // enable A0 Tx IRQ
            UCA0IFG &= ~UCTXIFG;            // clear flag

            UCA0TXBUF = command_to_call;
            UCA0IFG &= ~UCTXIFG;        // clear flag
        }
        if(Rx_Data == RESET_BYTE){      // if RESET_BYTE
            // CONFIRMATION OF RESET REQUEST
            P6OUT ^= BIT6;              // toggle LED1
        } else if (Rx_Data == PACKET_BYTE){     // if PACKET_BYTE
            // CONFIRMATION OF PACKET REQUEST
            //P1OUT ^= BIT0;              // toggle LED2

            packet_i = 0;
            sending_packet = 1;
            UCA0TXBUF = packet[packet_i];
            UCA0IFG &= ~UCTXIFG;        // clear flag
        }
    } else {
        if(packet_i >= 127){
            P1OUT |= BIT0;              // set LED1
            P6OUT |= BIT6;              // set LED2
            sending_packet = 0;

        } else {
            packet_i++;
            UCA0TXBUF = packet[packet_i];
        }
        UCA0IFG &= ~UCTXIFG;        // clear flag
    }

}

