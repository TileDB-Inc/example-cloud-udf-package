#!/usr/bin/env python

# This can be run after installing the "packaging_example" package
# and running `register.py`.

import tiledb.cloud
from tiledb.cloud import udf

me = tiledb.cloud.user_profile().username

three = udf.exec(f"{me}/number-three")
print(f"UDF `number-three` result is: {three}")