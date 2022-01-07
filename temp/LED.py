def waitforcompletion():
    pos=0
    dir=1
    while (1):
        try:
            Res=keith.query('*OPC?')
        except:
            print('\r',' '*pos,':-(','',end='')
            pos+=1
        else:
            print('\r',' :-) '*pos)
            #print(Res)
            break
        time.sleep(0.1)


def countdown(tcount,sleep_interval=0.1):
    #tcount: the time to countdown
    #sleep_interval; the steps to show
    ti=tcount
    while ti>0:
        print("\r", end="")
        print("{:.3f} ".format(ti), end="")
        time.sleep(sleep_interval)
        ti-=sleep_interval


def load_TSP(inst,script):
    """Load an anonymous TSP script into the K2636 nonvolatile memory."""
    try:
        #runs the script and this defines the functions
        inst.write('loadandrunscript')
        line_count = 1
        for line in open(script, mode='r'):
            #print(line)
            inst.write(line)
            line_count += 1
        inst.write('endscript')
        print('----------------------------------------')
        print('Uploaded TSP script: ', script,' with {} lines'.format(line_count))

    except FileNotFoundError:
            print('ERROR: Could not find tsp script. Check path.')
            raise SystemExit



#################################################################################
#################################################################################
#THE MAIN PART OF THE CODE
#################################################################################
#################################################################################


print ("I'm Alive and sometimes I kick")


"""
stuff to interact vi visa
"""


import pyvisa
import time
from plotter import plotxy
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
address='TCPIP::192.168.120.50::inst0::INSTR'
try:
    keith = rm.open_resource(address)
except:
    print('something bad happened. Could not open ',)
    exit(1)
if (keith):
    keith.write("localnode.prompts=0")
    keith.write("errorqueue.clear()")
    keith.write("*RST")
    keith.write("*CLS")
    time.sleep(.1)

    print('I could open it and it\'s called:')
    print(keith.query('*IDN?'))

#load and run the script to define functions
load_TSP(keith,'led_script.tsp')

#execute the sweep by calling the function
keith.write('DCSweepVLinear(-12, 1, 500, 0.05, 5)')
print ('script version is ',keith.read())
#the script prints the version of the code, read it back

print('going to wait for completion')
waitforcompletion()
keith.write('*CLS')

npoints=keith.query('print("n= "..smua.buffer.getstats(smua.nvbuffer1).n)')
print('Number of points from sweep=',npoints)

#'printbuffer' so that the instrument outputs
#query to get them
#arrange them in an array
vCurrent = [float(x) for x in keith.query('printbuffer' +'(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)').split(',')]
vVoltage = [float(x) for x in keith.query('printbuffer' +'(1, smua.nvbuffer1.n, smua.nvbuffer2.readings)').split(',')]

print('**** data from sweep')
print(vCurrent)
print(vVoltage)

#make a plot
plotxy(vVoltage,vCurrent)

exit(0)



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
