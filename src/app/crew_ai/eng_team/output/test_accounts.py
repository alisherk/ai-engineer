import unittest
from accounts import Account

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account(initial_deposit=1000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit_funds(self):
        self.account.deposit_funds(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 1)

    def test_withdraw_funds(self):
        self.account.withdraw_funds(200.0)
        self.assertEqual(self.account.balance, 800.0)

    def test_withdraw_funds_insufficient(self):
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(2000.0)

    def test_buy_shares(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.holdings['AAPL'], 2)
        self.assertEqual(self.account.balance, 700.0)

    def test_buy_shares_insufficient_funds(self):
        self.account.balance = 100.0
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 1)

    def test_sell_shares(self):
        self.account.buy_shares('AAPL', 2)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.holdings['AAPL'], 1)
        self.assertEqual(self.account.balance, 850.0)

    def test_sell_shares_insufficient(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 1)

    def test_calculate_portfolio_value(self):
        self.account.buy_shares('AAPL', 2)
        self.account.buy_shares('TSLA', 1)
        self.assertAlmostEqual(self.account.calculate_portfolio_value(), 150.0 * 2 + 720.0)

    def test_calculate_profit_loss(self):
        self.account.deposit_funds(500.0)
        self.account.buy_shares('AAPL', 2)
        self.assertAlmostEqual(self.account.calculate_profit_loss(), (150.0 * 2) - 500.0)

    def test_report_holdings(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.report_holdings(), {'AAPL': 2})

    def test_report_transactions(self):
        self.account.deposit_funds(500.0)
        self.assertEqual(len(self.account.report_transactions()), 1)

if __name__ == '__main__':
    unittest.main()