# Cài đặt lớp hình chữ nhật theo thiết kế
# Có 2 fields (thuộc tính): width, length
# Có các phương thức: 
# - tính diện tích (area)
# - tính chu vi (perimeter)
# - hiện thị cơ bản (display)
# Phạm vi khai báo class Rectangle được tính từ phím tab sau class Rectangle
# '''
class Rectangle:
# '''
# Hàm (method) khởi tạo (constructor)
# Đây là method (phương thức) đặc biệt phải có khi khai báo class
# Mục đích: Để nạp những giá trị ban đầu cho các thể hiện (cụ thể)
# của đối tượng khi chạy chương trình
# '''
    def __init__(self,width,length):
        self.width = width
        self.length = length
    def area(self):
        result = self.width * self.length
        return result
    def perimeter(self):
        result = 2*(self.width + self.length)
        return result
    def display(self):
        print(f'rộng: {self.width}, dài: {self.length}, chu vi: {self.perimeter():.2f}, diện tích: {self.area():.2f}\n')