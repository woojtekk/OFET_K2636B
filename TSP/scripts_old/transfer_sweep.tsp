----------------
-- TSP PROGRAM FOR PERFORMING TRANSFER SWEEPS
-- Sweeps over gate voltage and measures channel current
-- INPUT sweep start and end points with ABSOLUTE step size

function f_transfer(vds,start,stop,step)
	if start <= stop then
		step = math.abs(step)
	else
		step = -1*math.abs(step)
	end

	Vg=start
	while true do
		smub.source.levelv = Vg
		print(Vg, smua.measure.i(smua.nvbuffer1),smub.measure.i(smub.nvbuffer1))
		delay(0.25)

		Vg=Vg+step	 
		if math.abs(stop-Vg+step) <= 0 then
			break
		end
	end
end


-------- MAIN PROGRAM --------
reset()
display.clear()
print("zaczynamy")

-------- PARAMETERS --------
-- Vchan	= -20
-- Vds	 = 10
-- VgsStart = 0
-- VgsEnd	 = 10
-- VgsStep	 = 0.5
-- SWEEP	 = true
-- NPLC	 = 0.1
-- DELATE	 = 1

-- Beep in excitement
-- beeper.beep(1, 600)
beeper.beep(0.1, 659.25)
beeper.beep(0.1, 587.33)
beeper.beep(0.2, 349.23)
beeper.beep(0.2, 392.00)
beeper.beep(0.1, 523.25)
beeper.beep(0.1, 493.88)
beeper.beep(0.2, 293.66)
beeper.beep(0.2, 329.63)
beeper.beep(0.1, 493.88)
beeper.beep(0.1, 440.00)
beeper.beep(0.2, 261.63)
beeper.beep(0.2, 329.63)
beeper.beep(0.5, 440.00)

-- Clear buffers
smua.nvbuffer1.clear()
smub.nvbuffer1.clear()
-- Prepare buffers
smua.nvbuffer1.collectsourcevalues = 1
smub.nvbuffer1.collectsourcevalues = 1
format.data = format.ASCII
smua.nvbuffer1.appendmode = 1
smub.nvbuffer1.appendmode = 1
smua.measure.count = 1
smub.measure.count = 1

-- SMUA setup
smua.measure.delay = smua.DELAY_AUTO
smua.measure.delayfactor = DELATE
smua.measure.nplc = NPLC
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
smub.source.limiti = 10e-5
smua.measure.rangei = 10e-5

-- SMUB setup
smub.measure.delay = smub.DELAY_AUTO
smub.measure.delayfactor = DELATE
smub.measure.nplc = NPLC
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.limiti = 10e-8

--DISPLAY settings
display.smua.measure.func = display.MEASURE_DCAMPS
display.smub.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUA_SMUB

-- MEASUREMENT ROUTINE

smua.source.levelv = Vds
smua.source.output = smua.OUTPUT_ON
smub.source.levelv = VgsStart
smub.source.output = smub.OUTPUT_ON
delay(1)


f_transfer((Vds),(VgsStart), (VgsEnd), (VgsStep))
if SWEEP  then
f_transfer((Vds),(VgsEnd), (VgsStart), (VgsStep))
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
waitcomplete()
-------- END --------

-------------------------------

