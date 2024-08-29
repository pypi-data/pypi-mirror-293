from collections.abc import Callable, Iterable, Mapping, Iterable
from inspect import signature
from itertools import islice
from operator import contains
from typing import Any

from plum import dispatch
from toolz import curry as crr
from toolz import keyfilter


@dispatch
def apply_packed(fnct: Callable, itrb: Iterable) -> Any:
    return fnct(*itrb)


@dispatch
def apply_packed(fnct: Callable, assctbl: Mapping) -> Any:
    return fnct(**assctbl)


def packed(fnct: Callable) -> Callable:
    def fnct_packed(to_be_unpacked: Iterable | Mapping) -> Any:
        return apply_packed(fnct, to_be_unpacked)

    return fnct_packed


def packedmapping(fnct: Callable) -> Callable:
    def fnct_packed(assctbl: Mapping) -> Any:
        return fnct(**assctbl)

    return fnct_packed


@dispatch
def apply_packed_part(fnct: Callable, itrb: Iterable) -> Any:
    return fnct(*islice(itrb, len(signature(fnct).parameters)))


@dispatch
def apply_packed_part(fnct: Callable, assctbl: Mapping) -> Any:
    return fnct(**keyfilter(crr(contains)(signature(fnct).parameters.keys()), assctbl))


def packedpart(fnct: Callable) -> Callable:
    def fnct_packed(to_be_unpacked: Iterable | Mapping) -> Any:
        return apply_packed_part(fnct, to_be_unpacked)

    return fnct_packed


def packedmappingpart(fnct: Callable) -> Callable:
    def fnct_packed(assctbl: Mapping) -> Any:
        return fnct(**keyfilter(crr(contains)(signature(fnct).parameters.keys()), assctbl))

    return fnct_packed


if __name__ == "__main__":

    def test_fnct_add(x: int, y: int) -> int:
        added = x + y
        print(f"{x} added to {y} produces {added}")
        return added

    data_args = [1, 2]
    data_kwargs = {"x": 1, "y": 2}
    assert apply_packed(test_fnct_add, data_args) == 3
    assert packed(test_fnct_add)(data_args) == 3
    assert apply_packed(test_fnct_add, data_kwargs) == 3
    assert packed(test_fnct_add)(data_kwargs) == 3

    data_args_excess = [1, 2, 3]
    data_kwargs_excess = {"x": 1, "y": 2, "z": 3}
    assert apply_packed_part(test_fnct_add, data_args_excess) == 3
    assert packedpart(test_fnct_add)(data_args_excess) == 3
    assert apply_packed_part(test_fnct_add, data_kwargs_excess) == 3
    assert packedpart(test_fnct_add)(data_kwargs_excess) == 3
