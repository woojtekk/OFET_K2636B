loadscript
beeper.beep(0.1, 2400)
smua.reset()

smua.measure.autorangei = smua.AUTORANGE_ON
-- Select measure V autorange.
smua.measure.autorangev = smua.AUTORANGE_ON
-- Select ASCII data format.
format.data = format.ASCII
-- Set buffer count to 100.
smua.measure.count = 10
-- Set measure interval to 0.1 s.
smua.measure.interval = 0.1
-- Select source voltage function.
smua.source.func = smua.OUTPUT_DCVOLTS
-- Output 1 V.
smua.source.levelv = 1
-- Turn on output.
smua.source.output = smua.OUTPUT_ON
-- Create a temporary reading buffer.
mybuffer = smua.makebuffer(smua.measure.count)
-- Store current readings in mybuffer.
smua.measure.overlappedi(mybuffer)
-- Wait for buffer to fill.
waitcomplete()
-- Turn off output.
smua.source.output = smua.OUTPUT_OFF
-- Output readings 1 to 100 from mybuffer.
printbuffer(1, 10, mybuffer)
-- Delete mybuffer.
mybuffer = nil

beeper.beep(0.1, 2400)
beeper.beep(0.1, 2400)

print(">>END<<")
endscript

