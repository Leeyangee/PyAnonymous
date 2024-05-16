### [繁體中文](README_en.md)

<div align="center"> <img src="https://leeyabug-top-1309475701.cos-website.ap-nanjing.myqcloud.com/PyAnonymous/bugctf.png" width = 135 height = 99 /></div>
<p align="center">PyAnonymous: 基于Python3的无落地项目加载解决方案</p>

PyAnonymous(Py匿名)是一个基于Python3的无落地内存马加载解决方案，它可以将一个完整的简单Py项目变为一行简单的Py表达式.  

📕PyAnonymous的原理是：使用反射等手段将用户的Py项目注入到其他计算机的默认的官方库(如: math、socket)中，并在该官方库下预留项目入口，使得用户的Py项目在其他计算机的内存中持久化并方便调用

👊PyAnonymous相比于其他项目的优点在于：  
1. PyAnonymous将会自动处理简单的依赖，会将依赖和主文件一起打包至表达式中. 
2. PyAnonymous倡导全程无落地，在加载时无需任何文件落地.
3. PyAnonymous为项目入口文件提供预留攻击者接口，将入口文件以模块的形式注入进默认math库中，方便攻击者调用

在PyAnonymous生成表达式后，当攻击者发现目标Python应用的代码执行点，可以在目标服务代码执行点(如exec、eval)执行该行表达式，将会自动将该项目加载进目标内存并可通过预设的math手动调用

<div align="center"> <img src="https://leeyabug-top-1309475701.cos-website.ap-nanjing.myqcloud.com/PyAnonymous/pic1.png" width = 350 /></div>

💡对于绝大部分项目，都可以一键将其转化为Payload. 对于全部应用(Web应用、框架)的代码执行处，都可以一键向内存中写入项目并运行

<div align="center"> <img src="https://leeyabug-top-1309475701.cos-website.ap-nanjing.myqcloud.com/PyAnonymous/pic2.png" width = 350 /></div>

### [点这里查看如何将示例项目转换](使用例子/示例test.md)

### [点这里查看如何将一个XMR挖矿项目转换](使用例子/XMR转换.md)


🦙这是我自己的一个练手项目，希望师傅们多多包涵. 各位师傅可以提issue反馈问题

由leeya_bug开发

# 安装

下载并进入PyAnonymous: 
```vb
git clone https://github.com/Leeyangee/PyAnonymous
cd PyAnonymous
```

# 快速开始

1. 以默认命名空间生成test项目的Payload

    

    ```vb
    python main.py -e './测试项目/test/test_main.py'
    ```

    在其他计算机运行Payload后，项目入口文件 test_main.py 作为模块被注入至 math 模块中即: math.test_main，以下代码调用注入到内存的test项目入口中的函数

    ```py
    import math
    math.test_main.main()
    ```

2. 以默认命名空间生成ReadableCryptoMiner项目的Payload

    ```vb
    python main.py -e './测试项目/ReadableCryptoMiner/ggminer.py'
    ```

    在其他计算机运行Payload后，项目入口文件 ggminer.py 作为模块被注入至 math 模块中即: math.ggminer，以下代码调用注入到内存的ReadableCryptoMiner项目入口中的函数

    ```py
    import math
    math.ggminer.main()
    ```

在默认情况下，项目将会被加载至 math.<入口文件名称>中，您可以使用以下代码调用加载至内存中的项目
```py
import math
math.<入口文件名>.<文件中的函数>()
```



### [点这里查看如何将示例项目转换](使用例子/示例test.md)


# 注意事项

1. ⚠在您的项目中引入模块时，如果您是手动引入模块(如下列代码所示)
   ```py
    __import__('test_mod').get()
   ```
   请在该文件前添加格式为#dep <模块名> 的注释使得PyAnonymous在打包时能将该依赖一同打包，如下所示
   ```py
    #dep test_mod

    __import__('test_mod').get()
   ```

2. ❌当前版本暂时不支持相对路径引入(正在努力适配中)
   ```py
   from .display import dis #不支持相对路径导入，请更改为绝对路径导入
   ```

3. ⚠PyAnonymous生成的Payload跨平台
   
4. ⚠一般来说，在test项目中支持的导入方式，正式环境中都完美支持

# 鸣谢

在开发的过程中，少不了以下开源/开放代码的支持

* 作为测试项目被引入: https://github.com/wkta/ReadableCryptoMiner

* 作为测试项目被引入: https://github.com/kingkaki/weblogic-scan

<div align="center"> <img src="https://leeyabug-top-1309475701.cos-website.ap-nanjing.myqcloud.com/PyAnonymous/bugctf.png" width = 135 height = 99 /></div>