import os
import sys
os.chdir('./test')
print(sys.path)
print(__import__('test2'))