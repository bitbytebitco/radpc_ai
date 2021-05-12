import spidev
import time
import RPi.GPIO as GPIO

# GPIO init
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)

# SPI init
spi_bus =0 
spi_device = 0

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = 100000

def send_receive():
    try:
        # Send a null byte to check for value
        #send_byte = [0x00]
        send_byte = [x for x in range(0,128)] 

        # repeat to check for a response
        #rcv_byte = spi.xfer2(send_byte)
        #data_recv = rcv_byte[0:127]
        data_recv = spi.xfer3(send_byte,128)

        #if (data_recv != 0x80):
        print ("Response: "+str(data_recv))
    except Exception as e:
        print(e)

while True:
    if GPIO.input(23):
        print('HIGH')
        send_receive() 
    else:
        print('LOW')
    time.sleep(0.15)

#quit()
