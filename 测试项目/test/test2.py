#dep test3

from test12 import test6
from test12 import test4
from test12.test121.test1211 import test1211
import test34

def test2():
    return __import__('test3').test3() + __import__('test3').var + test6.test6(2)  + test4.test4() + test1211() + test34.a