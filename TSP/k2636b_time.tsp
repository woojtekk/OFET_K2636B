-------------------------------
-- TSP PROGRAM FOR PERFORMING TRANSFER SWEEPS
-- Sweeps over gate voltage and measures channel current
-- INPUT sweep start and end points with ABSOLUTE step size
-------------------------------

function f_time(vds, vgs, tstep, tlong)
    print(">>head<< dt IDS  IGS  VDS  VGS")
	smua.source.levelv = vds
	smub.source.levelv = vgs
	timer.reset()
	smua.source.output = smua.OUTPUT_ON
	smub.source.output = smub.OUTPUT_ON
	delay(tstep)
	dt=0
	td=0
	td = timer.measure.t()
	while true do
		dt = timer.measure.t()
		display.clear()
		display.settext(tostring(dt))

		print(dt, smua.measure.i(), smub.measure.i(), vds, vgs)
		td=dt
		delay(tstep)

		if dt >= tlong then break end
	end
end


-------- MAIN PROGRAM --------
reset()
-- display.clear()
-- display.settext("VDS ",tostring(Vds))
-- display.settext("$BTIME SWEEP")
-- display.settext("$N $B TIME SWEEP")


-- Beep in excitement
-- beeper.beep(0.1, 1000)
-- beeper.beep(0.1, 1000)

-------- PARAMETERS --------
--Vds
--Vgs
--Tlong

LIMIT_V = 200
LIMIT_I = 10e-3
LIMIT_R = 10e-3
NPLC   = 1
DELATE = 1

-- --Clear buffers and make sure the right thing is recorded
-- smua.nvbuffer1.clear()
-- smub.nvbuffer1.clear()
-- --Prepare buffers
-- smua.nvbuffer1.collectsourcevalues = 1
-- smub.nvbuffer1.collectsourcevalues = 1
-- format.data = format.ASCII
-- smua.nvbuffer1.appendmode = 1
-- smub.nvbuffer1.appendmode = 1
-- smua.measure.count = 1
-- smub.measure.count = 1

-- SMUA setup
smua.measure.delay = smua.DELAY_AUTO
smua.measure.delay = 0
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
smub.measure.delay = 0
smub.measure.delayfactor = DELATE
smub.measure.nplc = NPLC
smub.measure.analogfilter = 0
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.limiti  = LIMIT_I
smub.source.limitv  = LIMIT_V
smub.measure.rangei = LIMIT_R

--DISPLAY settings
-- display.smua.measure.func = display.MEASURE_DCAMPS
-- display.smub.measure.func = display.MEASURE_DCAMPS
-- display.screen = display.SMUA_SMUB
display.screen = display.USER
-- MEASUREMENT ROUTINE

f_time(Vds, Vgs, Tstep, Ttime)

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF


waitcomplete()

-- Beep in excitement
--beeper.beep(0.1, 1300)
-------- END --------


