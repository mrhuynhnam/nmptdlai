import Transaction as tx
import matplotlib.pyplot as plt

class CryptoWallet:
    def __init__(self, walletID, walletName, totalBalance=0, transactionHistory=None, ):
        self.walletID = walletID
        self.walletName = walletName
        self.totalBalance = totalBalance
        self.transactionHistory = []
    def calculateTotalBalance(self):
        total = 0
        for transaction in self.transactionHistory:
            if transaction.recipient == self.walletID:
                total += transaction.amount - transaction.fee
            elif hasattr(transaction, 'sender') and transaction.sender == self.walletID:
                total -= transaction.amount + transaction.fee
        self.totalBalance = total
        return self.totalBalance
    def calculateProfitLoss(self):
        # Giả sử lợi nhuận/lỗ là tổng giá trị nhận - tổng giá trị gửi
        profit = 0
        for t in self.transactionHistory:
            if hasattr(t, 'recipient') and t.recipient == self.walletID:
                profit += t.amount
            if hasattr(t, 'sender') and t.sender == self.walletID:
                profit -= t.amount
        return profit

    def calculateTotalFee(self):
        return sum(getattr(t, 'fee', 0) for t in self.transactionHistory)

    def countTransactions(self):
        return len(self.transactionHistory)

    def sumValue(self):
        buy = sum(t.amount for t in self.transactionHistory if hasattr(t, 'recipient') and t.recipient == self.walletID)
        sell = sum(t.amount for t in self.transactionHistory if hasattr(t, 'sender') and t.sender == self.walletID)
        return buy, sell

    def avgValue(self):
        if not self.transactionHistory:
            return 0
        return sum(getattr(t, 'amount', 0) for t in self.transactionHistory) / len(self.transactionHistory)

    def avgMonthlyTransaction(self):
        # Giả sử mỗi giao dịch có thuộc tính 'month' (bạn cần bổ sung nếu muốn chính xác)
        return round(len(self.transactionHistory) / 12, 2)

    def findMaxTransaction(self):
        if not self.transactionHistory:
            return None
        max_tx = max(self.transactionHistory, key=lambda t: getattr(t, 'amount', 0))
        return f"Mã: {getattr(max_tx, 'transactionID', None)}, Giá trị: {getattr(max_tx, 'amount', None)}"

    def sortTransactions(self, sort_by):
        if sort_by == "value":
            self.transactionHistory.sort(key=lambda t: getattr(t, 'amount', 0), reverse=True)
        # Nếu có thuộc tính 'time', bạn có thể thêm sắp xếp theo thời gian

    def plotProfit(self):
        if not self.transactionHistory:
            print(f"Không có giao dịch nào trong {self.walletName}")
            return
            
        # Tạo dữ liệu cho biểu đồ
        transactions = []
        amounts = []
        colors = []
        
        for i, t in enumerate(self.transactionHistory):
            transactions.append(f"TX{i+1}")
            amounts.append(t.amount)
            # Phân biệt màu theo loại giao dịch
            if t.recipient == self.walletID:  # Nhận tiền (mua/nạp)
                colors.append('green')
            else:  # Gửi tiền (bán/rút)
                colors.append('red')
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(transactions, amounts, color=colors)
        plt.title(f"Giá trị các giao dịch của {self.walletName}")
        plt.xlabel("Giao dịch")
        plt.ylabel("Giá trị (VND)")
        plt.xticks(rotation=45)
        
        # Thêm chú thích
        plt.legend(['Nhận tiền', 'Gửi tiền'], loc='upper right')
        
        # Hiển thị giá trị trên mỗi cột
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()

    def plotAssetDistribution(self):
        # Hiển thị phân bổ tài sản của tất cả các ví
        if not self.transactionHistory:
            print(f"Không có giao dịch nào trong {self.walletName}")
            return
            
        # Tạo dữ liệu cho biểu đồ
        labels = []
        sizes = []
        
        # Thêm ví hiện tại
        if self.totalBalance > 0:
            labels.append(self.walletName)
            sizes.append(self.totalBalance)
        
        # Thêm các loại giao dịch
        transaction_types = {}
        for t in self.transactionHistory:
            ttype = getattr(t, 'transactionType', 'Khác')
            if ttype not in transaction_types:
                transaction_types[ttype] = 0
            transaction_types[ttype] += t.amount
        
        for ttype, amount in transaction_types.items():
            if amount > 0:
                labels.append(f"{ttype}")
                sizes.append(amount)
        
        if not sizes:
            print(f"Không có dữ liệu để vẽ biểu đồ cho {self.walletName}")
            return
            
        plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(f"Phân bổ tài sản của {self.walletName}")
        plt.axis('equal')
        plt.show()

    def plotFeeComparison(self):
        if not self.transactionHistory:
            print(f"Không có giao dịch nào trong {self.walletName}")
            return
            
        # Tạo dữ liệu cho biểu đồ
        transactions = []
        fees = []
        
        for i, t in enumerate(self.transactionHistory):
            transactions.append(f"TX{i+1}")
            fees.append(t.fee)
        
        if not fees or all(f == 0 for f in fees):
            print(f"Không có phí giao dịch để hiển thị cho {self.walletName}")
            return
            
        plt.figure(figsize=(10, 6))
        bars = plt.bar(transactions, fees, color='orange')
        plt.title(f"Phí giao dịch của {self.walletName}")
        plt.xlabel("Giao dịch")
        plt.ylabel("Phí (VND)")
        plt.xticks(rotation=45)
        
        # Hiển thị giá trị phí trên mỗi cột
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()

    def plotTransactionCount(self):
        if not self.transactionHistory:
            print(f"Không có giao dịch nào trong {self.walletName}")
            return
            
        # Đếm số lượng giao dịch theo loại
        types = {"mua": 0, "bán": 0, "nạp": 0, "rút": 0}
        for t in self.transactionHistory:
            ttype = getattr(t, 'transactionType', None)
            if ttype in types:
                types[ttype] += 1
        
        # Chỉ hiển thị các loại có giao dịch
        filtered_types = {k: v for k, v in types.items() if v > 0}
        
        if not filtered_types:
            print(f"Không có loại giao dịch nào để hiển thị cho {self.walletName}")
            return
            
        plt.figure(figsize=(10, 6))
        bars = plt.bar(filtered_types.keys(), filtered_types.values(), color=['green', 'red', 'blue', 'orange'])
        plt.title(f"Số lượng giao dịch theo loại của {self.walletName}")
        plt.xlabel("Loại giao dịch")
        plt.ylabel("Số lượng")
        
        # Hiển thị số lượng trên mỗi cột
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()

    def to_dict(self):
        return {
            "walletID": self.walletID,
            "walletName": self.walletName,
            "totalBalance": self.totalBalance,
            "transactionHistory": [
                {
                    "transactionID": getattr(t, "transactionID", None),
                    "sender": getattr(t, "sender", None),
                    "recipient": getattr(t, "recipient", None),
                    "amount": getattr(t, "amount", None),
                    "fee": getattr(t, "fee", None),
                    "transactionType": getattr(t, "transactionType", None)
                }
                for t in self.transactionHistory
            ]
        }

    def editTransaction(self, transactionID):
        for t in self.transactionHistory:
            if getattr(t, "transactionID", None) == transactionID:
                new_amount = float(input("Nhập giá trị mới: "))
                new_fee = float(input("Nhập phí mới: "))
                t.amount = new_amount
                t.fee = new_fee
                print("Đã sửa giao dịch.")
                return
        print("Không tìm thấy giao dịch.")
    def display(self):
        print(f'Wallet ID: {self.walletID}, Wallet Name: {self.walletName}, Total Balance: {self.totalBalance}')
    def addTransaction(self, transaction):
        if isinstance(transaction, tx.Transaction):
            self.transactionHistory.append(transaction)
        else:
            raise TypeError("The transaction must be an instance of the Transaction class.")
    def removeTransaction(self, transactionID):
        self.transactionHistory = [t for t in self.transactionHistory if t.transactionID != transactionID]