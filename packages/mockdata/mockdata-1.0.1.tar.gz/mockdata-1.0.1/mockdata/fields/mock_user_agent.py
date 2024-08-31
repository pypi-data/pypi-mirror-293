from mockdata.init import Common


class MockUserAgent(Common):

    def __init__(self):
        super().__init__()
        self.fake = self.get_fake()

    def mock_android_platform_token(self):
        """android platform token"""
        return self.fake.android_platform_token()

    def mock_ios_platform_token(self):
        """ios platform token"""
        return self.fake.ios_platform_token()

    def mock_chrome(self):
        """chrome user agent"""
        return self.fake.chrome()

    def mock_firefox(self):
        """firefox user agent"""
        return self.fake.firefox()

    def mock_internet_explorer(self):
        """internet explorer user agent"""
        return self.fake.internet_explorer()

    def mock_linux_platform_token(self):
        """linux platform token"""
        return self.fake.linux_platform_token()

    def mock_user_agent(self):
        """user agent"""
        return self.fake.user_agent()

if __name__ == '__main__':
    print(MockUserAgent().mock_user_agent())

