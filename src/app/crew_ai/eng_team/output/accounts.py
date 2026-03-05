class Account:
    def __init__(self, initial_deposit: float) -> None:
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit_funds(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount, 'timestamp': self._current_timestamp()})

    def withdraw_funds(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("Withdrawal would cause negative balance.")
        self.balance -= amount
        self.transactions.append({'type': 'withdrawal', 'amount': amount, 'timestamp': self._current_timestamp()})

    def buy_shares(self, symbol: str, quantity: int) -> None:
        total_cost = self.get_share_price(symbol) * quantity
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")
        
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'price': self.get_share_price(symbol), 'timestamp': self._current_timestamp()})

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Insufficient shares to sell.")
        
        total_sale_value = self.get_share_price(symbol) * quantity
        self.balance += total_sale_value
        self.holdings[symbol] -= quantity
        
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity, 'price': self.get_share_price(symbol), 'timestamp': self._current_timestamp()})

    def calculate_portfolio_value(self) -> float:
        total_value = 0.0
        for symbol, quantity in self.holdings.items():
            total_value += self.get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        current_value = self.calculate_portfolio_value()
        return current_value - self.initial_deposit

    def report_holdings(self) -> dict:
        return self.holdings

    def report_transactions(self) -> list:
        return self.transactions

    @staticmethod
    def get_share_price(symbol: str) -> float:
        market_prices = {
            'AAPL': 150.0,
            'TSLA': 720.0,
            'GOOGL': 2800.0
        }
        return market_prices.get(symbol, 0.0)

    @staticmethod
    def _current_timestamp() -> str:
        from datetime import datetime
        return datetime.now().isoformat()