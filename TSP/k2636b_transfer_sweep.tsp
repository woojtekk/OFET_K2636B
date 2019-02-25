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
	delay(0.2)

	Vg=start
	while true do
		smub.source.levelv = Vg
		print(Vg, smua.measure.i(),smub.measure.i(),vds)
		delay(0.2)

		Vg=Vg+step	 
		if (stop-Vg) < 0 and step>0 then break	end
		if (stop-Vg) > 0 and step<0 then break	end
	end

	smua.source.output = smua.OUTPUT_OFF
	smub.source.output = smub.OUTPUT_OFF
end

-------- MAIN PROGRAM --------
reset()
-- Beep in excitement
--beeper.beep(0.1, 1000)
--beeper.beep(0.1, 1000)

-------- PARAMETERS --------
--Vds
--Vgs
--Tlong

ALIMIT_V = 100
ALIMIT_I = 10e-3
ALIMIT_R = 10e-3

BLIMIT_V = 100
BLIMIT_I = 10e-4
BALIMIT_R =10e-4

NPLC   = 1
DELATE = 1

format.data = format.ASCII
smua.measure.count = 1
smub.measure.count = 1

-- SMUA setup
smua.measure.delay = smua.DELAY_AUTO
smua.measure.delay = 0
smua.measure.delayfactor = DELATE
smua.measure.nplc = NPLC
smua.measure.analogfilter = 0
smua.source.func = smua.OUTPUT_DCVOLTS
smua.source.autorangev = smua.AUTORANGE_ON
smua.source.limiti  = ALIMIT_I
smua.source.limitv  = ALIMIT_V
smua.measure.rangei = ALIMIT_R
smua.sense = smua.SENSE_LOCAL

-- SMUB setup
smub.measure.delay = smub.DELAY_AUTO
smub.measure.delay = 0
smub.measure.delayfactor = DELATE
smub.measure.nplc = NPLC
smub.measure.analogfilter = 0
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.limiti  = BLIMIT_I
smub.source.limitv  = BLIMIT_V
smub.measure.rangei = BLIMIT_R


-- MEASUREMENT ROUTINE
display.smua.measure.func = display.MEASURE_DCAMPS
display.smub.measure.func = display.MEASURE_DCAMPS


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


