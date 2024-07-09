import tiledb.cloud
from tiledb.cloud import udf

me = tiledb.cloud.user_profile().username
udf_name = "number-three"

def udf_exists(name):
    try:
        udf.info(name=name, namespace=me)
        return True
    except tiledb.cloud.TileDBCloudError as exc:
        if "Unrecognized array" in str(exc):
            return False
        else:
            raise exc

if udf_exists(udf_name):
    udf.delete(udf_name, me)