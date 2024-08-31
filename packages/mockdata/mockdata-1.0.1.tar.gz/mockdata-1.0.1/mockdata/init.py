# 创建基类common，实例化faker
from faker import Faker


class Common:

    def __init__(self):
        self.fake_en = Faker()
        self.fake_cn = Faker("zh_CN")

    def get_fake(self, lan=True):  # 默认中文
        if lan:
            return self.fake_cn
        return self.fake_en


import subprocess


def check_debugtalk_code(path='.'):
    """
    运行flake8并获取输出，筛选包含字符'F'的错误行。

    :param path: 要检测的代码路径，默认为当前目录。
    :return: 返回第一条包含字符'F'的错误行，如果没有则返回None。
    """
    # 运行flake8并获取输出
    result = subprocess.run(['flake8', path], stdout=subprocess.PIPE, text=True)
    output = result.stdout
    # 使用字符串方法str.split和列表推导式筛选包含'F'的行
    errors_with_f = [line for line in output.splitlines() if 'F' in line]
    # 返回第一条结果
    for error in errors_with_f:
        print(error)

