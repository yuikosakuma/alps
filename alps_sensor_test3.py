from btle import Peripheral
import struct 
import btle
import binascii

def s16(value):
   return -(value & 0b1000000000000000) | (value & 0b0111111111111111)


class NtfyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here
    def handleNotification(self, cHandle, data):         # ... perhaps check cHandle
        # ... process 'data'
        cal = binascii.b2a_hex(data)
        #print u'handleNotification : {0}-{1}:'.format(cHandle, cal)
        if int((cal[0:2]), 16) == 0xf2:
            GeoMagnetic_X = s16(int((cal[6:8] + cal[4:6]), 16)) * 0.15
            GeoMagnetic_Y = s16(int((cal[10:12] + cal[8:10]), 16)) * 0.15
            GeoMagnetic_Z = s16(int((cal[14:16] + cal[12:14]), 16)) * 0.15
            print 'GeoMagnetic_X:{0:.3f}'.format(GeoMagnetic_X)
            print 'GeoMagnetic_Y:{0:.3f}'.format(GeoMagnetic_Y)
            print 'GeoMagnetic_Z:{0:.3f}'.format(GeoMagnetic_Z)
            Acceleration_X = 1.0 * s16(int((cal[18:20] + cal[16:18]), 16)) / 1024
            Acceleration_Y = 1.0 * s16(int((cal[22:24] + cal[20:22]), 16)) / 1024
            Acceleration_Z = 1.0 * s16(int((cal[26:28] + cal[24:26]), 16)) / 1024
            print 'Acceleration_X:{0:.3f}'.format(Acceleration_X)
            print 'Acceleration_Y:{0:.3f}'.format(Acceleration_Y)
            print 'Acceleration_Z:{0:.3f}'.format(Acceleration_Z)

        if int((cal[0:2]), 16) == 0xf3:
            Pressure = int((cal[6:8] + cal[4:6]), 16) * 860.0/65535 + 250   
            Humidity = 1.0 * (int((cal[10:12] + cal[8:10]), 16) - 896 )/64
            Temperature = 1.0*((int((cal[14:16] + cal[12:14]), 16) -2096)/50)
            UV = int((cal[18:20] + cal[16:18]), 16) / (100*0.388)
            AmbientLight = int((cal[22:24] + cal[20:22]), 16) / (0.05*0.928)
            print 'Pressure:{0:.3f}'.format(Pressure)
            print 'Humidity:{0:.3f}'.format(Humidity)
            print 'Temperature:{0:.3f}'.format(Temperature)
            print 'UV:{0:.3f}'.format(UV)
            print 'AmbientLight:{0:.3f}'.format(AmbientLight)
       

class AlpsSensor(Peripheral):
    def __init__(self,addr):
        Peripheral.__init__(self,addr)
        self.result = 1

def main():
    alps = AlpsSensor(" ")
    alps.setDelegate( NtfyDelegate(btle.DefaultDelegate) )
    alps.writeCharacteristic(0x0013, struct.pack('<bb', 0x01, 0x00), True)# Custom1 Notify Enable     
    alps.writeCharacteristic(0x0016, struct.pack('<bb', 0x01, 0x00), True)# Custom2 Notify Enable
    alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x2F, 0x03, 0x03), True)
    """
    # Only environment
    alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x01, 0x03, 0x7C), True)
    alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x04, 0x03, 0x00), True)# Slow 1sec
    alps.writeCharacteristic(0x0018, struct.pack('<bbbb', 0x05, 0x04, 0x3C, 0x00), True) 
    """
    # Hybrid mode
    alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x01, 0x03, 0x7F), True)
    alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x04, 0x03, 0x04), True)# Hybrid Mode
    alps.writeCharacteristic(0x0018, struct.pack('<bbbb', 0x06, 0x04, 0x64, 0x00), True) # Fasr 100msec 
    alps.writeCharacteristic(0x0018, struct.pack('<bbbb', 0x05, 0x04, 0x01, 0x00), True) # Slow 1sec
    alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x2F, 0x03, 0x01), True)#save
    alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x20, 0x03, 0x01), True)# i
     # Main loop --------
    while True:
       if alps.waitForNotifications(1.0):
            # handleNotification() was called
           continue
       print "Waiting..."
        # Perhaps do something else here
if __name__ == "__main__":
    main() 
