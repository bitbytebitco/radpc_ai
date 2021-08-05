import os
import spidev
import time
import RPi.GPIO as GPIO

# GPIO init
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)

# SPI init
spi_bus =0 
spi_device = 0

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
#spi.max_speed_hz = 4000 
#spi.max_speed_hz =  151000 
spi.max_speed_hz =  145000      # NOTE: CLOCK STUFF IS WEIRD! 

spi.no_cs = False

ACK = 0xEE
BINARY = False

# TODO: replace print statements with logging

def send_receive(channel=None):
    try:

        print('')
        print('send_receive')
        print('SENDING: ACK(`{}`)'.format(hex(ACK)))
        print(hex(ACK))

        ack_resp = spi.xfer([ACK])      # send 0xEE to MSP to start sequence
        command = spi.readbytes(1)[0]   # byte a byte which will be the COMMAND FOR THE RPI
   
        if hex(command) == "0x22":
            print('Command: RESET')
            spi.writebytes([0x22])      # SEND CONFIRMATION (echo command)
        elif hex(command) == "0x25": 
            print('Command: PACKET')

            if True:
                fake = []
                for i in range(127):
                    fake.append(0x00)

                spi.writebytes([0x25])  # SEND CONFIRMATION (echo command)
                packet = spi.xfer(fake) # read PACKET
            else: 
                spi.writebytes([0x25])
                packet = spi.readbytes(128)

            #print('packet data')
            #print(packet)
            #print([hex(i) for i in packet])
            #print("".join([chr(i) for i in packet]))

             
            bytes_str = bytes(bytearray([i for i in packet]))
            #print(str(bytes_str))
           
            packet_count = len(os.listdir(os.path.join(os.getcwd(), "packets"))) # count files for filename usage
            with open('packets/{}.txt'.format(int(packet_count)+1), 'w') as binary_file:
                if not(BINARY):
                    binary_file.write(str(bytes_str)) # saving as a str
                else:
                    binary_file.write(bytes_str) # saving as binary needs `wb` in open()
                print('packet {} saved'.format(packet_count))
            
        else:
            print("ELSE!")
            print(hex(command))
    except Exception as e:
        print(e)

# SETUP Interrupt
GPIO.add_event_detect(23, GPIO.RISING, callback=send_receive, bouncetime=500)

# Main Loop
while True:
    pass 

print('####')
print('####')

