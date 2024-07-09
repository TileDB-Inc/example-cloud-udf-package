import sys

import cloudpickle


# This line ensures that any function within packaging_example or any of its
# submodules is pickled by value rather than as "import X and get member Y".
cloudpickle.register_pickle_by_value(sys.modules[__name__])
