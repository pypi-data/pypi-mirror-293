####################################################
# __init__.py for the 'cmpparis' library
# Created by: Sofiane Charrad
####################################################

from .utils import hello_paris
from .document_db_manager import DocumentDBManager

__all__ = ["DocumentDBManager", "hello_paris"]