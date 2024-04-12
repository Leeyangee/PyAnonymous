### [繁體中文](README_en.md)

<div align="center"> <img src="bugctf.png" width = 135 height = 99 /></div>
<p align="center">PyAnonymous: 基于Python3的无落地项目加载解决方案</p>

PyAnonymous(Py匿名)是一个基于Python3的无落地加载解决方案，它可以将一个完整的简单Py项目变为一行简单的Py表达式.  

当攻击者发现目标Python应用的代码执行点，可以在目标服务代码执行点(如exec、eval)执行该行表达式，将会自动将该项目加载进目标内存并可通过预设的命名空间手动调用

<div align="center"> <img src="图片/pic1.png" width = 350 /></div>

💡对于绝大部分项目，都可以一键将其转化为Payload. 对于全部应用(Web应用、框架)的代码执行处，都可以一键向内存中写入项目并运行

<div align="center"> <img src="图片/pic2.png" width = 350 /></div>

### [点这里查看如何将示例项目转换](使用例子/示例test.md)

### [点这里查看如何将一个XMR挖矿项目转换](使用例子/XMR转换.md)

⚠注意事项: 

1. 当前版本暂时不支持相对路径引入(正在努力适配中)
2. 请尽量避免循环引入

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

    调用注入到内存的test项目

    ```py
    import math
    math.test_main.main()
    ```

2. 以默认命名空间生成ReadableCryptoMiner项目的Payload

    ```vb
    python main.py -e './测试项目/ReadableCryptoMiner/ggminer.py'
    ```

    调用注入到内存的ReadableCryptoMiner项目

    ```py
    import math
    math.ggminer.main()
    ```



### [点这里查看如何将示例项目转换](使用例子/示例test.md)


![测试1](https://raw.githubusercontent.com/Leeyangee/PyLineShell/main/%E6%B5%8B%E8%AF%951.png)

# 鸣谢

在开发的过程中，少不了以下开源/开放代码的支持

* 作为测试项目被引入: https://github.com/wkta/ReadableCryptoMiner

<div align="center"> <img src="bugctf.png" width = 135 height = 99 /></div>