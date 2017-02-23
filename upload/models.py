class S2EOutput():
	def __init__(self, s2e_out_dir):
		with open(s2e_out_dir + "warnings.txt", 'r') as destination:
			self.warnings = destination.read().replace("\n", " <br /> ")
		with open(s2e_out_dir + "messages.txt", 'r') as destination:
			self.messages = destination.read().replace("\n", " <br /> ")
		with open(s2e_out_dir + "info.txt", 'r') as destination:
			self.info = destination.read().replace("\n", " <br /> ")

