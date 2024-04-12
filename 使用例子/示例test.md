
接下来的示例，将会展示如何将一个Python项目转换为一行表达式代码，然后会在一台计算机上使用该一行表达式代码将入口点加载到命名空中并且手动执行

首先，先将PyAnonymous项目克隆到一台能够运行 Python3 的基于 Windows操作系统 的计算机上 (操作系统仅作演示，生成的Payload可跨平台)

1. 笔者接下来要演示打包项目位于PyAnonymous根目录下 "./测试项目/test" 位置的项目(以下简称test项目)

    该项目的入口点为 "./测试项目/test/test_main.py"

    入口点的入口函数为 main

    该项目结构如下所示
   
    ```
    test
        test12
            test4.py
            test6.py
        test34
            test341.py
        test_main.py
        test2.py
        test3.py
        test7.py
        test8.py
    ```

2. 接下来的步骤将test项目打包为一行表达式代码.  
   
    首先了解一下main.py的参数设置:  
    -e --entry 项目入口位置，默认为 "./测试项目/test/test_main.py"  
    -n --namespace 项目入口加载到的命名空间，默认为 math
   
    进入PyAnonymous项目根目录，**-e参数的值为项目入口点**，输入以下指令将会启动对test项目的打包过程  

    ```vb
    python main.py -e "./测试项目/test/test_main.py"
    ```

    接下来，程序在打包时将会出现如下依赖提示  

    ```
    包: test2 为module
        包: test3 为module
            包: os 为官方库不处理
            包: test12 为namespace
                正在分析namespace中包: test4
                正在分析namespace中包: test6
            包: test7 为module
                包: math 为官方库不处理
                包: test12 为namespace
                    正在分析namespace中包: test4
                    正在分析namespace中包: test6
                包: test8 为module
        包: test12 为namespace
            正在分析namespace中包: test4
            正在分析namespace中包: test6
    ```

    最后，将会输出这样一行表达式代码，这是最终Payload. 到此，表示 test项目 打包成功，整个项目成功被打包成了一行表达式代码
    
    ```py
    str(exec(__import__('base64').b64decode('CmRlZiBzdXJmYWNlX1p6UlRTb0RFKG0sIG4pOgogICAgZGVmIGRlZXBfWnpSVFNvREUobW4sIGMsIGQpOgogICAgICAgIGE9X19pbXBvcnRfXygnaW1wJykubmV3X21vZHVsZShtbikKICAgICAgICBmb3IgZDEgaW4gZDoKICAgICAgICAgICAgYS5fX2RpY3RfX1tkMV09ZGVlcF9aelJUU29ERShkMSwgZFtkMV1bMF0sIGRbZDFdWzFdKQogICAgICAgICAgICBfX2ltcG9ydF9fKCdzeXMnKS5tb2R1bGVzW2QxXSA9IGEuX19kaWN0X19bZDFdCiAgICAgICAgZXhlYyhfX2ltcG9ydF9fKCdiYXNlNjQnKS5iNjRkZWNvZGUoYyksIGEuX19kaWN0X18pCiAgICAgICAgcmV0dXJuIGEKICAgIGZvciBpIGluIG06bltpXT1kZWVwX1p6UlRTb0RFKGksIG1baV1bMF0sIG1baV1bMV0pCg==').decode()))+str(surface_ZzRTSoDE(eval(__import__('base64').b64decode('eyd0ZXN0X21haW4nOiBbJ0NtbHRjRzl5ZENCMFpYTjBNZ29LWkdWbUlHMWhhVzRvS1RvS0lDQWdJSEpsZEhWeWJpQjBaWE4wTWk1MFpYTjBNaWdwSUNzZ01Rb0tjSEpwYm5Rb2JXRnBiaWdwS1E9PScsIHsndGVzdDInOiBbJ0kyUmxjQ0IwWlhOME13b0tabkp2YlNCMFpYTjBNVElnYVcxd2IzSjBJSFJsYzNRMkNtWnliMjBnZEdWemRERXlJR2x0Y0c5eWRDQjBaWE4wTkFvS1pHVm1JSFJsYzNReUtDazZDaUFnSUNCeVpYUjFjbTRnWDE5cGJYQnZjblJmWHlnbmRHVnpkRE1uS1M1MFpYTjBNeWdwSUNzZ1gxOXBiWEJ2Y25SZlh5Z25kR1Z6ZERNbktTNTJZWElnS3lCMFpYTjBOaTUwWlhOME5pZ3lLU0FnS3lCMFpYTjBOQzUwWlhOME5DZ3AnLCB7J3Rlc3QzJzogWydDbVp5YjIwZ2RHVnpkRGNnYVcxd2IzSjBJSFJsYzNRM1gyTnNZWE56Q21sdGNHOXlkQ0J2Y3dwbWNtOXRJSFJsYzNReE1pQnBiWEJ2Y25RZ2RHVnpkRFlLQ25aaGNpQTlJRElLQ21SbFppQjBaWE4wTXlncE9nb2dJQ0FnWWlBOUlIUmxjM1EzWDJOc1lYTnpLREVwQ2lBZ0lDQnlaWFIxY200Z01TQXJJR0l1WjJWMFVtVnpLQ2tnS3lCMFpYTjBOaTUwWlhOME5pZ3lLUT09Jywgeyd0ZXN0MTInOiBbJycsIHsndGVzdDQnOiBbJ0NtUmxaaUIwWlhOME5DZ3BPZ29nSUNBZ2NtVjBkWEp1SURRPScsIHt9XSwgJ3Rlc3Q2JzogWydDbVJsWmlCMFpYTjBOaWgyWVhJeEtUb0tJQ0FnSUhKbGRIVnliaUF4TUNBcUlIWmhjakU9Jywge31dfV0sICd0ZXN0Nyc6IFsnQ21sdGNHOXlkQ0J0WVhSb0NtbHRjRzl5ZENCMFpYTjBPQXBtY205dElIUmxjM1F4TWlCcGJYQnZjblFnZEdWemREUUtDbU5zWVhOeklIUmxjM1EzWDJOc1lYTnpLQ2s2Q2lBZ0lDQmtaV1lnWDE5cGJtbDBYMThvYzJWc1ppd2dZU2s2Q2lBZ0lDQWdJQ0FnYzJWc1ppNWhJRDBnWVFvS0lDQWdJR1JsWmlCblpYUlNaWE1vYzJWc1ppazZDaUFnSUNBZ0lDQWdjbVYwZFhKdUlITmxiR1l1WVNBcUlESWdLeUIwWlhOME9DNTBaWE4wT0NncElDc2dkR1Z6ZERRdWRHVnpkRFFvS1E9PScsIHsndGVzdDEyJzogWycnLCB7J3Rlc3Q0JzogWydDbVJsWmlCMFpYTjBOQ2dwT2dvZ0lDQWdjbVYwZFhKdUlEUT0nLCB7fV0sICd0ZXN0Nic6IFsnQ21SbFppQjBaWE4wTmloMllYSXhLVG9LSUNBZ0lISmxkSFZ5YmlBeE1DQXFJSFpoY2pFPScsIHt9XX1dLCAndGVzdDgnOiBbJ0NtUmxaaUIwWlhOME9DZ3BPZ29nSUNBZ2NtVjBkWEp1SURJdycsIHt9XX1dfV0sICd0ZXN0MTInOiBbJycsIHsndGVzdDQnOiBbJ0NtUmxaaUIwWlhOME5DZ3BPZ29nSUNBZ2NtVjBkWEp1SURRPScsIHt9XSwgJ3Rlc3Q2JzogWydDbVJsWmlCMFpYTjBOaWgyWVhJeEtUb0tJQ0FnSUhKbGRIVnliaUF4TUNBcUlIWmhjakU9Jywge31dfV19XX1dfQ==').decode()), __import__("math").__dict__))
    ```

    

3. 在任意一台计算机上的任意一个能任意解析Py代码处(如python交互式shell、exec、eval等)输入最终Payload，该代码将会自动将test项目的入口test_main加载到默认命名空间 math 中

    ```py
    PS C:\> python
    Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> str(exec(__import__('base64').b64decode('CmRlZiBzdXJmYWNlX1p6UlRTb0RFKG0sIG4pOgogICAgZGVmIGRlZXBfWnpSVFNvREUobW4sIGMsIGQpOgogICAgICAgIGE9X19pbXBvcnRfXygnaW1wJykubmV3X21vZHVsZShtbikKICAgICAgICBmb3IgZDEgaW4gZDoKICAgICAgICAgICAgYS5fX2RpY3RfX1tkMV09ZGVlcF9aelJUU29ERShkMSwgZFtkMV1bMF0sIGRbZDFdWzFdKQogICAgICAgICAgICBfX2ltcG9ydF9fKCdzeXMnKS5tb2R1bGVzW2QxXSA9IGEuX19kaWN0X19bZDFdCiAgICAgICAgZXhlYyhfX2ltcG9ydF9fKCdiYXNlNjQnKS5iNjRkZWNvZGUoYyksIGEuX19kaWN0X18pCiAgICAgICAgcmV0dXJuIGEKICAgIGZvciBpIGluIG06bltpXT1kZWVwX1p6UlRTb0RFKGksIG1baV1bMF0sIG1baV1bMV0pCg==').decode()))+str(surface_ZzRTSoDE(eval(__import__('base64').b64decode('eyd0ZXN0X21haW4nOiBbJ0NtbHRjRzl5ZENCMFpYTjBNZ29LWkdWbUlHMWhhVzRvS1RvS0lDQWdJSEpsZEhWeWJpQjBaWE4wTWk1MFpYTjBNaWdwSUNzZ01Rb0tjSEpwYm5Rb2JXRnBiaWdwS1E9PScsIHsndGVzdDInOiBbJ0kyUmxjQ0IwWlhOME13b0tabkp2YlNCMFpYTjBNVElnYVcxd2IzSjBJSFJsYzNRMkNtWnliMjBnZEdWemRERXlJR2x0Y0c5eWRDQjBaWE4wTkFvS1pHVm1JSFJsYzNReUtDazZDaUFnSUNCeVpYUjFjbTRnWDE5cGJYQnZjblJmWHlnbmRHVnpkRE1uS1M1MFpYTjBNeWdwSUNzZ1gxOXBiWEJ2Y25SZlh5Z25kR1Z6ZERNbktTNTJZWElnS3lCMFpYTjBOaTUwWlhOME5pZ3lLU0FnS3lCMFpYTjBOQzUwWlhOME5DZ3AnLCB7J3Rlc3QzJzogWydDbVp5YjIwZ2RHVnpkRGNnYVcxd2IzSjBJSFJsYzNRM1gyTnNZWE56Q21sdGNHOXlkQ0J2Y3dwbWNtOXRJSFJsYzNReE1pQnBiWEJ2Y25RZ2RHVnpkRFlLQ25aaGNpQTlJRElLQ21SbFppQjBaWE4wTXlncE9nb2dJQ0FnWWlBOUlIUmxjM1EzWDJOc1lYTnpLREVwQ2lBZ0lDQnlaWFIxY200Z01TQXJJR0l1WjJWMFVtVnpLQ2tnS3lCMFpYTjBOaTUwWlhOME5pZ3lLUT09Jywgeyd0ZXN0MTInOiBbJycsIHsndGVzdDQnOiBbJ0NtUmxaaUIwWlhOME5DZ3BPZ29nSUNBZ2NtVjBkWEp1SURRPScsIHt9XSwgJ3Rlc3Q2JzogWydDbVJsWmlCMFpYTjBOaWgyWVhJeEtUb0tJQ0FnSUhKbGRIVnliaUF4TUNBcUlIWmhjakU9Jywge31dfV0sICd0ZXN0Nyc6IFsnQ21sdGNHOXlkQ0J0WVhSb0NtbHRjRzl5ZENCMFpYTjBPQXBtY205dElIUmxjM1F4TWlCcGJYQnZjblFnZEdWemREUUtDbU5zWVhOeklIUmxjM1EzWDJOc1lYTnpLQ2s2Q2lBZ0lDQmtaV1lnWDE5cGJtbDBYMThvYzJWc1ppd2dZU2s2Q2lBZ0lDQWdJQ0FnYzJWc1ppNWhJRDBnWVFvS0lDQWdJR1JsWmlCblpYUlNaWE1vYzJWc1ppazZDaUFnSUNBZ0lDQWdjbVYwZFhKdUlITmxiR1l1WVNBcUlESWdLeUIwWlhOME9DNTBaWE4wT0NncElDc2dkR1Z6ZERRdWRHVnpkRFFvS1E9PScsIHsndGVzdDEyJzogWycnLCB7J3Rlc3Q0JzogWydDbVJsWmlCMFpYTjBOQ2dwT2dvZ0lDQWdjbVYwZFhKdUlEUT0nLCB7fV0sICd0ZXN0Nic6IFsnQ21SbFppQjBaWE4wTmloMllYSXhLVG9LSUNBZ0lISmxkSFZ5YmlBeE1DQXFJSFpoY2pFPScsIHt9XX1dLCAndGVzdDgnOiBbJ0NtUmxaaUIwWlhOME9DZ3BPZ29nSUNBZ2NtVjBkWEp1SURJdycsIHt9XX1dfV0sICd0ZXN0MTInOiBbJycsIHsndGVzdDQnOiBbJ0NtUmxaaUIwWlhOME5DZ3BPZ29nSUNBZ2NtVjBkWEp1SURRPScsIHt9XSwgJ3Rlc3Q2JzogWydDbVJsWmlCMFpYTjBOaWgyWVhJeEtUb0tJQ0FnSUhKbGRIVnliaUF4TUNBcUlIWmhjakU9Jywge31dfV19XX1dfQ==').decode()), __import__("math").__dict__))
    __main__:4: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
    'NoneNone'
    >>>
    ```

4. 最后验证是否成功导入. 先导入math包(因为笔者选择的命名空间是math)，输入以下代码调用入口点下的入口函数main.  
    ```py
    >>> import math
    >>> math.test_main.main()
    75
    ```
    成功输出75，证明test项目入口连同整个项目被成功加载至math命名空间中