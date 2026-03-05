import gradio as gr
from accounts import Account

account = Account(initial_deposit=1000.0)

def create_account(initial_deposit):
    global account
    account = Account(initial_deposit)

def deposit(amount):
    account.deposit_funds(amount)
    return f"Deposited ${amount}. Current balance: ${account.balance}"

def withdraw(amount):
    try:
        account.withdraw_funds(amount)
        return f"Withdrew ${amount}. Current balance: ${account.balance}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. Current balance: ${account.balance}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. Current balance: ${account.balance}"
    except ValueError as e:
        return str(e)

def report_holdings():
    return account.report_holdings()

def report_profit_loss():
    return account.calculate_profit_loss()

def list_transactions():
    return account.report_transactions()

with gr.Blocks() as app:
    gr.Markdown("## Simple Trading Account Management System")
    
    with gr.Tab("Account Operations"):
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit")
        deposit_button.click(deposit, inputs=deposit_amount, outputs="output")
        withdraw_amount = gr.Number(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw")
        withdraw_button.click(withdraw, inputs=withdraw_amount, outputs="output")
    
    with gr.Tab("Trading Operations"):
        buy_symbol = gr.Textbox(label="Symbol (AAPL, TSLA, GOOGL)")
        buy_quantity = gr.Number(label="Quantity")
        buy_button = gr.Button("Buy Shares")
        buy_button.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs="output")
        
        sell_symbol = gr.Textbox(label="Symbol (AAPL, TSLA, GOOGL)")
        sell_quantity = gr.Number(label="Quantity")
        sell_button = gr.Button("Sell Shares")
        sell_button.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs="output")
    
    with gr.Tab("Reports"):
        holdings_button = gr.Button("Report Holdings")
        holdings_output = gr.Textbox()
        holdings_button.click(report_holdings, outputs=holdings_output)
        
        profit_loss_button = gr.Button("Calculate Profit/Loss")
        profit_loss_output = gr.Textbox()
        profit_loss_button.click(report_profit_loss, outputs=profit_loss_output)
        
        transactions_button = gr.Button("List Transactions")
        transactions_output = gr.Textbox()
        transactions_button.click(list_transactions, outputs=transactions_output)
    
    output = gr.Textbox(label="Output")

app.launch()