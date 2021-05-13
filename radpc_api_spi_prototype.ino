#include <SPI.h>

int i=1;
//int packet[] = {0x22,0x23,0x24,0x25};
char packet[128] = "Montana State Univ-RadPC";

void setup() 
{
  Serial.begin(115200);
  // Set the Main in Secondary Out as an output
  pinMode(MISO, OUTPUT);

  // turn on SPI as a secondary
  // Set appropriate bit in SPI Control Register
  //SPCR |= _BV(SPE);
  SPCR = (1<<SPE)|(0<<DORD)|(0<<MSTR)|(0<<CPOL)|(0<<CPHA)|(0<<SPR1)|(1<<SPR0); // SPI on
  SPDR = packet[0]; 
}

/**
  Handle reset transaction
*/
void reset_sequence()
{
  byte in_byte;
  SPDR = 0x22;
  
  if ((SPSR & (1 << SPIF)) != 0)
  {
    in_byte = SPDR;
    Serial.println(in_byte);
    if(in_byte == 0x22){
      Serial.println("test"); 
    }
  }
}

/**
  Handle transaction of a packet
*/
void packet_sequence()
{
  byte in_byte;
  SPDR = 0x25;
  
  if ((SPSR & (1 << SPIF)) != 0)
  {
    in_byte = SPDR;
    if(in_byte == 0x25){
      Serial.println("now send packet");
      for(i=0; i<128; i++){
        SPI.transfer(packet[i]);
      }
    }
  }
}

void loop () 
{
  //reset_sequence();
  packet_sequence();
}
