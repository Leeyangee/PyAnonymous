#dep test3
#dep test12.test6
#dep test12.test4

import test3
from test12 import test6
from test12 import test4

def test2():
    return test3.test3() + test3.var + test6.test6(2)  + test4.test4()