import itertools, math, operator, collections.abc as abc

from sys import maxsize
from functools import update_wrapper
from collections import deque, UserDict
from pydrycode import methodtools, callables, attrtools


from_iterable = itertools.chain.from_iterable
irepeat = itertools.repeat
args = operator.attrgetter('start', 'stop', 'step')
div_index = {0, -1}.__contains__
data_method = methodtools.dunder_method('data')

MAP = [itertools.repeat, from_iterable, reversed, itertools.islice,
operator.itemgetter(slice(None, None, -1)), operator.getitem,
operator.floordiv, len, operator.contains, operator.countOf]
MAP[:] = map(callables.bounders.map, MAP)

CC_MAP = MAP[-2:]
del MAP[-2:]
lens = MAP.pop()

ITII = abc.Iterator[tuple[int, int]]
EMPTY_PROD = callables.bounders.iter(((),))
EMPTY_ITERATOR = callables.return_value.__self__
ISLICE = callables.Bounder(itertools.islice)
NWISE_ITER = {1:zip, 2:itertools.pairwise}
MAXSIZE_RANGE = range(maxsize)
SENTINEL = object()


def islice(data, *args):
	'''islice(sequence, stop) --> seqslice object
	islice(sequence, start, stop[, step]) --> seqslice object
	Emulates an slice of a sequence.'''

	itertools.islice(args, *args)
	args = slice(*args)
	if isinstance(data, seqslice):
		return data[args]
	return seqslice(data, MAXSIZE_RANGE[args])


def kwinit(self, /, *data, r=None):
	self.data = data
	self.r = r


def efficient_nwise(iterable:abc.Iterable, n:int) -> abc.Generator[deque]:
	'''Yields efficients nwise views of the given iterable re-using a
	collections.deque object.'''
	
	data = deque(itertools.islice(iterable := iter(iterable), n - 1), n)
	for _ in map(data.append, iterable):
		yield data


def getitems(data, items, /):
	'''fetchs and Yields each item of the data object.'''

	return MAP[5](irepeat(data), items)


def checker(cls, /):
	'''Creates a Check method for SubSequence subclasses'''

	return methodtools.unassigned_method(
		lambda self, obj, /: obj.__class__ is cls and len(obj) == self.r)


def raiser(type, value, /):
	'''Function that raises exception with given value on a class object'''

	def func(self, /):
		raise type(value % self.__class__.__name__)

	return func


def comb_len(cls, /):
	'''Decorator for combinations and permutation classes that computes their lens based
	on their respective math function.'''

	func = getattr(math, cls.__name__[:4])
	
	@cls._new_method
	def __len__(self, /):
		return func(len(self.data), self.r)
	
	return cls


def starred_args(kwarg, /, *, bool_func=None, len_func=None):
	'''Decorator for sequence that accepts multiple sequence and base
	their size on the sizes of their sequences.'''

	def function(cls, /):
		add = cls._new_method
		
		if len_func:
			@add
			def __len__(self, /):
				return len_func(lens(self.data))

		if bool_func:
			add(data_func(bool_func), '__bool__')

		namespace = Sequence.__init__.__globals__
		co_name, default = kwarg
		co = kwinit.__code__.replace(co_varnames=('self', co_name, 'data'))
		func = add(callables.FunctionType(co, namespace, '__init__'))
		func.__kwdefaults__ = {co_name:default}
		return cls

	return function


class Sequence(attrtools.Slots, abc.Sequence, defaults=(None,)):
	'''Base Class for All Sequences off this module.'''
	__slots__ = ('data', 'r')
	data:abc.Sequence
	
	__reversed__ = __bool__ = data_method

	__len__, __contains__, __iter__ = (UserDict.__len__,
		UserDict.__contains__, UserDict.__iter__)

	def __getitem__(self, key, /):
		data = self.data[key]
		return self.__class__(data, self.r) if key.__class__ is slice else data

	def __init_subclass__(cls, /, iter_reverse=None, iter_func=None):
			add_method = cls._new_method
			if iter_reverse:
				factory = cls.__iter__
				iter_func = factory(None)
				add_method(factory(iter_reverse), '__reversed__')

			elif iter_func:
				if iter_func == 1:
					iter_func = getattr(itertools, cls.__name__)
				iter_func = attrtools.slotsfunc(iter_func)

			else:
				return

			add_method(iter_func, '__iter__')


	def __mul__(self, value, /):
		if self._mul:
			return self._replace(data=mul(self.data, value))
		return mul(self, value)

	IndexError = raiser(IndexError, '%s index out of range.')
	
	ValueError = raiser(ValueError, 'Value not in %s object.')

	index = property(operator.attrgetter('data.index'))

	count = property(operator.attrgetter('data.count'))

	def get(self, index, default=None, /):
		'''Return the value for key if key is in the sequence, else default.'''
		try:
			return self[index]
		except IndexError:
			return default

	def iter_index(self:abc.Sequence, value, start:int=0, stop:int=maxsize):
		try:
			while True:
				yield (start := self.index(value, start, stop))
				start += 1
		except (ValueError, TypeError):
			return
		else:
			from more_itertools import iter_index
			yield from iter_index(islice(self, start, stop), value)

	def sub(self, values, start:int=0, stop:int=maxsize, /):
		diff = 1
		first = values[0]
		values = seqslice(values, MAXSIZE_RANGE[diff:])
		while diff:
			index = start = self.index(first, start, stop)
			for start, value in enumerate(values, start + diff):
				if diff := value != self[start]:
					start += diff
					break
		return index


data_func = data_method.factory.with_func


class Range(Sequence):
	__slots__ = ()

	def __init__(self, data, /, *args):
		super().__init__(data, range(*args))

	def extend(self, i:int=1, /):
		r = self.r
		self.r = range(r.start, r.stop + i, r.step)

	def decref(self, i:int=-1, /):
		r = self.r
		self.r = range(r.start, r.stop - i, r.step)


class seqslice(Sequence):
	__slots__ = ()
	r:range

	def __getitem__(func, /):
		def function(self, key, value=None, /):
			return func(self.__class__, self.data,
				key := self.r[key],
				value, key.__class__ is range)
		return update_wrapper(function, func)

	@__getitem__
	def __setitem__(cls, data, key, value, r, /):
		data[slice(*args(key)) if r else key] = value

	@__getitem__
	def __getitem__(cls, data, key, value, r, /):
		return cls(data, key) if r else data[key]

	def __reversed__(self, /):
		size = len(data := self.data)
		start, stop, step = args(r := self.r[::-1])
		if start:
			return getitems(data, r)
		return itertools.islice(itertools.chain((None,), reversed(data)),
			size - start, size - stop, abs(step))
	
	def __iter__(self, /):
		gen = iter(data := self.data)
		start, stop, step = args(r := self.r)
		if start:
			try:
				gen.__setstate__(start)
			except AttributeError:
				return getitems(data, r)
			else:
				stop -= start
				start = 0
		return itertools.islice(gen, start, stop, step)

	def __contains__(self, value, /):
		r = self.r
		try:
			return self.data.index(value, r.start, r.stop) in r
		except ValueError:
			pass
		except TypeError:
			return value in iter(self)

	def __len__(func, FALSIES={'__bool__':False, '__len__':0}, /):
		value = FALSIES[func.__name__]
		def function(self, /):
			if (data := self.data) and (r := self.r):
				return func(data, r)
			return value
		return update_wrapper(function, func)

	@__len__
	def __bool__(data, r, /):
		return start < min(len(data), r.stop) if (start := r.start) else True

	@__len__
	def __len__(data, r, /):
		value = min(len(data), r.stop) - r.start
		return - (-value // r.step) if value > 0 else 0

	def __eq__(self, value, /):
		return (self.__class__ is value.__class__ and
			self.data is value.data and self.r == value.r)

	def __ne__(self, value, /):
		return (self.__class__ is not value.__class__ or
			 self.data is not value.data or self.r != value.r)

	def count(func, /):
		def function(self, value, start:int=0, stop:int=None, /) -> int:
			return func(self.data, value, self.r[+start:+stop])
		return update_wrapper(function, func)

	@count
	def index(data, value, r, /) -> int:
		if r:
			index = data.index
			return r.index(index(value) if start is None 
				else index(value, r.start, r.stop))
		self.ValueError()

	@count
	def count(data, value, r, /) -> int:
		if r:
			try:
				return data.count(value, r.start, r.stop)
			except TypeError:
				data = seqslice(data, r)
				return super().count(value)
		return 0

	@classmethod
	def fromslice(cls, data, slice_obj, /):
		return cls(data, MAXSIZE_RANGE[slice_obj])


@starred_args(('r', None), bool_func=any, len_func=sum)
class chain(Sequence):
	'''Same as itertools.chain but as a sequence.'''
	data:tuple[abc.Sequence]

	__slots__ = ()

	_mul = True

	def __getitem__(self, key, /):
		size = [*lens(data := self.data)]
		if key.__class__ is not slice:
			if key < 0:
				func = None
				data = reversed(data)
				size = reversed(size)
			else:
				func = operator.sub
			
			key = itertools.accumulate(size, func, initial=key)
			for seq, (k1, k2) in zip(data, itertools.pairwise(key)):
				if (k1 ^ k2) < 0:
					return seq[k1]
			self.IndexError()

		start, stop, step = key.indices(sum(size))
		key = step != 1
		values = []
		self = self._replace(data = values)

		for seq, size in zip(data, size):
			values.append(seq := seq[start:stop:step])
			if key:
				start = (step - ((((size - 1) - start) % step)) - 1)
			elif start:
				if seq:
					start = 0
				else:
					start -= size
			if (stop := (stop - size)) <= 0:
				break
		return self
			
	__iter__ = data_func(from_iterable)

	__reversed__ = data_func(callables.compose(reversed, MAP[2],
		from_iterable))
	
	def __add__(self, value, /):
		if self.__class__ is value.__class__:
			self = self.__copy__()
			self.data += value.data
			return value
		return NotImplemented

	def __contains__(func, fmap, /):
		return lambda self, obj, / : func(fmap(self.data, irepeat(obj)))

	__contains__, count = map(__contains__, (any, sum), CC_MAP)

	def index(self, value, start:int=SENTINEL, stop:int=maxsize, /) -> int:
		data = self.data
		size = [*itertools.accumulate(lens(data), initial=0)]
		if start is SENTINEL:
			for data, size in zip(data, size):
				try:
					value = data.index(value)
				except ValueError as e:
					pass
				else:
					return (value + size)
		else:
			if start < 0:
				start += size[-1]
			if stop < 0:
				stop += size[-1]
			for data, (size, n) in zip(data, itertools.pairwise(size)):
				if (r := (start - size)) < n and (n := (stop - size)) > 0:
					try:
						value = data.index(value, r, n)
					except ValueError as e:
						pass
					else:
						return value + size
		self.ValueError()

	@classmethod
	def from_iterable(cls, data:Sequence[Sequence], /):
		(self := cls._Slots__new()).data = data
		return self


class repeat(Sequence, iter_func=1):
	'''Same as itertools.repeat but as a sequence.'''
	__slots__ = ()
	r:int

	def __init__(self, object, times):
		self.data = object
		self.r = times if times > 0 else 0

	def __getitem__(self, key, /):
		data = self.data
		key = range(self.r)[key]
		return repeat(data, len(key)) if key.__class__ is range else data

	def __bool__(self, /):
		return self.r > 0

	def __len__(self, /):
		return self.r

	def __contains__(self, obj, /):
		return self.data == obj

	def __mul__(self, value, /):
		return self._replace(r = self.r * value)

	def __add__(self, value, /):
		if (cls := self.__class__) is value.__class__:
			if (data := self.data) == value.data:
				return cls(data, self.r + value.r)
		return NotImplemented

	def count(self, value, /):
		return self.r if self.data == value else 0

	def index(self, value, start:int=SENTINEL, stop:int=maxsize, /):
		if r := self.r:
			if start is not SENTINEL:
				if start >= min(r, stop):
					self.ValueError()
			if self.data == value:
				return 0
		self.ValueError()


class Size(Sequence):
	'''Base Class for sequence wrappers that transform their sequence size.'''
	__slots__ = ()
	r:int

	def __bool__(self, /):
		return True if self.data and self.r else False


class mul(Size, repeat):
	'''Emulates a data sequence multiplied r times.'''
	__slots__ = ()

	def __getitem__(self, key, /):
		try:
			floordiv, key = divmod(key, len(data := self.data))
			if div_index(floordiv // self.r):
				return data[key]
		except ZeroDivisionError:
			pass
		self.IndexError()

	def __iter__(reverse, /):
		r = MAP[2] if reverse else None
		def func(self, /):
			value = super().__iter__()
			if r:
				value = r(value)
			return from_iterable(value)
		return func

	def __len__(self, /):
		return len(self.data) * self.r

	def __contains__(self, value, /):
		return True if self.r and (value in self.data) else False

	def count(self, value, /) -> int:
		return (r := self.r) and self.data.count(value) * r

	def index(self, value, start:int=SENTINEL, stop:int=maxsize, /) -> int:
		index = self.data.index
		if (r := self.r):
			if start is SENTINEL:
				return index(value)
			div, start = divmod(start, r)
			if div_index(div):
				return index(value, start, stop % r)
		self.ValueError()


class repeats(mul, iter_reverse=True):
	'''Emulates a sequence with each elements repeated r times.'''
	__slots__ = ()

	def __getitem__(self, key, /):
		if (r := self.r):
			return self.data[key // r]
		self.IndexError()

	def __iter__(reverse, fmap=MAP[0], /):
		def func(self, /):
			data = self.data
			if reverse:
				data = reversed(data)
			return from_iterable(fmap(data, irepeat(self.r)))
		return func

	def index(self, value, start:int=SENTINEL, stop:int=maxsize, /) -> int:
		if not (r := self.r):
			self.ValueError()
		index = self.data.index
		if start is SENTINEL:
			return index(value) * r
		start, mod = divmod(start, r)
		return (index(value, start, stop//r) * r) + mod


class SubSequence(Sequence):
	'''Base Class for sequences of sequences'''
	__slots__ = ()
	r:int

	_index, _count = Sequence.index, Sequence.count

	_contains = Sequence.__contains__

	def index(self, value, /, start:int=SENTINEL, stop:int=maxsize):
		if self._check(value):
			if start is SENTINEL:
				start = None
			return self._index(value, start, stop)
		self.ValueError()

	def count(self, value, /):
		return self._count(value) if self._check(value) else 0

	def __contains__(self, value, /):
		return self._check(value) and self._contains(value)

	_check = checker(tuple)


class chunked(Size, SubSequence, iter_reverse=True):
	'''split the given sequence in iterables of r size.'''
	__slots__ = ()

	_mul = True

	def __getitem__(self, key, /):
		key *= (r := self.r)
		key = slice(key, (key + r) or None)
		if key.stop > len(data := self.data):
			Sequence.IndexError(data)
		return self._getitem(data, key)
	
	def __len__(self, /):
		return -(-len(self.data)//self.r)

	def __iter__(r, /):
		def func(self, /):
			return map(methodtools.MethodType(seqslice, self.data),
				itertools.starmap(range, self._indexes(r)))
		return func

	_getitem = seqslice.fromslice

	_check = checker(seqslice)

	def _indexes(self, reverse, rev=MAP[2], /) -> ITII:
		indices = MAXSIZE_RANGE[:len(self.data) + (r := self.r):r]
		if reverse:
			indices = reversed(indices)
		indices = itertools.pairwise(indices)
		if reverse:
			indices = fmap(indices)
		return indices

	def subiter(self, /):
		return itertools.starmap(ISLICE(self.data), self._indexes(None))

	flatten = Sequence.__iter__


class matrix(chunked, iter_reverse=True):
	'''Acts as it like the given sequence was splitted in rows of r size.'''
	__slots__ = ()

	def __iter__(reverse, /):
		def func(self, /):
			return getitems(self.data,
				itertools.starmap(slice, self._indexes(reverse)))
		return func

	def _check(self, value, /) -> bool:
		return value.__class__ is self.data.__class__ and len(value) == self.r

	_getitem  = operator.getitem


class batched(chunked, iter_func=1):
	"""Same as itertools.batched but as a sequence."""
	__slots__ = ()

	def __init__(self, data, n):
		if r < 0:
			raise ValueError("n must be greater than zero")
		super().__init__(data, n)

	def __reversed__(self, /):
		return MAP[4](itertools.batched(reversed(self.data), self.r))

	def _getitem(self, slice_obj, /):
		return tuple(getitems(self.data, MAXSIZE_RANGE[slice_obj]))


@starred_args(('strict', False), bool_func=all, len_func=min)
class sequencezip(SubSequence):
	"""Same as builtins.zip but as a sequence."""
	__slots__ = ()
	data:tuple[abc.Sequence]

	def __getitem__(self, key, /):
		data = tuple(map(operator.itemgetter(key), self.data))
		return self._replace(data) if key.__class__ is slice else data

	def __iter__(self, /):
		return zip(*self.data, strict=self.r)

	def __reversed__(self, revmap=MAP[2], /):
		return zip(*self._reversegen(self._levels(), self.r))

	@staticmethod
	def _reversegen(levels, r, /):
		for i, (data, level) in enumerate(levels):
			data = reversed(data)
			if level:
				if r:
					raise TypeError(f"Sequence #{i} has different size.")
				data = itertools.islice(data, level, None)
			yield data

	def _contains(self, value, /):
		try:
			self.index(value)
		except ValueError:
			return
		else:
			return True

	def _count(self, value, /):
		start = 0,
		try:
			for start in enumerate(self.iter_index(value)):
				pass
		except ValueError:
			return start[0]

	def _check(self, value, /):
		return value.__class__ is tuple and len(value) == len(self.data)

	def _levels(self, /) -> tuple[Sequence, ITII]:
		data = self.data
		n = irepeat(len(self))
		return zip(data, map(abs, map(operator.sub, n, lens(data))))

	def _index(self, values, start, stop, /):
		if data := self.data:
			if start is not None:
				indices = [seq.index(value, start,
					stop) for value, seq in zip(values, data)]
			else:
				indices = [*map(operator.indexOf, data, values)]
			maxvalue = max(indices)
			stop = maxvalue + 1
			n = len(data)
			while indices.count(maxvalue) != n:
				iterable = enumerate(zip(data, values, indices))
				for index, (seq, value, start) in iterable:
					if start != maxvalue:
						indices[index] = seq.index(value, start + 1, stop)
			return maxvalue
		self.ValueError()


@starred_args(('fillvalue', None), bool_func=any, len_func=max)
class zip_longest(sequencezip):
	'''Same as itertools.zip_longest but as a sequence.'''
	__slots__ = ()

	def __getitem__(self, key, /):
		if key.__class__ is slice:
			return super().__getitem__(key)
		default = self.r
		get = Sequence.get
		return tuple(get(data, key, default) if level else data[key]
			for data, level in self._levels())

	def __iter__(self):
		return itertools.zip_longest(*self.data, fillvalue=self.r)

	@staticmethod
	def _reversegen(levels, default, /):
		for data, level in levels:
			data = reversed(data)
			if level:
				data = itertools.chain(irepeat(default, start), data)
			yield data


class combinations(SubSequence):
	'''Base Class for combinatoric sequences. A combinations subclass is a type
	of sequence that returns r-length sucessive tuples of different combinations
	of all elements in data.'''
	__slots__ = ()

	def __bool__(self, /):
		return not (r := self.r) or len(self.data) >= r


class nwise(SubSequence, iter_reverse=True):
	'''Emulates tuples of every r elements of data.'''
	__slots__ = ()

	_mul = True

	def __getitem__(self, key, /):
		return tuple(getitems(self.data, range(key, key + self.r)))

	def __iter__(reverse, _=irepeat(None), /):
		def func(self, /):
			first = data = self.data

			if reverse:
				first = reversed(first)

			if not (r := self.r):
				return irepeat((), len(data))

			elif r in NWISE_ITER:
				return NWISE_ITER[r](first)

			else:
				r = range(1, r)
				first = iter(first)
				if not reverse:
					if hasattr(first, '__setstate__'):
						limit = itertools.islice
					else:
						limit = islice
						args = map(limit, irepeat(data), r, _)
					return zip(first, *args)
		return func

	def __len__(self, /):
		return len(self.data) - (self.r - 1) if self else 0

	def __bool__(self, /):
		return self.r <= len(self.data)

	def _contains(func, /):
		def function(self, value, /):
			data = efficient_nwise(self.data, self.r)
			value = irepeat(deque(value))
			return func(map(operator.eq, data, value))
		return function

	def _index(self, value, start, stop, /):
		return Sequence.sub(self.data, value, start, stop)

	_count = _contains(sum)

	@_contains
	def _contains(stream, /):
		return next(filter(None, stream), None)


@starred_args(('repeat', 1), bool_func=all)
class product(combinations, iter_reverse=True):
	'''Same as itertools.product but acts as a sequence.'''
	__slots__ = ()
	data:tuple[abc.Sequence]

	def __getitem__(self, key, /):
		data, size, _, r, n = self.stats()
		values, key = [], range(n)[key]
		for (data, size, r) in zip(data, size, r):
			values.append(data[((key % (size * r)) // r)])
		return tuple(values)

	def __len__(self, /):
		return math.prod(lens(self.data)) ** self.r

	def __iter__(r, /):
		def func(self, /)  -> zip:
			data, size, count, times, _, = self.stats()
			first, *values = data
			del count[0]
			if not data:
				return EMPTY_PROD()
			if values:
				repeat, unchain, mapreversed = MAP[:3]
				data = repeat(values, count)
				if r:
					first = reversed(first)
					data = map(mapreversed, data)
				values[:] = unchain(data)
				values.insert(0, first)
				values[:-1] = unchain(map(repeat, values[:-1], repeat(times)))
				return zip(*values)
			return zip(first)
		return func

	def _contains(func, fmap, /):
		return lambda self, value, /: func(fmap(self.data * self.r, value))

	def _check(self, value, /) -> bool:
		return value.__class__ is tuple and (len(value)
			// self.r) == len(self.data)

	def stats(self, /) -> tuple[tuple, (r := list[int]), r, r, int]:
		floordiv = MAP[-1]
		size = [*lens(data := self.data)]
		size *= (repeat := self.r)
		*count, n = itertools.accumulate(size, operator.mul, initial=1)
		times = [*floordiv(floordiv(irepeat(n), size), count)]
		return data * repeat, size, count, times, n

	def _index(self, value, start, stop, /):
		data, _, _, repeat, _, = self.stats()
		return math.sumprod(map(operator.indexOf, data, value), repeat)

	_contains, _count = map(_contains, (all, math.prod), CC_MAP)


@comb_len
class permutations(combinations):
	'''Same as itertools.permutations but as a Sequence. IN PROCESS...'''
	__slots__ = ()


@comb_len
class combinations(combinations):
	'''Same as itertools.combinations but as a Sequence. IN PROCESS...'''
	__slots__ = ()


class enumerated(SubSequence, iter_func=enumerate):
	"""Same as builtins.enumerate but as a sequence."""
	__slots__ = ()

	def __init__(self, data, /, start:int=0):
		self.data = data
		self.r = start

	def __getitem__(self, key, /):
		data = self.data
		value = data[key]
		if key < 0:
			key += len(data)
		return (key + self.r, value)
	
	def __reversed__(self, /):
		data = self.data
		return zip(itertools.count(self.r + len(data) - 1, -1), reversed(data))

	def _check(self, value, /):
		return value.__class__ is tuple and len(value) == 2

	def _index(self, value, start, stop, /):
		data = self.data
		index, obj = value
		if start or (r := self.r):
			i = data.index(obj, start, stop)
			if (r + i) == index:
				return value
		else:
			try:
				if data[index] == value:
					return index
			except IndexError:
				pass
		self.ValueError()

	def _count(self, value, /):
		return +(value in self)

	def _contains(self, value, /):
		index, obj = value
		if (r := self.r):
			index = abs(index - r)
		value = Sequence.get(self.data, index, SENTINEL)
		return value is not SENTINEL and value == obj


class compress(Size, iter_func=1):
	__slots__ = ()

	def __getitem__(self, key, /):
		keys = getitems(self.r, itertools.count(key, 1 if key > 0 else -1))
		return self.data[next(filter(None, keys))]


class indexed(Size, iter_func=getitems):
	__slots__ = ()


chain.__args__ = chain.data

repeat.__reversed__ = repeat.__iter__

Sequence.__mul__ = callables.method(mul)


del maxsize, abc, ITII, product.r, UserDict