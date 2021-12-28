
def load_TSP(inst,script):
    """Load an anonymous TSP script into the K2636 nonvolatile memory."""
    try:
        inst.write('loadscript')
        line_count = 1
        for line in open(script, mode='r'):
            print(line)
            inst.write(line)
            line_count += 1
        inst.write('endscript')
        print('----------------------------------------')
        print('Uploaded TSP script: ', script)

    except FileNotFoundError:
            print('ERROR: Could not find tsp script. Check path.')
            raise SystemExit




#THE MAIN PART OF THE CODE
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


load_TSP(keith,'led_script.tsp')

keith.write('DCSweepVLinear(-12, 1, 50, 0.05, 5)')
#keith.write('script.anonymous.run()')
print('Measurement in progress...')






"""
            df = self.readBufferIV()
            output_name = str(sample + '-iv-sweep.csv')
            df.to_csv(output_name, sep='\t', index=False)
            finish_time = time.time()
            print('IV sweep complete. Elapsed time %.2f mins.'
                  % ((finish_time - begin_time)/60))
"""




keith.close()
print('closed it')


#close the device
