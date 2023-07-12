import pdf2image
import io
import base64
from PIL import Image

def decode_base64(bytevar):
    bytevar.seek(0)
    _base64 = base64.b64encode(bytevar.read())
    return _base64.decode()

class PDF2IMGPDF:
    @staticmethod
    def convert_to_images(file_bytes, dpi=25) -> None:
        _images = pdf2image.convert_from_bytes(
            file_bytes, dpi=dpi
        )
        result = {}
        for k, v in enumerate(_images):
            img_byte_arr = io.BytesIO()
            v.save(img_byte_arr, format='JPEG')
            result[k] = img_byte_arr
        return result
        # return {k: v for k, v in enumerate(_images)}

    @staticmethod
    def decode_images(images):
        return {k: decode_base64(images[k]) for k in images}

    @staticmethod
    def img_to_pdf(images: list) -> None:
        images = [
            Image.open(
                io.BytesIO(
                    base64.b64decode(
                        str(img)
                    )
                )
            ) for img in images
        ]
        pdf_byte_arr = io.BytesIO()
        images[0].save(
            pdf_byte_arr,
            "PDF",
            save_all=True,
            append_images=images[1:]
        )
        return decode_base64(pdf_byte_arr)
