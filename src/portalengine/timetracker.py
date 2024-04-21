from dataclasses import dataclass


@dataclass
class TimeTracker:
	passed: int = 0
	delta: int = 0

	@property
	def passed_sec(self):
		return self.passed/1000
	
	@property
	def delta_sec(self):
		return self.delta/1000