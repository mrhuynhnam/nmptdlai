class Transaction:
    def __init__(self, sender, recipient, amount):
        self.transactionID = None  # This will be set when the transaction is added to the wallet
        self.sender = sender # Sender is the wallet ID of the sender
        self.recipient = recipient # Recipient is the wallet ID of the recipient
        self.amount = amount # Amount of the transaction
        self.fee = 0.01 * amount  # Assuming a fixed fee of 1% of the transaction amount
        self.transactionType = None  # Type of transaction (mua/bán/nạp/rút)
    
    def display(self):
        print(f'Transaction ID: {self.transactionID}, Sender: {self.sender}, Recipient: {self.recipient}, Amount: {self.amount}, Fee: {self.fee}, Type: {self.transactionType}')