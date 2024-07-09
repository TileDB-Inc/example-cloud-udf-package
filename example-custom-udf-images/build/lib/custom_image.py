from tiledb.cloud import udf

def test_custom_image():
    import tiledb.cloud
    from tiledb.cloud.utilities import get_logger
    from PIL import Image 
    
    tiledb_py_version = tiledb.__version__
    tiledb_version = tiledb.libtiledb.version()

    img  = Image.new( mode = "RGB", size = (400, 300), color = (209, 123, 193) )
    pixel_value = img.getpixel((50, 100))

    logger = get_logger()
    logger.info(pixel_value)
    logger.info(tiledb_py_version)
    logger.info(tiledb_version)

udf.exec(test_custom_image, namespace="andreas", image_name="my_custom_image")