# 创建基类common，实例化faker
from faker import Faker


class Common:

    def __init__(self):
        self.fake_en = Faker()
        self.fake_cn = Faker("zh_CN")

    def get_fake(self, lan=True):  # 默认中文
        if lan:
            return self.fake_cn
        else:
            return self.fake_en
