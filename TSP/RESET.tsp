reset()
ABORT()
display.clear()
display.settext("$B    --- ABORT ---")
-- Beep in excitement
beeper.beep(0.1, 600)
beeper.beep(0.6, 600)
beeper.beep(0.1, 600)

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
