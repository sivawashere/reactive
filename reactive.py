from collections import Callable

# reactive.py 
# Written by Siva Somayyajula and Ellis Tsung

class Reactive:
	def __init__(self, r, *deps):
		self.r    = r if isinstance(r, Callable) else lambda: r
		self.deps = deps

	def __call__(self):
		return self.r(*[dep() for dep in self.deps])

	def set(self, reactive):
		self.r    = reactive.r
		self.deps = reactive.deps

	def set(self, r, *deps):
		self.__init__(r, *deps)