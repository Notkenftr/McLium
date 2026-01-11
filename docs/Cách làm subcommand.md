# Cách làm sub command
## Tạo module 
Để tạo 1 subcommand. Cần vào folder ``./modules`` và tạo tên module bạn muốn
sau đó trong folder module tạo 1 file để làm entry point của module.
Vd ở đây tôi sẽ tạo ``command.py`` thì cấu trúc sẽ như sau 
```
modules/
    ├ example/
        ├ command.py   <- xác định này là entry point 
    ├ ... các module khác
```
## Tạo command 
Truy cập vào ``command.py`` và import api sau 
```python
from McLiumSDK import Flag
from McLiumSDK import McLiumCommand
```
### Tạo Flag
Flag là gì. Kiểu khi nhập như sau 
``McLium Subcommand --example value``
thì --example sẽ là flag
```python
from McLiumSDK import Flag

Flags = [
    Flag(
        short='-e',         # short là lệnh ngắn thay vì nhập -example thì giờ có thể nhập -e 
        long='--example',   # Đây là lệnh dài 
        required=False,     # Cái này có buộc phải có trong subcommand hay ko  
        type=str,           # Kiểu dữ liệu của flag ví dụ int thì chỉ được đưa vào int 
        help="Lệnh mẫu",    # dùng để gợi ý khi nhập -h / --help,
        default=None,       # Giá trị mặc định nếu user không nhập
        action="store"      # Hành động khi flag được gọi: "store" lưu giá trị, "store_true" cho bool, ...  
    ),
    Flag(...) # Các flag khác,
]
```
### Thiết lập subcommand
```python 
from McLiumSDK import McLiumCommand

Flags = [] #như trên 

sub = McLiumCommand(
    name="example", #Tạo subcommand tên example 
    *Flags # Truyền vào Flag, nếu không có flag thì để None hoặc list rỗng 
)

@sub.setCallback    # Khi người dùng nhập flag thì hàm bên dưới decorator setCallback sẽ được call tự động 
def callback(args): # Lưu ý phải có 1 tham số ở đây. Sẽ nói lý do ở dưới 
    ...
```

### Cách lấy dữ liệu từ flag
```python 
from McLiumSDK import McLiumCommand

sub = McLiumCommand(
    name="example", 
    *None 
)

@sub.setCallback    
def callback(args): 
    # Ví dụ trong flags có 1 flag tên --example thì để lấy value của nó ta làm như sau 
    example_value = args.example # sử dụng args.{tên flag} để lấy giá trị

```

ví dụ:<br>
ta sài: ``McLium Subcommand -e abc``
thì ``example_value`` trong callback sẽ mang value là ``abc`` 





