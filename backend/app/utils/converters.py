from psycopg2.extras import NumericRange
import typing as t


# ******************************************************
# convert from one data type to another.
# especially helpful for postgresql-specific types
# like Int4Range.
# ******************************************************


def int4range2list(l: t.List[int]) -> t.Optional[t.List]:
    """
    convert a postgres `int4range` into a list: postgres' `int4range`
    type increments the top year by 1 (`[1994,1997]` -> `[1994,1998)`),
    so we need to retroconvert it. string representation of the list
    will be done on the front end.
    sqlalchemy aldready converts int4range types to list, so we receive
    a list as input.
    see: https://www.psycopg.org/docs/extras.html#psycopg2.extras.NumericRange
    """
    if l is not None:
        return [ l.lower, l.upper-1 ]
    return None


def list2int4range(l:t.List[int]) -> NumericRange | t.List:
    """
    the contrary of the above function: transform
    a list into a postgresql Int4Range.
    """
    if len(l) != 0 and len(l) != 2:
        raise ValueError(f"converters.list2int4range: length of input "
                        +f"list must be 0 or 2, got `{len(l)}` on list `{l}`")
    if l is not None and len(l):
        return NumericRange(lower=l[0], upper=l[1]+1, bounds="[)")
    return l

