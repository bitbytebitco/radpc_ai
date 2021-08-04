#include <msp430.h> 

int Rx_Data;
char packet[128] = "Montana State Univ-RadPC";

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

    P2IE |= BIT3;       // enable P4.1 IRQ
    P2IFG &= ~BIT3;     // clear flag

    PM5CTL0 &= ~LOCKLPM5;

    UCA0CTLW0 &= ~UCSWRST;          // take eUSCI_A0 out of RESET mode

    UCA0IE |= UCRXIE;               // enable A0 Rx IRQ
    UCA0IFG &= ~UCRXIFG;            // clear flag

    __enable_interrupt();

    int i;
    while(1){}

    return 0;
}

#pragma vector=PORT2_VECTOR
__interrupt void ISR_PORT2_S2(void){
    P6OUT ^= BIT6;      // toggle LED2
    P2IFG &= ~BIT3;     // clear flag
}

/**
 * ISR for when SPI Rx occurs
 */
#pragma vector = EUSCI_A0_VECTOR
__interrupt void ISR_EUSCI_A0(void){
    Rx_Data = UCA0RXBUF;
//    P6OUT ^= BIT6;
    if(Rx_Data == 0x0022){
        P1OUT ^= BIT0;              // toggle LED1
    } else if (Rx_Data == 0x0025){
        P6OUT ^= BIT6;              // toggle LED2
    }
    UCA0IFG &= ~UCTXIFG;            // clear flag
}

