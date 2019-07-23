#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import usbtmc
import time

class k2400():
	
	def __init__(self):
		self.Connect2()
	
	def Connect2(self):
		self.inst = usbtmc.Instrument(0x05e6, 0x2636)
		self.inst.write("*CLS")
		return 0
	
	
	def kwrite(self, cmd):
		"""Write to instrument."""
		try:
			assert type(cmd) == str
			self.inst.write(cmd+"\r")
		except AttributeError:
			print('ERROR: Could not write device.')
	
	
	def kread(self):
		"""Read instrument."""
		try:
			r = self.inst.read()
			return r
		except AttributeError:
			print('ERROR: Could not read from device.')
			raise SystemExit
	
	def port_wr(self,cmd):
		self.kwrite(cmd)
		return self.kread()
		
	def info(self):
		# print(self.port_wr('*IDN?\r'))
		print(self.kwrite("OUTP ON"))
		print(self.kwrite(':SOURCE:VOLTAGE 12.345'))
		
		for x in range(0,11,1)+range(10,-1,-1):
			self.kwrite(':SOURCE:VOLTAGE '+str(x))
			print(self.port_wr("MEASure?"))
	
		self.kwrite("OUTP OFF")
	
	def port_error(ser, cmd="aa"):
		err = [":STAT:MEAS?  ",\
		       ":SYST:ERR:ALL?",\
		       "*ESR?  ",\
		       "*OPC?  ",\
		       ":STAT:OPER?  ",\
		       ":STAT:MEAS?  ",\
		       ":STAT:QUES?  "]
		# for x in err:



if __name__ == '__main__':
	kk=k2400()
	start=time.time()
	kk.info()
	print(time.time()-start)
	
