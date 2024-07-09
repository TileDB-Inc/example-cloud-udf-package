# Sub-modules can also import other modules.
from . import library_b


def two() -> int:
    return library_b.one() + library_b.one()
