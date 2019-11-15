-------------------------------
-- TSP PROGRAM FOR PERFORMING TRANSFER SWEEPS
-- Sweeps over gate voltage and measures channel current
-- INPUT sweep start and end points with ABSOLUTE step size
-------------------------------

function f_transfer(start,stop,step)

    print(">>head<<V(__) \t I(__)")

	smub.source.levelv = start
	smub.source.output = smub.OUTPUT_ON
	-- delay(DELATE)
	-- dummy measure I x2
    smub.measure.i()
    smub.measure.i()

	Vg=start
	while true do
		smub.source.levelv = Vg
		print(Vg, (smub.measure.i()))
		beeper.beep(0.1, 2000)

		delay(DELATE)
		Vg=Vg+step
		if (stop-Vg) < 0 and step>0 then break	end
		if (stop-Vg) > 0 and step<0 then break	end
	end

	smub.source.output = smub.OUTPUT_OFF
end

-------- MAIN PROGRAM --------
reset()
smua.reset()
smub.reset()

-- Beep in excitement
beeper.beep(0.1, 2400)

-------- PARAMETERS --------

--------  SMUB setup --------
--smub.measure.analogfilter = 0
--smub.measure.delay = 0

format.data              = format.ASCII
smub.source.limiti       = LIMIT_I
smub.source.limitv       = LIMIT_V
smub.source.func         = smub.OUTPUT_DCVOLTS

-- MEASUREMENT ROUTINE
display.smub.measure.func = display.MEASURE_DCAMPS
smub.measure.count        = 1
smub.measure.delay        = smub.DELAY_AUTO
smub.measure.delayfactor  = smub.DELAY_AUTO
smub.measure.nplc         = NPLC
--smub.measure.autorangei   = smub.AUTORANGE_ON
smub.measure.autozero     = smub.AUTOZERO_AUTO
--smub.measure.rangei = 2


if (V_Start) <= (V_Stop) then
	V_Step = math.abs(V_Step)
else
	V_Step = -1*math.abs(V_Step)
end


f_transfer((V_Start), (V_Stop), (V_Step))
if SWEEP then
f_transfer((V_Stop), (V_Start), (-1*V_Step))
end

waitcomplete()
beeper.beep(0.1, 2350)
beeper.beep(0.1, 2450)

-------- END --------


