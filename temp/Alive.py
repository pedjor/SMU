print ("I'm Alive and sometimes I kick")


"""
stuff to interact vi visa
"""


import pyvisa

"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import time
from serial import SerialException
"""

address='TCPIP0::192.168.120.50::inst0::INSTR'
#
rm = pyvisa.ResourceManager('@py')  # use py-visa backend
#rm = pyvisa.ResourceManager()  # use py-visa backend
#print(rm.list_resources())
keith = rm.open_resource('TCPIP::192.168.120.50::inst0::INSTR')
#print ('opening instrument')
#print (self.inst)
if (keith): 
    print('I could open it and it\'s called:')
print(keith.query('*IDN?'))


keith.close()



#close the device
