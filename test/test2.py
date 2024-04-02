#dep test3
#dep test12.test4
#dep test12.test6

import test3
from test12.test4 import test4
import test12.test6

def test2():
    return test3.test3() + test3.var + test4() + test12.test6.test6()