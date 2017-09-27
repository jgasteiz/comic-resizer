import logging
from zipfile import ZipFile

from io import BytesIO
from PIL import Image
from rarfile import RarFile

CBR = 'cbr'
CBZ = 'cbz'


def resize_comic(file):
    """
    Resize a given comic file.
    """

    if file.name.endswith('.{}'.format(CBR)):
        cb_file = RarFile(file)
        cb_type = CBR
    elif file.name.endswith('.{}'.format(CBZ)):
        cb_file = ZipFile(file)
        cb_type = CBZ
    else:
        return None

    # Go through the CBZ/CBR pages and upload all of them to s3.
    resized_comic = BytesIO()
    resized_cbz = ZipFile(resized_comic, 'w')
    for file_name in cb_file.namelist():
        if not file_name.lower().endswith('.jpg') and not file_name.lower().endswith('.png'):
            continue

        print('Found image {}'.format(file_name))

        try:
            img = Image.open(cb_file.open(file_name))
            print('Original size: {}'.format(img.size))
            width, height = img.size
            new_size = (int(width / 2), int(height / 2))
            print('New size: {}'.format(new_size))
            img.resize(new_size, Image.ANTIALIAS)
            output = BytesIO()
            img.save(output, 'JPEG')
            data = output.getvalue()
            resized_cbz.writestr(file_name, data)
        except Exception as e:
            logging.critical(e)

    resized_cbz.close()
    return resized_comic
