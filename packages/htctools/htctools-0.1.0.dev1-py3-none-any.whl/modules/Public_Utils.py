import os

# 获取terminal当前路径
def get_terminal_directory():
    return os.getcwd()

# 获取程序的路径
def get_program_directory():
    # 首先获取当前脚本的绝对路径
    current_directory = os.path.abspath(__file__)
    # 然后获取这个路径的目录部分
    program_directory = os.path.dirname(current_directory)
    # 最后，再次使用 dirname 获取上一级目录
    parent_directory = os.path.dirname(program_directory)
    return parent_directory