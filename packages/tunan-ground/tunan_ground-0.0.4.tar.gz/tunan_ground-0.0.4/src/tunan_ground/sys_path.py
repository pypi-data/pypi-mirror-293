import os
import sys
import pathlib

"""
这是一个获取系统路径的模块
里面有获取当前操作系统的家路径的方法调用封装。
为什么要分装呢？ 应为自己封装的更加清楚底层用了什么api。
"""


def get_home_dir_2():
    """
    获得当前用户家目录，支持windows，linux和macosx
    更新方法，更加简单
    :return:
    """
    homedir = str(pathlib.Path.home())
    return homedir


def get_home_dir():
    # print(f"当前的系统平台：{sys.platform}")
    if sys.platform == 'win32':
        homedir = os.environ['USERPROFILE']
    elif sys.platform == 'linux' or sys.platform == 'darwin':
        homedir = os.environ['HOME']
    else:
        raise NotImplemented(f'Error! Not this system. {sys.platform}')
    '''
    获得家目录
    :return:
    '''
    return homedir


# print(get_home_dir())
# print(get_home_dir_2())
