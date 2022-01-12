--[[
	Name:	DCSweepVLinear(start, stop, numPoints, limitI, nplc)

	Description:
		This function performs an autoranged DC linear voltage sweep.  It
		demonstrates the simplest trigger model configuration to perform
		this sweep.

	Parameters:
		start:			The voltage level of the first step in the sweep in volts
		stop:			The voltage level of the last step in the sweep in volts
		numPoints:		The number of points in the sweep
		limitI:			The current limit of the source in amps
		nplc:			The measurment aperture setting in PLCs where 1 PLC = 1/60 s for 60Hz power

	Example Usage:
		DCSweepVLinear(0, 10, 11, 0.1, 1)
--]]
function DCSweepVLinear(start, stop, numPoints, limitI, nplc)
	reset()
    display.clear()
	print("V0005")
    -- Beep in excitement
    beeper.beep(1, 600)


	-- Configure the SMU
	smua.reset()
	smua.source.func					= smua.OUTPUT_DCVOLTS
	smua.source.limiti					= limitI
	smua.measure.nplc					= nplc
	smua.measure.delay					= smua.DELAY_AUTO

	-- Prepare the Reading Buffers
	smua.nvbuffer1.clear()
	smua.nvbuffer1.collecttimestamps	= 1
	smua.nvbuffer2.clear()
	smua.nvbuffer2.collecttimestamps	= 1

    --DISPLAY settings
    display.smua.measure.func = display.MEASURE_DCAMPS
    display.screen = display.SMUA

	-- Configure SMU Trigger Model for Sweep
	smua.trigger.source.linearv(start, stop, numPoints)
	smua.trigger.source.limiti			= limitI
	smua.trigger.measure.action			= smua.ENABLE
	smua.trigger.measure.iv(smua.nvbuffer1, smua.nvbuffer2)
	smua.trigger.endpulse.action		= smua.SOURCE_HOLD
	-- By setting the endsweep action to SOURCE_IDLE, the output will return
	-- to the bias level at the end of the sweep.
	smua.trigger.endsweep.action		= smua.SOURCE_IDLE
	smua.trigger.count					= numPoints
	smua.trigger.source.action			= smua.ENABLE
	smua.measure.autozero 				= smua.AUTOZERO_ONCE
	smua.measure.delay 					= 0.01

	smua.measure.lowrangei = 10e-3

	-- Ready to begin the test

	smua.source.output					= smua.OUTPUT_ON
	-- Start the trigger model execution
	smua.trigger.initiate()
	-- Wait until the sweep has completed
	waitcomplete()
	smua.source.output					= smua.OUTPUT_OFF
	
	-- Print the data back to the Console in tabular format
	--[[
	print("Time\tVoltage\tCurrent")
	for x=1,smua.nvbuffer1.n do
		-- Voltage readings are in nvbuffer2.  Current readings are in nvbuffer1.
		print(smua.nvbuffer1.timestamps[x], smua.nvbuffer2[x], smua.nvbuffer1[x])
	end

    print("smua.nvbuffer1.n",smua.nvbuffer1.n)
    --]]

end

-- DCSweepVLinear(start, stop, numPoints, limitI, nplc)
-- DCSweepVLinear(-12, 1, 50, 0.05, 5)