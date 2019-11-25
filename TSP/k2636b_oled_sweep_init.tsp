    reset()
    smua.reset()
    smub.reset()
    --beeper.beep(0.1, 2400)
    format.data              = format.ASCII
    smub.source.limiti       = LIMIT_I
    smub.source.limitv       = LIMIT_V
    smub.source.func         = smub.OUTPUT_DCVOLTS
    display.smub.measure.func = display.MEASURE_DCAMPS
    --smub.measure.count        = 1
    --smub.measure.delay        = 0.5
    smub.measure.delayfactor  = 0.5
    smub.measure.nplc         = NPLC
    smub.measure.autozero     = smub.AUTOZERO_AUTO

    smub.source.levelv = 0
    smub.source.output = smub.OUTPUT_ON
    print(">>head<<V(__) \t I(__)")
endscript

-------- END --------


loadscript mm
		smub.source.levelv = Vg
		beeper.beep(0.1, 2000)
		print(Vg, (smub.measure.i()))

endscript


loadscript exit
	smua.source.output = smub.OUTPUT_OFF
	smub.source.output = smub.OUTPUT_OFF
	beeper.beep(0.1, 2350)
    beeper.beep(0.1, 2450)
    reset()
    smua.reset()
    smub.reset()
    print(">>END<<")






