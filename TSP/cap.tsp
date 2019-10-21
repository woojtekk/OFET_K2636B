function Cap_Leak(vsrc, soak) --Configure instrument to source user-defined voltage
beeper.beep(0.1, 2400)

--and measure current.
--Instrument variables.
local l_soak = soak --Source delay before measurement (Recommended 7RC)
local l_icmpl = 1E-2 --Source compliance
local l_nplc = 1 --Measurement Integration Rate
local l_vsrc = vsrc--Voltage source value
--Define measured and calculated variables
local l_leaki = 0 --Initialize leakage current measurement
local l_leakres = 0 --Initialize leakage resistance measurement
local l_comp_val = false --Initialize compliance variable
--Default setting and level check


if (l_vsrc == nil) then --Use default value
l_vsrc = 40
end --if
if (l_vsrc > 100) then --Coerce source value within range
l_vsrc = 100
print(“Maximum voltage value is 100V!!”)
end --if
if (l_soak == nil) then --Use default value
l_soak = 10
end --if
--Configure source and measure settings
smua.reset() --Reset SMU
errorqueue.clear() --Clear the error queue
smua.source.func = smua.OUTPUT_DCVOLTS --Output Voltage
smua.source.levelv = 0 --Source 0 before enabling output
smua.measure.nplc = l_nplc --Set integration rate
smua.source.autorangev = smua.AUTORANGE_ON --Enable source autorange
smua.source.limiti = l_icmpl
smua.measure.autorangei = smua.AUTORANGE_ON --Enable measurement autorange
--Begin test
beeper.beep(0.1, 2400)

smua.source.output = smua.OUTPUT_ON --Enable output
smua.source.levelv = l_vsrc --Source programmed value
delay(soak) --wait before making measurement
l_comp_val = Check_Comp() --check compliance
if l_comp_val == true then
smua.source.output = smua.OUTPUT_OFF --Disable output
else
l_leaki = smua.measure.i() --measure current
smua.source.output = smua.OUTPUT_OFF --Disable output
l_leakres = Calc_Val(l_vsrc, l_leaki) --calculate
Print_Data(l_leaki, l_leakres) --print
end --if
end --function Cap_Leak()




function Check_Comp() --Function checks state of compliance, if true, prints warning and
beeper.beep(0.1, 2200)

returns
--to run_test()
local l_comp_val = false --Initialize local variable
l_comp_val = smua.source.compliance --Check compliance
if l_comp_val == true then
print(“”)
print(“SMU Source in Compliance!”)
print(“Ensure proper connections, stable device, and settings are correct”)
print(“Rerun Test”)
print(“”)
end --if
return l_comp_val
end --function Check_Comp()
function Calc_Val(vsrc, leaki) --function calculates resistance and voltage coefficient
local l_vsrc = vsrc --Pass global source variable to local
local l_leaki = leaki --Pass global current variable to local
local l_leakres = 0 --Initialize leakage resistance local
l_leakres = vsrc/leaki --Return quotient = resistance calculation
return l_leakres
end --function Calc_Val()
function Print_Data(leaki, leakres)
local l_leaki = leaki
local l_leakres = leakres
print(“”)
print(“**** Data ****”)
print(“”)
print(“Leakage Current: “, l_leaki, “A”) --Print Leakage Current
print(“”)
print(“Leakage Resistance: “, l_leakres, “Ohms”) --Print resistance value
end --function Print_Data()
--Cap_Leak() --Call Cap_Leak() function