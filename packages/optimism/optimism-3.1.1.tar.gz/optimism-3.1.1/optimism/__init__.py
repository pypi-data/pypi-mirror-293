"""
This package init just imports everything from optimism.py, including
explicitly the version number (which otherwise would be skipped since it
starts with '_'). That way, importing optimism-the-package is the same as
importing optimism-the-file, except that private variables are not
exported by the package. So you can distribute the package OR just the
optimism.py file and both should work the same.
"""

from .optimism import *

from .optimism import __version__
