-------------------------------
-- TSP PROGRAM FOR PERFORMING TRANSFER SWEEPS
-- Sweeps over gate voltage and measures channel current
-- INPUT sweep start and end points with ABSOLUTE step size
-------------------------------

function oled_ltp(V_start,dd)

    print(">>head<<dt(__) \t I(__)")

	smub.source.levelv = V_start
	smub.source.output = smub.OUTPUT_ON

	--delay(1)
	-- dummy measure I x2
    smub.measure.i()
    smub.measure.i()

    timer.reset()
	while true do
		print(timer.measure.t(), smub.measure.i())
		delay(OLED_dT)
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
--Vds
--Vgs
--Tlong
--BLIMIT_V = 50
--BLIMIT_I = 10e-4
--BALIMIT_R =10e-4
--NPLC   = 1
--DELATE = 1



-- SMUB setup
--smub.measure.analogfilter = 0
--smub.measure.delay = 0


format.data = format.ASCII
smub.source.limiti       = BLIMIT_I
smub.source.limitv       = BLIMIT_V
smub.source.func         = smub.OUTPUT_DCVOLTS

-- MEASUREMENT ROUTINE
display.smub.measure.func = display.MEASURE_DCAMPS
smub.measure.count = 1
smub.measure.delay        = smub.DELAY_AUTO
smub.measure.delayfactor  = smub.DELAY_AUTO
smub.measure.nplc         = NPLC
smub.measure.autorangei   = smub.AUTORANGE_ON
smub.measure.autozero     = smub.AUTOZERO_AUTO


oled_ltp((OLED_V),DELATE)



waitcomplete()
beeper.beep(0.1, 2400)
beeper.beep(0.1, 2400)

-------- END --------


