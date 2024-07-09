# All imports within the packaging_example library must be at module level,
# not as internal imports within the function. Anything else that is imported
# must be either part of the standard library or another package that is
# already available in the UDF execution environment.

# In this example, we use relative imports of modules, but this is not required;
# you can directly import functions or use fully qualified names when importing.
from . import library_a
from . import library_b


def three() -> int:
    return library_a.two() + library_b.one()
