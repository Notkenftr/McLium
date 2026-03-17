# file research by @kenftr

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
        num |= (data & 0x7F) << shift

        if not (data & 0x80): # 0x80 dùng để check xem còn byte ko
            # ví dụ
            # 10000000 & 10000000 = 128 -> còn byte vì nếu = 0 thì mới đó là byte cuối ^^
            _e_0x80mul10000000()
            #return num, offset # return nếu trong func
            break

        shift += 7 # vì sao lại là += 7? vì 1 byte = 8 bit
                   # nhưng VarInt chỉ dùng 7 bit để chứa value
                   # bit còn lại dùng làm flag (0x80)

