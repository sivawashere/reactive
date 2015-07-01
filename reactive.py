from collections import Callable

# reactive.py 
# Written by Siva Somayyajula and Ellis Tsung

class Reactive:
	# create
	def __init__(self, r, *deps):
		if isinstance(r, Reactive):
			self.r    = reactive.r
			self.deps = reactive.deps
		else:
			self.r    = r if isinstance(r, Callable) else lambda: r
			self.deps = deps

	# read
	def __call__(self):
		return self.r(*self.deps)

	# write/modify
	def set(self, r, *deps):
		self.__init__(r, *deps)

	# Reactive object equivalency
	# note: dependancy order matters because Reactive.r is order-sensitive
	def equals(self, other):
		return isinstance(other, Reactive) and self.r == other.r and self.deps == other.deps

	# overload builtins
	def __bool__(self):
		return bool(self.r or self.deps)

	def __len__(self):
		return len(self.deps)

	# emulate list operations
	def __getitem__(self, key):
		if isinstance(key, int):
			return self.deps[key]
		raise TypeError

	def __setitem__(self, key, value):
		if isinstance(key, int):
			self.deps[key] = value
		raise TypeError

	def __iter__(self):
		return iter(self.deps)

	def __contains__(self, item):
		return item in self.deps

	# overload comparisons
	# note: these only compare values
	def __lt__(self, other):
		return self() < other

	def __le__(self, other):
		return self() <= other

	def __eq__(self, other):
		return self() == other

	def __ne__(self, other):
		return self() != other

	def __gt__(self, other):
		return self() > other

	def __ge__(self, other):
		return self() >= other

	# overload operators
	def __add__(self, other):
		return self() + other

	def __sub__(self, other):
		return self() - other

	def __mul__(self, other):
		return self() * other

	def __truediv__(self, other):
		return self() / other

	def __floordiv__(self, other):
		return self() // other

	def __mod__(self, other):
		return self() % other

	def __divmod__(self, other):
		return divmod(self, other)

	def __pow__(self, other):
		return self() ** other

	def __pow__(self, other, modulo):
		return pow(self(), other, modulo)

	def __lshift__(self, other):
		return self() << other

	def __rshift__(self, other):
		return self() >> other

	def __and__(self, other):
		return self() & other

	def __xor__(self, other):
		return self() ^ other

	def __or__(self, other):
		return self() | other

	def __radd__(self, other):
		return other + self()

	def __rsub__(self, other):
		return other - self()

	def __rmul__(self, other):
		return other * self()

	def __rtruediv__(self, other):
		return other / self()

	def __rfloordiv__(self, other):
		return other // self()

	def __rmod__(self, other):
		return other % self()

	def __rdivmod__(self, other):
		return divmod(other, self())

	def __rpow__(self, other):
		return other ** self()

	def __rlshift__(self, other):
		return other << self()

	def __rrshift__(self, other):
		return other >> self()

	def __rand__(self, other):
		return other & self()

	def __rxor__(self, other):
		return other ^ self()

	def __ror__(self, other):
		return other | self()

	def __neg__(self):
		return -self()

	def __pos__(self):
		return +self()

	def __abs__(self):
		return abs(self())

	def __invert__(self):
		return ~self()

	# reject augmented assignment
	def __iadd__(self, other):
		raise TypeError

	def __isub__(self, other):
		raise TypeError

	def __imul__(self, other):
		raise TypeError

	def __itruediv__(self, other):
		raise TypeError

	def __ifloordiv__(self, other):
		raise TypeError

	def __imod__(self, other):
		raise TypeError

	def __ipow__(self, other, modulo=None):
		raise TypeError

	def __ilshift__(self, other):
		raise TypeError

	def __irshift__(self, other):
		raise TypeError

	def __iand__(self, other):
		raise TypeError

	def __ixor__(self, other):
		raise TypeError

	def __ior__(self, other):
		raise TypeError

	# output
	def __str__(self):
		return str(self())
