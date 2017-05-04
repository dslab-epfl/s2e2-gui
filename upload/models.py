class S2EOutput():
	def __init__(self, has_s2e_error, s2e_out_dir):
		if has_s2e_error != 0 : 
			self.warnings = ""
			self.messages = ""
			self.info = ""
			self.debug = ""
			
		else:	
			with open(s2e_out_dir + "warnings.txt", 'r') as destination:
				self.warnings = destination.read()
			with open(s2e_out_dir + "info.txt", 'r') as destination:
				self.info = destination.read()
			with open(s2e_out_dir + "debug.txt", 'r') as destination:
				self.debug = destination.read()

