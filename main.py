#by leeya_bug

import os

class Doc2Dict():
    class docClass(object):
        def __init__(self, path):
            self.path = path
            

        def analyzeDependence(path) -> set:
            dependence = set()
            with open(path) as f:
                lines = f.readlines()
            for line in lines:
                if line.startswith('#dep '):
                    dependence.append(line.split('#dep ')[1])
                
            

        def getOriginalCode(path):
            pass

    def __init__(self, path):
        self.dep = self.readPath(path)
        self.dep = self.analyseDep(self.dep)
        print(self.dep)


a = Doc2Dict('./test')



if False:

    import base64
    import yaml
    import os

    with open(relation, 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)

    def generate(depen_ori):
        dependence = {}
        for mod in depen_ori:
            if not os.path.isdir(depen_ori[mod]['file']):
                with open(depen_ori[mod]['file'],'rb') as f:
                    content = base64.b64encode(f.read()).decode()
            else:
                content = ''
            if 'dependence' in depen_ori[mod]:
                dep = generate(depen_ori[mod]['dependence'])
            else:
                dep = {}
            dependence[mod] = (content, dep)
        return dependence

    moban = generate(result)
    moban = base64.b64encode(str(moban).encode()).decode()

    a = base64.b64encode('''
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

    payload = f'''str(exec(__import__('base64').b64decode('{a}').decode()))+str(surface_ZzRTSoDE(eval(__import__('base64').b64decode('{moban}').decode()), {namespace}))'''


    print(payload)


if __name__ == "__main__":
    print('请阅读 解释.md 获取更多操作细节')
    namespace = input('''请输入要落地的命名空间(默认为 __import__('math').__dict__): ''')
    namespace = namespace if namespace != '' else "__import__('math').__dict__"
    relation = input('''请输入依赖关系配置文件(默认为 依赖关系.yml): ''')
    relation = relation if relation != '' else "依赖关系.yml"