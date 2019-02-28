function f_output(VdsStart,VdsEnd,VdsStep,VgsStart,VgsEnd,VgsStep)


    smua.source.levelv = VdsStart
    smub.source.levelv = VgsStart
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON
    delay(0.1)

    Vg=VgsStart
    while true do
        txt="VDS(" .. Vg .. ") VGS(" .. Vg .. ") IDS(" .. Vg ..") IGS(" .. Vg .. ")"
        print(">>head<<" .. txt)
        smub.source.levelv = Vg

        Vd=VdsStart
        while true do
            smua.source.levelv = Vd
            delay(0.1)
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

smua.measure.autorangei = 1
smub.measure.autorangei = 1

-- MEASUREMENT ROUTINE

f_output(VdsStart,VdsEnd,VdsStep,VgsStart,VgsEnd,VgsStep)

smua.source.output = smua.OUTPUT_OFF
smub.source.output = smub.OUTPUT_OFF
