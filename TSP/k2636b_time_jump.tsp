-------------------------------
-- TSP PROGRAM FOR PERFORMING TRANSFER SWEEPS
-- Sweeps over gate voltage and measures channel current
-- INPUT sweep start and end points with ABSOLUTE step size
-------------------------------

function f_time(vds, vgs, tstep, tlong)
    print(">>head<< #dt IDS  IGS  VDS  VGS")
    vgs_new=0
    xx=0
	smua.source.levelv = vds
	smub.source.levelv = vgs
	timer.reset()
	smua.source.output = smua.OUTPUT_ON
	smub.source.output = smub.OUTPUT_ON
	--delay(0.2)
	timer.reset()

    tjump=0
	while true do
		dt = timer.measure.t()
		print(dt, smua.measure.i(), smub.measure.i(), smua.measure.v(), smub.measure.v())
		--delay(tstep)

        if tjump>=20 and (xx==0) then
            smub.source.levelv = vgs_new
            vgs_new = vgs_new-2
            xx=1
            tjump=0
        end

        if (tjump>=20) and (xx==1) then
            smub.source.levelv = vgs
            vgs_new = vgs_new-2
            xx=0
            tjump=0
        end


        tjump=tjump+1

		if dt >= tlong then break end
	end
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
--smua.source.limiti  = ALIMIT_I
--smua.source.limitv  = ALIMIT_V
--smua.measure.rangei = ALIMIT_R
--smua.sense = smua.SENSE_LOCAL


-- SMUB setup
smub.measure.delay = smub.DELAY_AUTO
smub.measure.delay = 0
smub.measure.delayfactor = DELATE
smub.measure.nplc = NPLC
smub.measure.analogfilter = 0
smub.source.func = smub.OUTPUT_DCVOLTS
--smub.source.limiti  = BLIMIT_I
--smub.source.limitv  = BLIMIT_V
--smub.measure.rangei = BLIMIT_R
--smub.sense = smub.SENSE_LOCAL


-- MEASUREMENT ROUTINE
display.smua.measure.func = display.MEASURE_DCAMPS
display.smub.measure.func = display.MEASURE_DCAMPS


smua.measure.autorangei = 1
smub.measure.autorangei = 1

f_time(Vds, Vgs, Tstep, Ttime)

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF


waitcomplete()

-- Beep in excitement
--beeper.beep(0.1, 1300)
-------- END --------


