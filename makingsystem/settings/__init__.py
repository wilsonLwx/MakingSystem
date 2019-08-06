# __author__ = 'wilsonLwx'
# __date__ = '2019/08/07'
from .base import *

db_conf = os.getenv('app_conf', 'dev')

if db_conf == 'dev':
    from .dev import *
else:
    from .test import *
