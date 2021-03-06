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
-------- PARAMETERS --------
Vstart = -20
Vend = 20
Vstep = 10


-------- MAIN PROGRAM --------
reset()
display.clear()

-- Beep in excitement
-- beeper.beep(1, 600)

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

-- Measurement Setup
-- To adjust the delay factor.
smua.measure.delayfactor = 1
smua.measure.nplc = 10
-- SMUA setup
smua.source.func = smua.OUTPUT_DCVOLTS
smua.sense = smua.SENSE_LOCAL
smua.source.autorangev = smua.AUTORANGE_ON
smua.source.limiti = 1e-5
smua.measure.rangei = 1e-5

--DISPLAY settings
display.smua.measure.func = display.MEASURE_DCAMPS
display.screen = display.SMUA

-- Measurement routine
V = Vstart
smua.source.output = smua.OUTPUT_ON
smua.source.levelv = V
delay(1)

smua.source.output = smua.OUTPUT_ON
v=0
while true do
print(v,V,smua.measure.i(smua.nvbuffer1))
delay(0.1)
v=v+1
end

smua.source.output = smua.OUTPUT_OFF

waitcomplete()

