### [繁體中文](README_en.md)

<div align="center"> <img src="bugctf.png" width = 135 height = 99 /></div>
<p align="center">PyLineShell: 一个基于Python3的个人Shell Payload库</p>


PyAnonymous(Py匿名)是一个基于Python3的无落地加载项目，它可以将一个完整的项目加载为

🔍生成的Payload基本上为简单的一行表达式代码，主要针对于无法赋值、无法多行输入的命令执行点. 

💽主要适用于不落地内存加载Py代码、无落地处理Py项目依赖并运行Py项目源码、无回显不出网等场景，用户可以直接在目标机器一键无文件落地运行Py项目代码. 

💡对于绝大部分应用(Web应用、框架)的命令执行处，都可以一键命令执行和一键写入代码

🦙这是我自己的一个练手项目，希望师傅们多多包涵. 各位师傅可以提issue反馈问题

由leeya_bug开发

# 安装并使用

```cmd
git clone https://github.com/Leeyangee/PyLineShell
cd PyLineShell
```

# 快速开始

使用Python生成一个普通版执行命令的Payload

![测试1](https://raw.githubusercontent.com/Leeyangee/PyLineShell/main/%E6%B5%8B%E8%AF%951.png)

使用Python ASCII码代码混淆器

![测试2](https://raw.githubusercontent.com/Leeyangee/PyLineShell/main/%E6%B5%8B%E8%AF%952.png)

# 鸣谢

在开发的过程中，少不了以下开源/开放代码的支持

* bfengj的Flask内存马代码: https://blog.csdn.net/rfrder/article/details/121005608

* yiqing提供的部分代码  

<div align="center"> <img src="bugctf.png" width = 135 height = 99 /></div>