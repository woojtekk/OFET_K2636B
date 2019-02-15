----------------
-- TSP PROGRAM FOR PERFORMING TRANSFER SWEEPS
-- Sweeps over gate voltage and measures channel current

-- INPUT sweep start and end points with ABSOLUTE step size


-------- PARAMETERS --------
-- Vchan	= -20
Vds	 = -20
VgsStart = -20
VgsEnd	 = 20
VgsStep	 = 15
NPLN	 = 10
DELATE	 = 1.0
-------- MAIN PROGRAM --------
reset()
display.clear()

-- Beep in excitement
beeper.beep(1, 600)

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
smua.measure.delayfactor = DELATE
smua.measure.nplc = NPLC
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
smua.source.limiti = 10e-5
smua.measure.rangei = 10e-5

-- SMUB setup
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

Vg = VgsStart
smub.source.levelv = Vg
smub.source.output = smub.OUTPUT_ON
delay(1)

-- Forward Vg scan
if VgsStart < VgsEnd then
    while Vg <= VgsEnd do
        smub.source.levelv = Vg
        smub.source.output = smub.OUTPUT_ON
        delay(0.2)
        print(smua.measure.i(smua.nvbuffer1),smub.measure.i(smub.nvbuffer1))

        smub.source.output = smub.OUTPUT_OFF
        Vg = Vg + VgsStep
    end

-- Reverse scan
elseif VgStart > VgEnd then
    while Vg >= VgEnd do
        smub.source.levelv = Vg
        smub.source.output = smub.OUTPUT_ON
        delay(0.2)
        smua.measure.i(smua.nvbuffer1)
        smub.measure.i(smub.nvbuffer1)

        smub.source.output = smub.OUTPUT_OFF
        Vg = Vg - VgStep
    end

else
    error("Invalid sweep parameters.")
end

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
waitcomplete()
-------- END --------
