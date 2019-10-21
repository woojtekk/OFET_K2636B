-------------------------------
-- TSP PROGRAM FOR PERFORMING TRANSFER SWEEPS
-- Sweeps over gate voltage and measures channel current
-- INPUT sweep start and end points with ABSOLUTE step size
-------------------------------

function f_transfer(start,stop,step)

    print(">>head<<V(__) \t I(__)")

	smub.source.levelv = start
	smub.source.output = smub.OUTPUT_ON
	--delay(0.2)
    smub.measure.i()

	Vg=start
	while true do
		smub.source.levelv = Vg
		print(Vg, (smub.measure.i()))
		delay(0.5)
		Vg=Vg+step
		if (stop-Vg) < 0 and step>0 then break	end
		if (stop-Vg) > 0 and step<0 then break	end
	end

	smub.source.output = smub.OUTPUT_OFF
end

-------- MAIN PROGRAM --------
reset()
--smua.reset()
--smub.reset()

-- Beep in excitement
beeper.beep(0.1, 2400)

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
smub.measure.count = 1


-- SMUB setup
smub.measure.delay = smub.DELAY_AUTO
--smub.measure.delay = 0
smub.measure.delayfactor = smub.DELAY_AUTO
smub.measure.nplc = NPLC
--smub.measure.analogfilter = 0
smub.source.func = smub.OUTPUT_DCVOLTS
--smub.source.limiti  = BLIMIT_I
--smub.source.limitv  = BLIMIT_V
--smub.measure.rangei = BLIMIT_R


-- MEASUREMENT ROUTINE
display.smub.measure.func = display.MEASURE_DCAMPS
smub.measure.autorangei = smub.AUTORANGE_ON
smub.measure.autozero = smub.AUTOZERO_AUTO


if (OLED_VStart) <= (OLED_VEnd) then
	OLED_VStep = math.abs(OLED_VStep)
else
	OLED_VStep = -1*math.abs(OLED_VStep)
end


f_transfer((OLED_VStart), (OLED_VEnd), (OLED_VStep))
f_transfer((OLED_VEnd), (OLED_VStart), (-1*OLED_VStep))

waitcomplete()
beeper.beep(0.1, 2400)
beeper.beep(0.1, 2400)

-------- END --------


