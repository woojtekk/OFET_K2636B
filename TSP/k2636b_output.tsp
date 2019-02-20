function f_output(VdsStart,VdsEnd,VdsStep,VgsStart,VgsEnd,VgsStep)


    smua.source.levelv = VdsStart
    smub.source.levelv = VgsStart
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON
    delay(1)

    Vg=VgsStart
    while true do
        txt="VDS(" .. Vg .. ") VGS(" .. Vg .. ") IDS(" .. Vg ..") IGS(" .. Vg .. ")"

        print(">>head<<" .. txt)
        smub.source.levelv = Vg

        Vd=VdsStart
        while true do
            smua.source.levelv = Vd
            delay(0.05)

            print(Vd, smua.measure.i(), smub.measure.i(), Vg)

            Vd=Vd+VdsStep

                    if (VdsEnd-Vd) > 0 and VdsStep<0 then break  end
                    if (VdsEnd-Vd) < 0 and VdsStep>0 then break  end

        end

        Vg=Vg+VgsStep
            if (VgsEnd-Vg) > 0 and VgsStep<0 then break  end
            if (VgsEnd-Vg) < 0 and VgsStep>0 then break  end


    end

end



-------- MAIN PROGRAM --------
-- Beep in excitement
reset()
--display.clear()
--display.settext("OUTPUT SWEEP")

--beeper.beep(1, 600)

-- PARAMETERS
LIMIT_I = 1
LIMIT_V = 200
LIMIT_R = 1

-- Clear buffers and make sure the right thing is recorded
smua.nvbuffer1.clear()
smub.nvbuffer1.clear()
smua.nvbuffer1.collectsourcevalues = 1
smub.nvbuffer1.collectsourcevalues = 1
format.data = format.ASCII
smua.nvbuffer1.appendmode = 1
smub.nvbuffer1.appendmode = 1
smua.measure.count = 1
smub.measure.count = 1

-- SMUA setup
smua.measure.delay = smua.DELAY_AUTO
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
smub.measure.delayfactor = DELATE
smub.measure.nplc = NPLC
smub.measure.analogfilter = 0
smub.source.func = smub.OUTPUT_DCVOLTS
smub.source.limiti  = LIMIT_I
smub.source.limitv  = LIMIT_V
smub.measure.rangei = LIMIT_R
smua.sense = smua.SENSE_LOCAL

--DISPLAY settings
display.smua.measure.func = display.MEASURE_DCAMPS
display.smub.measure.func = display.MEASURE_DCAMPS
--display.screen = display.SMUA_SMUB
--display.screen = display.USER

-- MEASUREMENT ROUTINE

f_output(VdsStart,VdsEnd,VdsStep,VgsStart,VgsEnd,VgsStep)

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
