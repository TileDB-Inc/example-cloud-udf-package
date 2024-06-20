# TileDB Cloud UDF usage with package functions

This repository demonstrates the usage of a Python package providing multiple functions for usage with a [TileDB Cloud UDF](https://docs.tiledb.com/cloud/concepts/tiledb-cloud-internals/serverless-udfs)

## Background

First, the requirements:

- Code in the target package needs to import only modules which are available in the TileDB Cloud UDF runtime environment.
- Cross-imports within the target package need to be done at the module level, not within functions. See [example and discussion here](https://github.com/TileDB-Inc/example-cloud-udf-package/blob/bbcc2833211e2a5d728095caf2cd08d3e7099a54/src/packaging_example/important_functions.py#L1-L8).

This sets us up for the important parts.

The `cloudpickle.register_pickle_by_value` function ensures that, when registered functions are pickled, they are serialized as the function's code itself and not an "import X and find function Y" directive. It can be applied to modules, after which functions within the module and sub-modules will all be pickled by value. The easiest way to accomplish this is probably to have the root module register itself. In this demo, this is done within the main `__init__.py` file ([here](https://github.com/TileDB-Inc/example-cloud-udf-package/blob/bbcc2833211e2a5d728095caf2cd08d3e7099a54/src/packaging_example/__init__.py#L8)):

```
# This line ensures that any function within packaging_example or any of its
# submodules is pickled by value rather than as "import X and get member Y".
cloudpickle.register_pickle_by_value(sys.modules[__name__])
```

## Usage

The files `register.py`, `run.py`, `unregister.py` and `update.py` in this package are used for demonstration purposes and are _not_ part of the installed python package.

1. From root of this source tree, `pip install .`
2. `python register.py`
3. `python run.py`
4. (Repeat as necessary)
    - Make code changes to `important_functions.three` or related functions
    - Commit changes
    - Run `update.py` to update the registered UDF on TileDB Cloud
5. (If necessary, run `python unregister.py` to remove the registered UDF.)
