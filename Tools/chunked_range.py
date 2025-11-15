"""Utilities for producing chunked, range-like iterators.

This module provides `chunked_range`, a small helper that yields
range-like iterators (instances of `range`) that contain at most
`chunk` elements each, stepping from `start` toward `stop` by `stride`.

Assumptions (pre-conditions) the function relies on:
- All inputs are ints.
- start < stop
- stride > 0
- chunk > 0
"""

from typing import Iterator


def chunked_range(start: int, stop: int, stride: int, chunk: int) -> Iterator[range]:
	"""Yield range-like iterators each with at most `chunk` elements.

	Each yielded object is a Python `range(start_i, end_i, stride)` where
	`start_i` is the first element in that chunk and `end_i` is chosen so
	that the range contains at most `chunk` elements and does not reach
	or exceed `stop`.

	Example:
		list(map(list, chunked_range(0, 15, 2, 5))) == [[0,2,4,6,8], [10,12,14]]

	Raises
	------
	ValueError
		If the pre-conditions are violated (start >= stop, non-positive
		stride or chunk).
	"""
	# Basic validation of pre-conditions
	if not isinstance(start, int) or not isinstance(stop, int) or not isinstance(stride, int) or not isinstance(chunk, int):
		raise TypeError("start, stop, stride and chunk must be ints")
	if start >= stop:
		raise ValueError("start must be less than stop")
	if stride <= 0:
		raise ValueError("stride must be > 0")
	if chunk <= 0:
		raise ValueError("chunk must be > 0")

	current = start
	# Each chunk covers at most chunk values, which corresponds to a span
	# of stride * chunk in the numeric domain for the range stop bound.
	while current < stop:
		end = current + stride * chunk
		if end > stop:
			end = stop
		# Use Python's range which is itself an iterator-like and lazy.
		yield range(current, end, stride)
		current = end


__all__ = ["chunked_range"]

