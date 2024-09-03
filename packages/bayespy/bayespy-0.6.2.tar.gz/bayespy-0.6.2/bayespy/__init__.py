################################################################################
# Copyright (C) 2011-2016 Jaakko Luttinen
#
# This file is licensed under the MIT License.
################################################################################

from . import utils
from . import inference
from . import nodes

try:
    from . import plot
except ImportError:
    # Matplotlib not available
    pass

from ._meta import __author__, __copyright__, __contact__, __license__

from . import _version
__version__ = _version.get_versions()['version']
