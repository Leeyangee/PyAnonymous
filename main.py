#by leeya_bug

DEP_SIGN = '#dep '

import os
import sys
import base64
from typing import Tuple
from typing import List
from typing import Dict
import types
import importlib
from pathlib import Path
import re
import argparse
import chardet

class logger:

    class PrintDep(object):
        '''
        打印日志并在with 的代码块中依赖缩进
        '''
        def __init__(self, text: str) -> None:
            global prev
            print(prev + text)

        def __enter__(self) -> None:
            global prev
            prev += '  '

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            global prev
            prev = prev[2:]

prev = ''

class Serialize(object):

    class EnvAdd(object):
        '''
        添加依赖的环境变量路径，必须以with EnvAdd(path)调用
        '''
        def __init__(self, path: str) -> None:
            self.path = path

        def __enter__(self) -> None:
            sys.path = [self.path] + sys.path

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            sys.path = sys.path[1:]

    def depMerge(self, main: dict, branch: dict) -> None:
            '''
            依赖链合并，将分支依赖链 branch 合并进主依赖链 main 中
            '''
            if branch == {}:
                return
            for branch_key in branch.keys():
                if branch_key in main:
                    self.depMerge(main[branch_key][1], branch[branch_key][1])
                else:
                    main[branch_key] = branch[branch_key]

class DirSerialize(Serialize):

    def __init__(self, path: str, import1: list = []) -> None:
        # 'self.dirname' 保存当前模块所在位置
        self.path: str = path
        self.depChain = dict()
        self.__init__Code_List: List[str] = ['']
        self.import1: list = import1

        self.depMerge(self.depChain, self.analyzeMultiDependence(path))

    def analyzeMultiDependence(self, path):
        '''
        查找path目录下的module，并将module加载到该namespace中
        '''
        depChain = dict()
        if True:
            for file in os.listdir(path):
                file: str
                if True:
                    if file.endswith('.py'):
                        pkg_name: str = path_to_pkgname(file)
                    else:
                        pkg_name: str = file
                    #是 from ... import ... 引入的包或者包名为 __init__ 时
                    if pkg_name in self.import1 or pkg_name == '__init__':
                        #with logger.PrintDep(f'正在分析namespace中包: ' + pkg_name):
                            with self.EnvAdd(path):
                                curDependence: types.ModuleType = importlib.import_module(pkg_name)
                                print(sys.path)
                                print(curDependence.__file__)
                            if hasattr(curDependence, '__file__'):
                                #若该依赖为namespace
                                if hasattr(curDependence, '__path__'):
                                    with logger.PrintDep(f'包: {pkg_name} 为namespace'):
                                        depChain[pkg_name] = DirSerialize(list(curDependence.__path__)[0]).getRes()
                                #若该依赖为module
                                else:
                                    with logger.PrintDep(f'包: {pkg_name} 为module'):
                                        if pkg_name == '__init__':
                                            res1 = DocSerialize(curDependence.__file__).getRes()
                                            self.__init__Code_List = res1[0]
                                            self.depMerge(depChain, res1[1])
                                        else:
                                            depChain[pkg_name] = DocSerialize(curDependence.__file__ ).getRes()                            
        return depChain
    
    def getRes(self) -> list:
        '''
        最后返回一个经编码序列化后的依赖链

        一个依赖链包含以下两个部分: module源代码 module的依赖
        '''
        return [ self.__init__Code_List, self.depChain ]
        

class DocSerialize(Serialize):

    class DocClass(object):
        '''
        文件处理类
        '''
        def __init__(self, path: str) -> None:
            self.path: str = path
            self.fromImport: Dict[str, List[str]] = {}

            self.analyzeDependence(self.path)
            self.analyzeCode(self.path)

        def addFromImport(self, from1: str, import1: str) -> None:
            if from1 not in self.fromImport:
                self.fromImport[from1] = []
            self.fromImport[from1].append(import1)
                
        def getFromImport(self, from1: str) -> list:
            if from1 not in self.fromImport:
                self.fromImport[from1] = []
            return self.fromImport[from1]

        def analyzeDependence(self, path: str) -> None:
            '''
            静态分析路径path的py文件包含哪些依赖
            '''
            if os.path.exists(path) and os.path.isfile(path):
                dependence = set()
                with open(path, 'r', encoding='utf-8') as f:
                    lines: list = f.readlines()
                for line in lines:
                    line: str
                    line = line.strip('\n')
                    #分析手动添加的 #dep 依赖
                    if line.startswith(DEP_SIGN):
                        result = line.split(DEP_SIGN)[1].strip(' ')
                        dependence.add(result)
                    
                    line = line.split('#')[0]
                    #分析 import *** 的依赖
                    if line.startswith('import '):
                        #分析有as情况
                        if ' as ' in line:
                            result = line.split('import ')[1].split(' as ')[0].strip(' ')
                        #分析无as情况
                        else:
                            result = line.split('import ')[1].strip(' ')

                        #逗号多个引入的情况
                        if ',' in result:
                            dependence |= { res.strip(' ') for res in  result.split(',') }
                        else:
                            dependence.add(result)
                    #分析 from *** import *** 的依赖
                    if line.startswith('from '):
                        #分析有as情况
                        if ' as ' in line:
                            from1: str = line.split('from ')[1].split(' import ')[0]
                            import1: str = line.split('import ')[1].split(' as ')[0]
                        #分析无as情况
                        else:
                            from1: str = line.split('from ')[1].split(' import ')[0]
                            import1: str = line.split('import ')[1]

                        #逗号多个引入的情况
                        if ',' in import1:
                            for i1 in import1.split(','): self.addFromImport(from1, i1.strip(' '))
                        else:
                            self.addFromImport(from1, import1)
                        dependence.add(from1)
                self.dependence: set = dependence
            else:
                raise NameError(f'{path} 该文件不存在，无法读取其依赖')

        def analyzeCode(self, path: str) -> None:
            '''
            读取路径path的code，并将其base64编码
            '''
            if os.path.exists(path) and os.path.isfile(path):
                with open(path, 'r', encoding='utf-8') as f:
                    code = f.read()
                code_base64ed = base64.b64encode(code.encode()).decode()
                self.code = code
                self.code_base64ed = code_base64ed
            else:
                raise NameError(f'{path} 该文件不存在，无法读取代码内容')
        
        def getDependence(self) -> Tuple[set, Dict[str, List[str]]]:
            return self.dependence, self.fromImport

        def getCode(self) -> Tuple[str, str]:
            return self.code, self.code_base64ed

    def __init__(self, path: str) -> None:
        self.doc = self.DocClass(path)
        # 'self.dirname' 保存当前模块所在位置
        self.dirname = os.path.dirname(path)
        self.depChain: Dict[str, list] = dict()

        def depList(dep: str) -> list:
            '''
            将多个依赖分割成列表
            '''
            return dep.strip('.').split('.')
        
        dependence, fromimport = self.doc.getDependence()
        self.fromimport: Dict[str, List[str]] = fromimport

        for dep in dependence:
            depChainBranch = self.analyzeMultiDependence(dependence = dep)
            self.depMerge(self.depChain, depChainBranch)

    def analyzeMultiDependence(self, dependence: str) -> dict:
        '''
        分析多重依赖的函数
        '''
        pkg_name: str = dependence

        #with self.EnvAdd(self.dirname):
        if True:
            try:
                curDependence: types.ModuleType = importlib.import_module(pkg_name)
            except:
                raise NameError(f'包: {pkg_name} 引入失败，请检查其是否存在或其子依赖是否存在')

        #若该依赖包含__file__
        if hasattr(curDependence, '__file__'):
            dep_location = curDependence.__file__ if curDependence.__file__ != None else list(curDependence.__path__)[0]
            dad = Path(entry_path)
            son = Path(dep_location)
            #若该依赖在项目路径下，则非 官方依赖
            if dad in son.parents:
                #若该依赖为namespace, 下列步骤将namespace解释为module. 有__path__变量必为namespace
                if hasattr(curDependence, '__path__'):
                    with logger.PrintDep(f'包: {pkg_name} 为namespace'):
                        if pkg_name in self.fromimport:
                            return {
                                pkg_name: DirSerialize(list(curDependence.__path__)[0], self.fromimport[pkg_name]).getRes()
                            }
                        else:
                            return {
                                pkg_name: DirSerialize(list(curDependence.__path__)[0], []).getRes()
                            }
                #若该依赖为module
                else:
                    with logger.PrintDep(f'包: {pkg_name} 为module'):
                        return {
                            pkg_name: DocSerialize(curDependence.__file__).getRes()
                        }
            #若该依赖不在项目路径下，无关库或官方依赖不处理
            else:
                logger.PrintDep(f'包: {pkg_name} 为官方库或无关库不处理')
                return {}
        #若该依赖不包含__file__，官方依赖
        else:
            logger.PrintDep(f'包: {pkg_name} 为官方库不处理')
            return {}
        
    def getRes(self) -> list:
        '''
        最后返回一个经编码序列化后的依赖链

        一个依赖链包含以下两个部分: module源代码 module的依赖
        '''
        return [ [self.doc.getCode()[1]], self.depChain ]

class Payload(object):

    loaderList: list = [('''
def surface_ZzRTSoDE(m, n):
    def deep_ZzRTSoDE(mn, c, d):
        a=__import__('imp').new_module(mn)
        for d1 in d:
            a.__dict__[d1]=deep_ZzRTSoDE(d1, d[d1][0], d[d1][1])
            __import__('sys').modules[d1] = a.__dict__[d1]
        for c1 in c: exec(__import__('base64').b64decode(c1), a.__dict__)
        return a
    for i in m:n[i]=deep_ZzRTSoDE(i, m[i][0], m[i][1])
''', 'surface_ZzRTSoDE')#普通加载器
]
    
    initerList: list = [
        '''str(exec(__import__('base64').b64decode('{loader_base64}').decode()))+str({loader_entry}(eval(__import__('base64').b64decode('{depChain}').decode()), {namespace}))'''
    ]

    def __init__(self, depChain: dict, namespace: str, loader: int = 0, initer: int = 0) -> None:
        self.depChain = depChain
        self.namespace = f'__import__(\'{namespace}\').__dict__'

        self.initer = initer
        self.loader = loader

    def getIniter(self) -> str:
        '''
        初始化器能够将加载器、依赖链加载到内存中，并启动加载器
        '''
        return self.initerList[self.initer]

    def getLoader(self) -> Tuple[str, str]:
        '''
        加载器能够将 编码序列化后的依赖链 转换为 module实例
        '''
        return (base64.b64encode(self.loaderList[self.loader][0].encode()).decode(), self.loaderList[self.loader][1])
    
    def getdepChain(self) -> str:
        '''
        依赖链根据DocSerialize类转换而来，依赖链能被 加载器加载 后转换为 module实例
        '''
        return base64.b64encode(str(self.depChain).encode()).decode()

    def getRes(self) -> str:
        loader_base64, loader_entry = self.getLoader()
        return self.getIniter().format(loader_base64 = loader_base64, loader_entry = loader_entry, depChain = self.getdepChain(), namespace = self.namespace)

def path_to_pkgname(path: str) -> str:
    '''
    路径提取模块名称
    '''
    return os.path.splitext(os.path.basename(path))[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="PyAnonymous(Py匿名)是一个基于Python3的无落地加载解决方案，它可以将一个完整的简单Py项目变为一行简单的Py表达式"
    )
    parser.add_argument("-e", "--entry", default="./测试项目/test/test_main.py", help="要加载的项目入口(默认为自带测试项目)")
    parser.add_argument("-n", "--namespace", default='math', help="要将项目入口加载到的命名空间(默认为 math)")
    parser.add_argument("-s", "--start" , action='store_true', default=False, help='GAT with sparse version or not.')
    options = parser.parse_args(sys.argv[1:])

    entry = options.entry
    namespace = options.namespace
    start = options.start

    entry_name = path_to_pkgname(entry)

    entry_path = os.path.dirname(entry)
    sys.path.append(entry_path)

    print(f'---------------------依赖分析---------------------')
    depChain = DocSerialize(entry)
    print(depChain.getRes())
    depChain = { entry_name: depChain.getRes() }
    print(f'---------------------生成的Payload---------------------')
    payload = Payload(depChain = depChain, namespace = namespace)
    result = payload.getRes()
    print(result)
    if start:
        print(f'---------------------试运行结果---------------------')
        exec(result)
        exec(f'''
import {namespace}
{namespace}.{entry_name}.main()
             ''')
