import os


def is_test_environment():
    return os.environ.get('TEST') == 'true'
