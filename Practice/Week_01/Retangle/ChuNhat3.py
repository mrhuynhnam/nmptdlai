# Lưu trữ danh sách các hình chữ nhật từ file input.db
# Lưu danh sách các hình chữ nhật xuống file output.db theo định dạng
# rong-dai-chuvi-dientich
# Lưu ý: Trong các file mỗi hàng là thông tin một hình chữ nhật
import Rectangle as rect
# Tải dữ liệu từ file vào listRectangle
fr = open('input.db',mode='r',encoding='utf-8')
listRectangle = []
for line in fr:
    stripLine = line.strip('\n')
    ds = stripLine.split(',')
    cr = float(ds[0])
    cd = float(ds[1]) 
    cn = rect.Rectangle(cr,cd)
    listRectangle.append(hcn)
fr.close()
# Ghi dữ liệu từ listRectangle xuống file
fw = open('output.db',mode='w',encoding='utf-8')
for item in listRectangle:
    fw.write(f'{item.width}-{item.length}-{item.perimeter()}-{item.area()}\n')
fw.close()
'''
(*) Sinh viên tự thực hành
Viết chương trình menu
1- Đọc dữ liệu từ file input.db
2- Thêm mới hình chữ nhật
3- Hiển thị danh sách hình chữ nhật
4- Lưu danh sách hình chữ nhật xuống file demo4output.db
Others- Thoát
'''
import Rectangle as rect
menu ={
1:'1- Đọc dữ liệu từ file input.db'   ,
2:'2- Thêm mới hình chữ nhật',
3:'3- Hiển thị danh sách hình chữ nhật',
4:'4- Lưu danh sách hình chữ nhật xuống file demo4output.db',
'Others':'Thoát'
}
def print_menu():
    for key in menu.keys():
        print (key,'--',menu[key])
#Khai báo biến lưu trữ hình chữ nhật
while(True):
    print_menu()
    chon=''
    try:
        chon =int(input('Nhập tùy chọn:'))
    except:
        print('Nhập sai định dạng, hãy nhập lại:')
        continue
    #Kiểm tra các lựa chọn
    if chon ==1:
    #1- Đọc dữ liệu từ file input.db
        fr=open('input.db', mode='r',encoding ='utf-8') 
        dsHCN =[]
        for line in fr:
            stripLine = line.strip('\n')
        ds =stripLine.split(',')
        cr =float(ds[0])
        cd =float(ds[1])
        hcn=rect.Rectangle(cr,cd)
        dsHCN.append(hcn)
        fr.close()
    elif chon ==2:
    # 2- Thêm mới hình chữ nhật
        cr =float(input("Nhập chiều rộng:"))
        cd =float(input("Nhập chiều dài:"))
        hcn =rect.Rectangle(cr,cd)
        dsHCN.append(hcn)
    elif chon ==3:
    #3- Hiển thị danh sách hình chữ nhật
        if dsHCN.count ==0:
            print('Danh sách rỗng')
        else:
            for item in dsHCN:
                item.display()
    elif chon ==4:
    #4- Lưu danh sách hình chữ nhật xuống file demo4output.db
        fw =open('outpudemo4.db',mode='w',encoding ='utf-8')
        for item in dsHCN:
            fw.write(f'{item.width}-{item.length}-{item.perimeter()}-{item.area()}\n)')
        fw.close() 
    else:
        print('Kết thúc chương trình') 
    break