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
spi.max_speed_hz = 4000 
#spi.max_speed_hz = 100000 

def send_test(channel=None):
    print('')
    print('test send')

    command = spi.xfer2([0x22])[0]
    print(command)
    time.sleep(1)
    command = spi.xfer2([0x25])[0]
    time.sleep(1)
    print(command)

    #num = 0x00
    #for i in range(4):
    #    command = spi.writebytes([num])
    #    num = num + 1

def send_receive(channel):
    try:
        # Send a null byte to check for value
        #send_byte = [0x00]
        '''
        send_byte = [x for x in range(0,128)] 
        data_recv = spi.xfer3(send_byte,128)
        '''
        print('')
        print('send_receive')
        command = spi.xfer2([0x22])[0]
        print(command)
        if hex(command) == "0x22":
            print('Command: RESET')
            spi.xfer([command])
        elif hex(command) == "0x25": 
            print('packet command') 
            res = spi.xfer([command])
            print(res)
            send_byte = [x for x in range(0,128)] 
            data_recv = spi.xfer3(send_byte,128)
            print(data_recv)
            print("".join([chr(x) for x in data_recv]))
        else:
            print ("Response: "+str(hex(data_recv[0])))
    except Exception as e:
        print(e)

#GPIO.add_event_detect(23, GPIO.RISING, callback=send_test, bouncetime=500)
#GPIO.add_event_detect(23, GPIO.RISING, callback=send_receive, bouncetime=500)

#while True:
#    pass 

## FOR TESTING
while True:
    time.sleep(1)
    send_test()

'''
while True:
    if GPIO.input(23):
        print('HIGH')
        send_receive()
    else:
        print('LOW')
    time.sleep(0.15)
'''
#quit()
