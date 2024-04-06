#by leeya_bug

DEP_SIGN = '#dep '

import os
import sys
import base64
from typing import Tuple
from typing import List
import types
import importlib
from pathlib import Path
import re
import argparse

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

class DocSerialize(object):

    class DocClass(object):
        '''
        文件处理类
        '''
        def __init__(self, path: str) -> None:
            self.path = path
            self.analyzeDependence(self.path)
            self.analyzeCode(self.path)

        def analyzeDependence(self, path: str) -> None:
            '''
            静态分析路径path的py文件包含哪些依赖
            '''
            if os.path.exists(path) and os.path.isfile(path):
                dependence = set()
                with open(path, 'r') as f:
                    lines: list = f.readlines()
                for line in lines:
                    line: str
                    line = line.strip('\n')
                    #分析手动添加的 #dep 依赖
                    if line.startswith(DEP_SIGN):
                        result = line.split(DEP_SIGN)[1].strip(' ').strip('.')
                        dependence.add(result)
                    
                    line = line.split('#')[0]
                    #分析 import *** 的依赖
                    if line.startswith('import'):
                        result = line.split('import ')[1].strip(' ').strip('.')
                        if ',' in result:
                            result: set = { res.strip(' ').strip('.') for res in  result.split(',') }
                            dependence |= result
                        else:
                            dependence.add(result)
                    #分析 from *** import *** 的依赖
                    if line.startswith('from'):
                        result = set(re.findall(r'from (.*?) import', line))
                        result_filter = { r.strip(' ').strip('.') for r in result }
                        dependence |= result_filter
                self.dependence: set = dependence
            else:
                raise NameError(f'{path} 该文件不存在，无法读取其依赖')

        def analyzeCode(self, path: str) -> None:
            '''
            读取路径path的code，并将其base64编码
            '''
            if os.path.exists(path) and os.path.isfile(path):
                with open(path, 'r') as f:
                    code = f.read()
                code_base64ed = base64.b64encode(code.encode()).decode()
                self.code = code
                self.code_base64ed = code_base64ed
            else:
                raise NameError(f'{path} 该文件不存在，无法读取代码内容')
        
        def getDependence(self) -> set:
            return self.dependence

        def getCode(self) -> Tuple[str, str]:
            return self.code, self.code_base64ed
    
    class EnvAdd(object):
        '''
        添加依赖的环境变量路径，必须以with EnvAdd(path)调用
        '''
        def __init__(self, path: str) -> None:
            self.path = path

        def __enter__(self) -> None:
            sys.path.append(self.path)

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            sys.path.remove(self.path)

    def __init__(self, path: str) -> None:
        self.doc = self.DocClass(path)
        # 'self.dirname' 保存当前模块所在位置
        self.dirname = os.path.dirname(path)
        self.depChain = dict()

        def depMerge(main: dict, branch: dict) -> None:
            '''
            依赖链合并，将分支依赖链 branch 合并进主依赖链 main 中
            '''
            if branch == {}:
                return
            branch_key = list(branch.keys())[0]
            if branch_key in main:
                depMerge(main[branch_key][1], branch[branch_key][1])
            else:
                main[branch_key] = branch[branch_key]

        def depList(dep: str) -> list:
            '''
            将多个依赖分割成列表
            '''
            return dep.strip('.').split('.')

        for dep in self.doc.getDependence():
            depChainBranch = self.analyzeMultiDependence(dependence = depList(dep))
            depMerge(self.depChain, depChainBranch)

    #弃用的分析函数，适用于多层namespace情况 
    '''
    def analyzeMultiDependence(self, dependence: list, dependence_num : int = 1) -> dict:
        sys.path.append(self.dirname)
        curDependence: types.ModuleType = importlib.import_module('.'.join(dependence[: dependence_num]))
        sys.path.remove(self.dirname)

        if curDependence.__file__ == None:
            
        else:
            return {
                dependence[dependence_num - 1]: DocSerialize(curDependence.__file__).getRes()
            }
    '''

    def analyzeMultiDependence(self, dependence: list, dependence_num : int = 1) -> dict:
        '''
        分析多重依赖的函数
        '''
        pkg_name: str = '.'.join(dependence[: dependence_num])
        dep_name: str = dependence[dependence_num - 1]

        with self.EnvAdd(self.dirname):
            try:
                curDependence: types.ModuleType = importlib.import_module(pkg_name)
            except:
                raise NameError(f'包: {pkg_name} 引入失败，请检查其是否存在或其子依赖是否存在')

        #若该依赖包含__file__
        if hasattr(curDependence, '__file__'):
            dep_location = curDependence.__file__ if curDependence.__file__ != None else list(curDependence.__path__)[0]
            dad = Path(self.dirname)
            son = Path(dep_location)
            #若该依赖在引入的路径下，则必不为 官方依赖
            if dad in son.parents:
                #若该依赖为namespace, 下列步骤将namespace解释为module. 有__path__变量必为namespace
                if hasattr(curDependence, '__path__'):
                    with logger.PrintDep(f'包: ' + pkg_name + ' 为namespace'):
                        def dirSearch(path: str) -> dict:
                            '''
                            查找path目录下的module，并将module加载到该namespace中
                            '''
                            depChain = dict()
                            with self.EnvAdd(path):
                                for file in os.listdir(path):
                                    file: str
                                    if file.endswith('.py'):
                                        file_basename: str = path_to_pkgname(file)
                                        logger.PrintDep(f'正在分析namespace中包: ' + file_basename)
                                        file_m: types.ModuleType = importlib.import_module(file_basename)
                                        if hasattr(file_m, '__file__'):
                                            if file_m.__file__ != None:
                                                depChain[file_basename] = file_m.__file__
                                return { key: DocSerialize(depChain[key]).getRes() for key in depChain.keys() }

                        return {
                            dep_name: [
                                '',
                                dirSearch(list(curDependence.__path__)[0])
                            ]
                        }
                #若该依赖为module
                else:
                    with logger.PrintDep(f'包: {pkg_name} 为module'):
                        return {
                            dep_name: DocSerialize(curDependence.__file__).getRes()
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
        return [ self.doc.getCode()[1], self.depChain ]

class Payload(object):

    loaderList: list = [('''
def surface_ZzRTSoDE(m, n):
    def deep_ZzRTSoDE(mn, c, d):
        a=__import__('imp').new_module(mn)
        for d1 in d:
            a.__dict__[d1]=deep_ZzRTSoDE(d1, d[d1][0], d[d1][1])
            __import__('sys').modules[d1] = a.__dict__[d1]
        exec(__import__('base64').b64decode(c), a.__dict__)
        return a
    for i in m:n[i]=deep_ZzRTSoDE(i, m[i][0], m[i][1])
''', 'surface_ZzRTSoDE')#普通加载器
]
    
    initerList: list = [
        '''str(exec(__import__('base64').b64decode('{loader_base64}').decode()))+str({loader_entry}(eval(__import__('base64').b64decode('{depChain}').decode()), {namespace}))'''
    ]

    def __init__(self, depChain: dict, namespace: str, loader: int = 0, initer: int = 0) -> None:
        self.depChain = depChain
        self.namespace = namespace

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
    parser.add_argument("-n", "--namespace", default='__import__("math").__dict__', help="要将项目入口加载到的命名空间(默认为 __import('math').__dict__ )")
    options = parser.parse_args(sys.argv[1:])

    entry = options.entry
    namespace = options.namespace

    entry_name = path_to_pkgname(entry)

    print(f'---------------------依赖分析---------------------')
    depChain = DocSerialize(entry)
    depChain = { entry_name: depChain.getRes() }
    print(f'---------------------生成的Payload---------------------')
    payload = Payload(depChain = depChain, namespace = namespace)
    print(payload.getRes())
