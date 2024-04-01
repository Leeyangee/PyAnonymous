#dep test3
#dep test12

import test3
from test12 import test4

def test2():
    return test3.test3() + test3.var + test4.test4()