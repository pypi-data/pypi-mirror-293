import json
import random

from mockdata.init import Common


class MockCreditCard(Common):
    def __init__(self):
        super().__init__()
        self.fake = self.get_fake()

    def mock_credit_card_expire(self):
        """生成信用卡到期日期"""
        return self.fake.credit_card_expire()

    def mock_credit_card_full(self):
        """生成信用卡详细信息"""
        return self.fake.credit_card_full()

    def mock_credit_card_number(self):
        """生成信用卡卡号"""
        return self.fake.credit_card_number()

    @staticmethod
    def mock_credit_card_provider():
        """生成信用卡提供者"""
        banks = open('../bank.json', 'r', encoding='utf-8').read()
        banks_list = json.loads(banks)['bank']
        return random.choice(banks_list)

    def mock_credit_card_security_code(self):
        """生成信用卡安全码"""
        return self.fake.credit_card_security_code()



