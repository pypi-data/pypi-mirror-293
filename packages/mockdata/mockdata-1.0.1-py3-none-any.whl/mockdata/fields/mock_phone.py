from mockdata.init import Common


class MockPhone(Common):

    def __init__(self):
        super().__init__()
        self.fake = self.get_fake()

    def mock_country_calling_code(self):
        """国家呼叫代码"""
        return self.fake.country_calling_code()

    def mock_msisdn(self):
        """摩斯登密码"""
        return self.fake.msisdn()

    def mock_phone_number(self):
        """电话号码"""
        return self.fake.phone_number()

if __name__ == '__main__':
    mock_phone = MockPhone()
    print(mock_phone.mock_phone_number())

