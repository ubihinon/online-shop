from common.utils import is_test_environment

if is_test_environment():
    from .test import *
else:
    from .dev import *
