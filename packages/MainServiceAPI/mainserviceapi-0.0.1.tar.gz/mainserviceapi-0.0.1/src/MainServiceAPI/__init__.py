"""
\u0420\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u0447\u0438\u043A: MainPlay TG
https://t.me/MainPlayCh"""

__scripts__ = []
import sys
imported = False
if sys.platform == "linux":
  from .linux import *
  imported = True
if not imported:
  raise RuntimeError("Unsupported platform: %r" % sys.platform)
del imported
from ._module_info import version as __version__
