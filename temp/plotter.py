import matplotlib.pyplot as plt

def plotxy(x,y):

    fig,ax1 = plt.subplots()
    try:
#        ax1.plot(df1['Channel Voltage [V]'],
 #                    df1['Channel Current [A]'] / 1e-6, '.')
        ax1.plot(x,y)
        ax1.set_title('I-V sweep')
        ax1.set_xlabel('Channel Voltage [V]')
        ax1.set_ylabel('Channel Current [$\mu$A]')
    except:
        pass
    plt.show()