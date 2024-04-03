#by leeya_bug

DEP_SIGN = '#dep '

import os
import sys
import base64
from typing import Tuple
import types
import importlib

class DocSerialize():

    class DocClass(object):

        def __init__(self, path: str):
            self.path = path
            self.analyzeDependence(self.path)
            self.analyzeCode(self.path)

        def analyzeDependence(self, path: str) -> None:
            dependence = set()
            with open(path, 'r') as f:
                lines: list = f.readlines()
            for line in lines:
                if line.startswith(DEP_SIGN):
                    dependence.add(line.split(DEP_SIGN)[1].strip('\n'))
            self.dependence = dependence

        def analyzeCode(self, path: str) -> None:
            with open(path, 'r') as f:
                code = f.read()
            code_base64ed = base64.b64encode(code.encode()).decode()
            self.code = code
            self.code_base64ed = code_base64ed
        
        def getDependence(self) -> set:
            return self.dependence

        def getCode(self) -> Tuple[str, str]:
            return self.code, self.code_base64ed
        
    def __init__(self, path: str):
        self.doc = self.DocClass(path)
        self.dirname = os.path.dirname(path)
        self.depChain = {}

        def depMerge(main: dict, branch: dict) -> dict:
            branch_key = list(branch.keys())[0]
            if branch_key in main:
                depMerge(main[branch_key][1], branch[branch_key][1])
            else:
                main[branch_key] = branch[branch_key]

        for dep in self.doc.getDependence():
            dep_listed = dep.split('.')
            depChainBranch = self.analyzeMultiDependence(dependence = dep_listed)
            depMerge(self.depChain, depChainBranch)
        
    def analyzeMultiDependence(self, dependence: list, dependence_num : int = 1) -> dict:
        sys.path.append(self.dirname)
        print('.'.join(dependence[: dependence_num]))
        curDependence: types.ModuleType = importlib.import_module('.'.join(dependence[: dependence_num]))
        sys.path.remove(self.dirname)

        if curDependence.__file__ == None:
            return {
                dependence[dependence_num - 1]: [
                    '',
                    self.analyzeMultiDependence(dependence = dependence, dependence_num = dependence_num + 1)
                ]
            }
        else:
            return {
                dependence[dependence_num - 1]: DocSerialize(curDependence.__file__).getRes()
            }
        
    def getRes(self) -> set:
        return [self.doc.getCode()[1], self.depChain]


a = DocSerialize('./test/test_main.py')

moban = base64.b64encode(str({'test1': a.getRes()}).encode()).decode()

loader = base64.b64encode('''
def surface_ZzRTSoDE(moban, Namespace):
    def deep_ZzRTSoDE(modName, code, dependence):
        a = __import__('imp').new_module(modName)
        for dep in dependence:
            a.__dict__[dep] = deep_ZzRTSoDE(dep, dependence[dep][0], dependence[dep][1])
            __import__('sys').modules[dep] = a.__dict__[dep]
        exec(__import__('base64').b64decode(code), a.__dict__)
        return a
    for i in moban:Namespace[i]=deep_ZzRTSoDE(i, moban[i][0], moban[i][1])
'''.encode()).decode()

namespace = '__import__("math").__dict__'
payload = f'''str(exec(__import__('base64').b64decode('{loader}').decode()))+str(surface_ZzRTSoDE(eval(__import__('base64').b64decode('{moban}').decode()), {namespace}))'''
print(payload)