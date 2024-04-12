
接下来的示例，会将一个XMR挖矿项目转换为一行表达式代码，并在计算机上运行该一行表达式代码

1. 以PyAnonymous根目录下 "./测试项目/ReadableCryptoMiner" 的挖矿项目为例，以下简称为ReadableCryptoMiner

    该项目的入口点为 "./测试项目/ReadableCryptoMiner/ggminer.py"

    入口点的入口函数为 main

2. 输入以下指令将会启动对ReadableCryptoMiner的打包过程  

    ```vb
    python .\main.py -e "./测试项目/ReadableCryptoMiner/ggminer.py"
    ```

    输出的一行表达式代码连同调用方法，笔者已经放于 XMR转换.py 中. 供各位学习研究

    笔者写入的矿池、XMR地址均为笔者本人的地址，有需要的读者可以修改 ggminer.py 第42行 ~ 第44行的参数设置