from collections import Callable

# reactive.py 
# Written by Siva Somayyajula and Ellis Tsung

class Reactive:
	# create
	def __init__(self, r, *deps):
		if isinstance(r, Reactive):
			self.r    = r.r
			self.deps = r.deps
		else:
			self.r    = r if isinstance(r, Callable) else lambda: r
			self.deps = deps
		self.state = 0
		self.dep_states = None
		self.value = None

	# read
	def changed(self):
		for i in range(len(self.deps)):
			if self.deps[i].state != self.dep_states[i] or self.deps[i].changed():
				return True
		return False

	def __call__(self):
		if self.value is None or self.changed():
			self.dep_states = [dep.state for dep in self.deps]
			self.value = self.r(*self.deps)
		return self.value

	# write/modify
	def set(self, r, *deps):
		self.state += 1
		self.dep_states = None
		self.value = None
		if isinstance(r, Reactive):
			self.r    = r.r
			self.deps = r.deps
		else:
			self.r    = r if isinstance(r, Callable) else lambda: r
			self.deps = deps

	# Reactive object equivalency
	# note: dependency order matters because Reactive.r is order-sensitive
	def equals(self, other):
		return isinstance(other, Reactive) and self.r == other.r and self.deps == other.deps

	# overload builtins
	def __bool__(self):
		return bool(self.r or self.deps)

	def __len__(self):
		return len(self.deps)

	def __hash__(self):
		return hash(self.r) ^ hash(self.deps)

	# emulate list operations
	def __getitem__(self, index):
		if isinstance(index, int):
			return self.deps[index]
		raise TypeError("list indices must be integers, not " + type(index).__name__)

	def __setitem__(self, index, value):
		if isinstance(index, int):
			self.state += 1
			self.dep_states = None
			self.value = None
			self.deps = self.deps[:index] + value + self.deps[index + 1:]
		raise TypeError("list indices must be integers, not " + type(index).__name__)

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
	@staticmethod
	def package(obj):
		if isinstance(obj, Reactive):
			return obj
		return Reactive(obj)

	def __add__(self, other):
		return Reactive(lambda a, b: a() + b(), self, Reactive.package(other))

	def __sub__(self, other):
		return Reactive(lambda a, b: a() - b(), self, Reactive.package(other))

	def __mul__(self, other):
		return Reactive(lambda a, b: a() * b(), self, Reactive.package(other))

	def __truediv__(self, other):
		return Reactive(lambda a, b: a() / b(), self, Reactive.package(other))

	def __floordiv__(self, other):
		return Reactive(lambda a, b: a() // b(), self, Reactive.package(other))

	def __mod__(self, other):
		return Reactive(lambda a, b: a() % b(), self, Reactive.package(other))

	def __divmod__(self, other):
		return Reactive(lambda a, b: divmod(a(), b()), self, Reactive.package(other))

	def __pow__(self, other):
		return Reactive(lambda a, b: a() ** b(), self, Reactive.package(other))

	def __lshift__(self, other):
		return Reactive(lambda a, b: a() << b(), self, Reactive.package(other))

	def __rshift__(self, other):
		return Reactive(lambda a, b: a() >> b(), self, Reactive.package(other))

	def __and__(self, other):
		return Reactive(lambda a, b: a() & b(), self, Reactive.package(other))

	def __xor__(self, other):
		return Reactive(lambda a, b: a() ^ b(), self, Reactive.package(other))

	def __or__(self, other):
		return Reactive(lambda a, b: a() | b(), self, Reactive.package(other))

	def __radd__(self, other):
		return Reactive(lambda a, b: a() + b(), Reactive.package(other), self)

	def __rsub__(self, other):
		return Reactive(lambda a, b: a() - b(), Reactive.package(other), self)

	def __rmul__(self, other):
		return Reactive(lambda a, b: a() * b(), Reactive.package(other), self)

	def __rtruediv__(self, other):
		return Reactive(lambda a, b: a() / b(), Reactive.package(other), self)

	def __rfloordiv__(self, other):
		return Reactive(lambda a, b: a() // b(), Reactive.package(other), self)

	def __rmod__(self, other):
		return Reactive(lambda a, b: a() % b(), Reactive.package(other), self)

	def __rdivmod__(self, other):
		return Reactive(lambda a, b: divmod(a(), b()), Reactive.package(other), self)

	def __rpow__(self, other):
		return Reactive(lambda a, b: a() ** b(), Reactive.package(other), self)

	def __rlshift__(self, other):
		return Reactive(lambda a, b: a() << b(), Reactive.package(other), self)

	def __rrshift__(self, other):
		return Reactive(lambda a, b: a() >> b(), Reactive.package(other), self)

	def __rand__(self, other):
		return Reactive(lambda a, b: a() & b(), Reactive.package(other), self)

	def __rxor__(self, other):
		return Reactive(lambda a, b: a() ^ b(), Reactive.package(other), self)

	def __ror__(self, other):
		return Reactive(lambda a, b: a() | b(), Reactive.package(other), self)

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
		raise TypeError("unsupported operand type(s) for +=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __isub__(self, other):
		raise TypeError("unsupported operand type(s) for |=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __imul__(self, other):
		raise TypeError("unsupported operand type(s) for *=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __itruediv__(self, other):
		raise TypeError("unsupported operand type(s) for /=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __ifloordiv__(self, other):
		raise TypeError("unsupported operand type(s) for //=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __imod__(self, other):
		raise TypeError("unsupported operand type(s) for %=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __ipow__(self, other, modulo=None):
		raise TypeError("unsupported operand type(s) for **=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __ilshift__(self, other):
		raise TypeError("unsupported operand type(s) for <<=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __irshift__(self, other):
		raise TypeError("unsupported operand type(s) for >>=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __iand__(self, other):
		raise TypeError("unsupported operand type(s) for &=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __ixor__(self, other):
		raise TypeError("unsupported operand type(s) for ^=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	def __ior__(self, other):
		raise TypeError("unsupported operand type(s) for |=: 'Reactive' and '" +
		                type(other).__name__ + "'")

	# output
	def __str__(self):
		return str(self())
