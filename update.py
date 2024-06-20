#!/usr/bin/env python

# This can be run after installing the "packaging_example" package.

from packaging_example import important_functions
import tiledb.cloud
from tiledb.cloud import udf

me = tiledb.cloud.user_profile().username

udf.update_udf(important_functions.three, "number-three")