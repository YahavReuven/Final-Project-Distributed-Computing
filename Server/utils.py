import base64
import binascii

from errors import InvalidBase64Error


def validate_base64_and_decode(encoded: str, return_obj=True):
    try:
        obj = base64.b64decode(encoded)
    except binascii.Error:
        raise InvalidBase64Error()
    if return_obj:
        return obj
