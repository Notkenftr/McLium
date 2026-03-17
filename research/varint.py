# file research by @kenftr

#read varint

# công thức varint
# num = Σ ( (byte_i & 0x7F) << (7 * i) )
# | Thành phần | Ý nghĩa               |
# | ---------- | --------------------- |
# | byte_i   | byte thứ i            |
# | & 0x7F   | lấy 7 bit data        |
# | << (7*i) | dịch trái theo vị trí |
# | Σ        | cộng tất cả lại       |

def _e_0x80mul10000000():
    print(0x80 & 0b10000000)

# First
# varint là số nguyên có độ dài thay đổi.
# nếu bit 7 (tức bit đầu) là 1 thì đó chưa phải byte cuối
# nếu bit 7 (tức bit đầu) là 0 thì đó là byte cuối
# ví dụ
# 10000000 : bit đầu là 1 -> byte này chưa phải byte cuối
# 00000100 : bit đầu là 0 -> byte đó là byte cuối

# lưu ý
# 0x80 = 10000000 ( dùng để check xem đó có phải byte cuối chưa vì ?byte & 0x80 nếu bit đầu lầ 1 thì nó sẽ ra 128)

if __name__ == '__main__':
    byte_array = b'\x03\x03\x80\x02'

    num = 0
    shift = 0
    offset = 0
    for i in range(5):
        data = byte_array[offset]
        offset += 1 # vì sao lại +1 vì chúng ta dựa vào offset để đi qua byte_array nên cần +1 để đến byte tiếp theo

        # để hiểu dòng này chúng ta cần hiểu được byte shift là gì
        # có 2 loại shift chính:
        # shift trái: x << y
        # shift phải: x >> y
        # ví dụ
        # 5 << 1
        # 5 = 00000101
        # thì khi shift trái 1 sẽ dịch 00000101 sang 1 bit tức là 00001010
        # truwc quan
        # 00000101
        # 00001010 nnó đã dịch sang 1 ô

        # |=  nghĩa là or rồi gán lại
        # | A | B | A OR B  |
        # | 0 | 0 | 0       |
        # | 0 | 1 | 1       |
        # | 1 | 0 | 1       |
        # | 1 | 1 | 1       |
        # VÍ DỤ
        # A = 00000010
        # B = 00000010
        # A |= B -> 00000010

        # A = 00000011
        # B = 00000001
        # A |= B -> 00000011 # vì 1 | 0 = 1

        num |= (data & 0x7F) << shift
        #

        if not (data & 0x80): # 0x80 dùng để check xem còn byte ko
            # ví dụ
            # 10000000 & 10000000 = 128 -> còn byte vì nếu = 0 thì mới đó là byte cuối ^^
            _e_0x80mul10000000()
            #return num, offset # return nếu trong func
            break

        shift += 7 # vì sao lại là += 7? vì 1 byte = 8 bit
                   # nhưng VarInt chỉ dùng 7 bit để chứa value
                   # bit còn lại dùng làm flag (0x80)

# encode varint

# encode ngược lại với read
# read: ghép từng byte -> số
# encode: tách số -> từng byte

# công thức
# byte_i = ((value >> (7 * i)) & 0x7F) | (0x80 nếu còn byte sau, ngược lại 0)

if __name__ == '__main__':
    value = 2 # value example
    result = bytearray()
    while True:
        byte = value & 0x7F
        # vì sao lại là 0x7F?
        # 0x7F = 01111111
        # tức là giữ 7 bit sau bỏ bit đầu
        # ví dụ
        # 10000000 & 0xF7 ( 0x7F = 01111111 )
        # -> 00000000 # đã bỏ flag đầu thay bằng 0

        value >>= 7 # dịch value sang phải 7 bit ( bỏ 7 bit vừa lấy ra từ value & 0x7F)
        # ví dụ về shift phải
        # 5 = 00000101
        # dịch phải 1 bit
        # 00000101  →  00000010
        # dịch phải 7 bit
        # 00000101 -> 00000000

        if value != 0: # nếu value chx hết
            value |= 0x80 # như đã nói ở varint cái này sẽ giúp ktra xem bit còn k
        result.append(byte)

        if value == 0:
            break # end
    # return bytes(result)
    print(bytes(result))























