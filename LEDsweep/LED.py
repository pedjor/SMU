def waitforcompletion():
    pos = 0

    while 1 :
        try:
            res=keith.query('*OPC?')
        except:
            print('\r',' '*pos,':-(','',end='')
            pos+=1
        else:
            if res.find('1')==0:
                print('\r',' :-) '*pos)
            else:
                print(Fore.RED+"not getting the reply I expected"+Style.RESET_ALL)
                print("Result is:" + Back.LIGHTRED_EX, res , Style.RESET_ALL)
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
        # loads and runs the script and this defines the functions
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

####### IMPORTS
import pyvisa
import time
from plotter import plotxy
from colorama import Fore, Back, Style

##############
# MAIN
##############


print ("Starting the LED sweep program")
#start_time = time.localtime()
#print(Fore.LIGHTBLUE_EX + "start Time: " , time.strftime("%H:%M:%S",start_time) + Style.RESET_ALL)
print(Fore.LIGHTBLUE_EX + "Start Time: " , time.asctime(), Style.RESET_ALL)


#The address of the instrument
address='TCPIP0::192.168.120.50::inst0::INSTR'

res_man = pyvisa.ResourceManager('@py')  # use py-visa backend
#res_man = pyvisa.ResourceManager()  # use System (e.g. NI-VISA) backend

try:
    keith = res_man.open_resource(address)
except:
    print('something bad happened. Could not open ',)
    exit(1)
else:
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

#start stopwatch for the sweep
stopwatchbegin=time.perf_counter()

keith.write('DCSweepVLinear(-12, 1, 50, 0.05, 5)')
print ('script version is ',keith.read())
#the script prints the version of the code, read it back

print('going to wait for completion')
waitforcompletion()
keith.write('*CLS')

#start stopwatch for the sweep
stopwatchend=time.perf_counter()
print("total time: %. seconds",stopwatchend-stopwatchbegin)

npoints=keith.query('print(smua.buffer.getstats(smua.nvbuffer1).n)')
print('Number of points from sweep:',npoints)

############## DATA
#'printbuffer' so that the instrument outputs
#query to get them
#arrange them in an array
vCurrent = [float(x) for x in keith.query('printbuffer' +'(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)').split(',')]
vVoltage = [float(x) for x in keith.query('printbuffer' +'(1, smua.nvbuffer1.n, smua.nvbuffer2.readings)').split(',')]


keith.close()
print('closed it')


print('**** data from sweep')
print(vCurrent)
print(vVoltage)

#end_time = time.localtime()
#print(Fore.LIGHTBLUE_EX + "End Time: " , time.strftime("%H:%M:%S",end_time) + Style.RESET_ALL)
print(Fore.LIGHTBLUE_EX + "End Time: " , time.asctime(), Style.RESET_ALL)


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





#close the device
