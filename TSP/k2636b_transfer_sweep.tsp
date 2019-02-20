-------------------------------
-- TSP PROGRAM FOR PERFORMING TRANSFER SWEEPS
-- Sweeps over gate voltage and measures channel current
-- INPUT sweep start and end points with ABSOLUTE step size
-------------------------------

function f_transfer(vds,start,stop,step)

    print(">>head<<VGS("..start..") IDS("..start..") IGS("..start..") VDS("..start..")")

	smua.source.levelv = vds
	smub.source.levelv = start
	smua.source.output = smua.OUTPUT_ON
	smub.source.output = smub.OUTPUT_ON
	delay(0.5)

	Vg=start
	while true do
		smub.source.levelv = Vg
		print(Vg, smua.measure.i(),smub.measure.i(),vds)
		delay(0.05)

		Vg=Vg+step	 
		if (stop-Vg) < 0 and step>0 then break	end
		if (stop-Vg) > 0 and step<0 then break	end
	end

	smua.source.output = smua.OUTPUT_OFF
	smub.source.output = smub.OUTPUT_OFF
end


-------- MAIN PROGRAM --------
reset()
--display.clear()
--display.settext("TRANSFER SWEEP")


-- Beep in excitement
--beeper.beep(1, 600)

-------- PARAMETERS --------
-- Vchan	= -20
-- Vds	 = 10
-- VgsStart = 0
-- VgsEnd	 = 10
-- VgsStep	 = 0.5
-- SWEEP	 = true
-- NPLC	 = 0.1
-- DELATE	 = 1

--LIMIT_I = 10e-3
--LIMIT_V = 100
--LIMIT_R = 10e-3

LIMIT_I = 1
LIMIT_V = 100
LIMIT_R = 1


-- Clear buffers and make sure the right thing is recorded
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
smua.measure.analogfilter = 0
smua.source.func = smua.OUTPUT_DCVOLTS
smua.source.autorangev = smua.AUTORANGE_ON
smua.source.limiti  = LIMIT_I
smua.source.limitv  = LIMIT_V
smua.measure.rangei = LIMIT_R
smua.sense = smua.SENSE_LOCAL

-- SMUB setup
smub.measure.delay = smub.DELAY_AUTO
smub.measure.delayfactor = DELATE
smub.measure.nplc = NPLC
smub.measure.analogfilter = 0
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.limiti  = LIMIT_I
smub.source.limitv  = LIMIT_V
smub.measure.rangei = LIMIT_R

--DISPLAY settings
--display.smua.measure.func = display.MEASURE_DCAMPS
--display.smub.measure.func = display.MEASURE_DCAMPS
--display.screen = display.SMUA_SMUB
--display.screen = display.USER
-- MEASUREMENT ROUTINE

if (VgsStart) <= (VgsEnd) then
	VgsStep = math.abs(VgsStep)
else
	VgsStep = -1*math.abs(VgsStep)
end


f_transfer((Vds),(VgsStart), (VgsEnd), (VgsStep))
if SWEEP  then
f_transfer((Vds),(VgsEnd), (VgsStart), (-1*VgsStep))
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
waitcomplete()
-------- END --------


