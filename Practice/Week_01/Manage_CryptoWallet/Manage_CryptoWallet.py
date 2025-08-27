'''
Ứng Dụng Quản Lý Ví Tiền Ảo
Khai Báo Đối Tượng CryptoWallet (Ví tiền ảo)

Các thuộc tính (fields, states) sau:

- Mã ví (walletID): Mã định danh duy nhất của ví.

- Tên ví (walletName): Tên do người dùng đặt (ví dụ: "Ví BTC chính").

- Tổng số dư (totalBalance): Tổng giá trị hiện tại của ví, tính bằng USD hoặc VND.

- Lịch sử giao dịch (transactionHistory): Một danh sách (list) các đối tượng Transaction để lưu trữ tất cả các giao dịch.

Các phương thức (behaviors, methods):

- Tính tổng giá trị hiện tại (calculateTotalBalance): Tính tổng giá trị của tất cả các tài sản trong ví dựa trên giá thị trường hiện tại.

- In thông tin của ví (display): In ra mã ví, tên ví và tổng số dư hiện tại.

- Thêm giao dịch (addTransaction): Thêm một giao dịch mới vào transactionHistory.

- Xóa giao dịch (removeTransaction): Xóa một giao dịch khỏi lịch sử dựa trên mã giao dịch.

Yêu Cầu Chương Trình Chính:

    Khai báo biến đối tượng CryptoWallet để lưu trữ tất cả thông tin và viết chương trình menu thực hiện các chức năng bên dưới.

    Opt-1: Tải dữ liệu từ file: Tải thông tin ví và lịch sử giao dịch từ file my_wallet.json.

    Opt-2: Thêm một giao dịch mới: Ghi lại một giao dịch (mua, bán, nạp, rút) và thêm vào ví.

    Opt-3: Hiển thị lịch sử giao dịch: Liệt kê tất cả các giao dịch đã được ghi lại.

    Opt-4: Hiển thị thông tin ví: Hiển thị tổng số dư và tên ví.

    Opt-5: Sửa giao dịch: Chỉnh sửa thông tin một giao dịch (ví dụ: số lượng, phí).

    Opt-6: Xóa một giao dịch: Xóa một giao dịch khỏi lịch sử.

    Opt-7: Tính tổng lợi nhuận/lỗ: Tính tổng lợi nhuận hoặc lỗ của toàn bộ ví dựa trên giá mua và giá hiện tại.

    Opt-8: Tính tổng phí giao dịch: Tính tổng số tiền phí đã chi trả cho tất cả các giao dịch.

    Opt-9: Tính số lượng giao dịch (countTransactions): Đếm và hiển thị tổng số giao dịch đã thực hiện.

    Opt-10: Tính tổng giá trị mua/bán (sumValue): Tính tổng giá trị đã mua và tổng giá trị đã bán trong ví.

    Opt-11: Tính giá trị trung bình mỗi giao dịch (avgValue): Tính giá trị trung bình của các giao dịch.

    Opt-12: Tính số lượng giao dịch trung bình mỗi tháng (avgMonthlyTransaction): Tính trung bình số giao dịch thực hiện mỗi tháng.

    Opt-13: Tìm giao dịch có giá trị cao nhất: Tìm và hiển thị giao dịch có giá trị lớn nhất.

    Opt-14: Sắp xếp giao dịch: Sắp xếp danh sách giao dịch theo thời gian hoặc giá trị.

    Opt-15: Vẽ biểu đồ lợi nhuận: Biểu diễn sự thay đổi lợi nhuận của ví theo thời gian.

    Opt-16: Vẽ biểu đồ phân bổ tài sản: Biểu đồ tròn thể hiện phần trăm của mỗi loại tiền ảo trong tổng giá trị ví.

    Opt-17: Vẽ biểu đồ so sánh phí: Biểu đồ cột so sánh tổng phí đã trả cho các loại tiền ảo khác nhau.

    Opt-18: Vẽ biểu đồ số lượng giao dịch: Biểu đồ thể hiện số lượng giao dịch đã thực hiện theo từng loại (mua, bán, nạp, rút).

    Opt-19: Lưu dữ liệu xuống file: Lưu thông tin ví và lịch sử giao dịch vào file my_wallet.json.

    Opt-Khác: Thoát chương trình.
'''
import matplotlib.pyplot as plt
import CryptoWallet as w
import Transaction as tx
menu_options = {
    1: "Tải dữ liệu từ file",
    2: "Thêm một giao dịch mới",
    3: "Hiển thị lịch sử giao dịch",
    4: "Hiển thị thông tin ví",
    5: "Sửa giao dịch",
    6: "Xóa một giao dịch",
    7: "Tính tổng lợi nhuận/lỗ",
    8: "Tính tổng phí giao dịch",
    9: "Tính số lượng giao dịch",
    10: "Tính tổng giá trị mua/bán",
    11: "Tính giá trị trung bình mỗi giao dịch",
    12: "Tính số lượng giao dịch trung bình mỗi tháng",
    13: "Tìm giao dịch có giá trị cao nhất",
    14: "Sắp xếp giao dịch",
    15: "Vẽ biểu đồ lợi nhuận",
    16: "Vẽ biểu đồ phân bổ tài sản",
    17: "Vẽ biểu đồ so sánh phí",
    18: "Vẽ biểu đồ số lượng giao dịch",
    19: "Lưu dữ liệu xuống file",
    0: "Thoát chương trình"
}
def display_menu():
    print("\nMenu:")
    for key in menu_options:
        print(f"{key}: {menu_options[key]}")
list_wallet = []
while True:
    display_menu()
    choice = int(input("Chọn một tùy chọn: "))
    if choice == 0:
        print("Thoát chương trình.")
        break
    elif choice == 1:
        # Tải dữ liệu từ file
        try:
            with open('my_wallet.json', 'r') as file:
                import json
                data = json.load(file)
                for wallet_data in data:
                    wallet = w.CryptoWallet(wallet_data['walletID'], wallet_data['walletName'], wallet_data['totalBalance'])
                    # Chuyển đổi transaction từ dict thành Transaction object
                    for tx_data in wallet_data['transactionHistory']:
                        transaction = tx.Transaction(tx_data['sender'], tx_data['recipient'], tx_data['amount'])
                        transaction.transactionID = tx_data['transactionID']
                        transaction.fee = tx_data['fee']
                        transaction.transactionType = tx_data['transactionType']
                        wallet.addTransaction(transaction)
                    list_wallet.append(wallet)
                print("Dữ liệu đã được tải thành công.")
        except FileNotFoundError:
            print("File không tồn tại. Vui lòng kiểm tra lại.")
    elif choice == 2:
        # Thêm một giao dịch mới
        walletID = input("Nhập mã ví: ")
        walletName = input("Nhập tên ví: ")
        totalBalance = float(input("Nhập tổng số dư: "))
        wallet = w.CryptoWallet(walletID, walletName, totalBalance)
        transactionID = input("Nhập mã giao dịch: ")
        transactionType = input("Nhập loại giao dịch (mua/bán/nạp/rút): ")
        value = float(input("Nhập giá trị giao dịch: "))
        fee = float(input("Nhập phí giao dịch: "))
        # Giả sử nạp/rút là từ hệ thống, mua/bán là giữa các ví
        if transactionType == "nạp":
            sender = "system"
            recipient = walletID
        elif transactionType == "rút":
            sender = walletID
            recipient = "system"
        elif transactionType == "mua":
            sender = "market"
            recipient = walletID
        elif transactionType == "bán":
            sender = walletID
            recipient = "market"
        else:
            sender = ""
            recipient = ""
        transaction = tx.Transaction(sender, recipient, value)
        transaction.transactionID = transactionID
        transaction.fee = fee
        transaction.transactionType = transactionType
        wallet.addTransaction(transaction)
        list_wallet.append(wallet)
        print("Giao dịch mới đã được thêm thành công.")
    elif choice == 3:
        # Hiển thị lịch sử giao dịch
        for w in list_wallet:
            print(f"Lịch sử giao dịch của {w.walletName}:")
            if w.transactionHistory:
                for transaction in w.transactionHistory:
                    # Nếu transaction là dict (từ file), chuyển thành Transaction object
                    if isinstance(transaction, dict):
                        print(f"  - Mã giao dịch: {transaction.get('transactionID')}, Loại: {transaction.get('transactionType')}, Giá trị: {transaction.get('amount')}, Phí: {transaction.get('fee')}")
                    else:
                        print(f"  - Mã giao dịch: {getattr(transaction, 'transactionID', None)}, Loại: {getattr(transaction, 'transactionType', None)}, Giá trị: {getattr(transaction, 'amount', None)}, Phí: {getattr(transaction, 'fee', None)}")
            else:
                print("  Không có giao dịch nào.")
    elif choice == 4:
        # Hiển thị thông tin ví
        for w in list_wallet:
            w.display()
    elif choice == 5:
        # Sửa giao dịch
        transaction_id = input("Nhập mã giao dịch cần sửa: ")
        for w in list_wallet:
            w.editTransaction(transaction_id)
    elif choice == 6:
        # Xóa một giao dịch
        transaction_id = input("Nhập mã giao dịch cần xóa: ")
        for w in list_wallet:
            w.removeTransaction(transaction_id)
    elif choice == 7:
        # Tính tổng lợi nhuận/lỗ
        for w in list_wallet:
            print(f"Lợi nhuận/lỗ của {w.walletName}: {w.calculateProfitLoss()}")
    elif choice == 8:
        # Tính tổng phí giao dịch
        for w in list_wallet:
            print(f"Tổng phí giao dịch của {w.walletName}: {w.calculateTotalFee()}")
    elif choice == 9:
        # Tính số lượng giao dịch
        for w in list_wallet:
            print(f"Số lượng giao dịch của {w.walletName}: {w.countTransactions()}")
    elif choice == 10:
        # Tính tổng giá trị mua/bán
        for w in list_wallet:
            buy, sell = w.sumValue()
            print(f"{w.walletName}: Tổng mua: {buy}, Tổng bán: {sell}")
    elif choice == 11:
        # Tính giá trị trung bình mỗi giao dịch
        for w in list_wallet:
            print(f"Giá trị trung bình mỗi giao dịch của {w.walletName}: {w.avgValue()}")
    elif choice == 12:
        # Tính số lượng giao dịch trung bình mỗi tháng
        for w in list_wallet:
            print(f"Số lượng giao dịch trung bình mỗi tháng của {w.walletName}: {w.avgMonthlyTransaction()}")
    elif choice == 13:
        # Tìm giao dịch có giá trị cao nhất
        for w in list_wallet:
            tx = w.findMaxTransaction()
            print(f"Giao dịch lớn nhất của {w.walletName}: {tx}")
    elif choice == 14:
        # Sắp xếp giao dịch
        sort_by = input("Sắp xếp theo (time/value): ")
        for w in list_wallet:
            w.sortTransactions(sort_by)
            print(f"Đã sắp xếp giao dịch cho {w.walletName}.")
    elif choice == 15:
        # Vẽ biểu đồ lợi nhuận
        for w in list_wallet:
            w.plotProfit()
    elif choice == 16:
        # Vẽ biểu đồ phân bổ tài sản
        for w in list_wallet:
            w.plotAssetDistribution()
    elif choice == 17:
        # Vẽ biểu đồ so sánh phí
        for w in list_wallet:
            w.plotFeeComparison()
    elif choice == 18:
        # Vẽ biểu đồ số lượng giao dịch
        for w in list_wallet:
            w.plotTransactionCount()
    elif choice == 19:
        # Lưu dữ liệu xuống file
        import json
        for w in list_wallet:
            data = w.to_dict()
            with open('my_wallet.json', 'w') as file:
                json.dump(data, file)
        print("Dữ liệu đã được lưu thành công.")
    else:
        print("Tùy chọn không hợp lệ. Vui lòng thử lại.")