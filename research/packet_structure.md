# Lưu ý trước khi đọc 
1. Cần hiểu rõ varint 

# minecraft có 2 loại packet
1. packet nén 
2. packet ko nén 

## Đầu tiên cta sẽ nói đến ko nén (cái dễ nhất )
thì cấu trúc của nó như sau 
``` 
[VarInt Length][VarInt PacketID][Byte[] Data]
```

| Field     | Kiểu dữ liệu | Mô tả                      |
| --------- | ------------ | -------------------------- |
| Length    | VarInt       | Độ dài của PacketID + Data |
| Packet ID | VarInt       | ID của packet              |
| Data      | Byte[]       | Nội dung packet            |

### Giải mã 
thì mục tiêu của chúng ta là đọc được value từ nó.
Đầu tiên chúng ta sẽ đọc **Length** (đây là cái đầu tiên)
thì Length nó là VarInt nên chúng ta chỉ cần đọc nó. (varint sẽ end ở bit 7 = 0 (đọc qua varint để hiểu cái này!))

**Đầu tiên đây là packet mẫu (Ko nén):**
``` 
b'\x03\x03\x80\x02\x1b\x00\x02\xcce2\x88\x9f\xf1>\xf7\x99[2\xc6/_\xcd\xc4\x06kenftr\x00\x01'
```

**Đọc length,packet_id**
như đã biết length nó là varint nên có thể đọc bằng api read varint của mclium hoặc tự viết logic (ở đây tui sẽ tự viết logic )
```python 
data = b'\x03\x03\x80\x02\x1b\x00\x02\xcce2\x88\x9f\xf1>\xf7\x99[2\xc6/_\xcd\xc4\x06kenftr\x00\x01' # byte mẫu ở trên

def read_varint(data,offset):
    num = 0
    shift = 0
    # lặp qua data
    for i in range(5):
        current = data[offset]
        offset += 1
        
        num |= (current & 0x7F) << shift
        
        if not (current & 0x80):
            return num,offset
        
        shift += 7 # skip qua byte kế 

if __name__ == '__main__':
    # đọc length 
    offset = 0 # đầu tiên cần khai báo offset đã ( vì đọc này cần offset)
    length,offset = read_varint(data,offset)
    # làm sao để biết đọc đúng chưa
    # thì length nằm ở vị trí đầu tiên nên offset chắc chắn sẽ là 1
    # vaf cais này = 1
    
    # đọc packet id 
    # vì packet id nằm sau length và cũng varint nên chúng ta chỉ việc call tiếp varint với offset đã + từ trước
    
    packet_id,offset = read_varint(length,offset)
    
    # như vậy là đã đọc được length và packet_id    
    # còn packet_data sẽ viết ở trang khác, vì cái đó rất nhiều kiểu dữ liệu
```

## Packet có nén 
thì cấu trúc của nó như sau:
``` 
[PacketLength][DataLength][Compressed Data]
```
| Field           | Kiểu dữ liệu | Mô tả                                                |
| --------------- | ------------ | ---------------------------------------------------- |
| PacketLength    | VarInt       | Độ dài của toàn bộ phần phía sau (DataLength + Data) |
| DataLength      | VarInt       | Độ dài của dữ liệu **trước khi nén**                 |
| Compressed Data | Byte[]       | Dữ liệu đã nén bằng zlib                             |


### Bên trong compressed data:
đống bên dưới là sau khi decompres ( tùy server mà bth sẽ là ZLIB)
| Field     | Kiểu dữ liệu |
| --------- | ------------ |
| Packet ID | VarInt       |
| Data      | Byte[]       |
thì compressed data nó cũng y chang packet bth thoi, đọc như cái kia 

chú ý qtrong 
DataLength > 0 → data đã bị nén
DataLength = 0 → KHÔNG nén (dù compression đã bật)

### Giải mã 
thì mục tiêu như kia, cta cần đọc được value từ nó ở đây là packet id 

```python
import zlib

data = b''  # buffer chứa raw bytes nhận từ socket (có thể chứa 1 hoặc nhiều packet)

def decompressed(data):
    # hàm dùng để giải nén dữ liệu bằng zlib
    # chỉ được gọi khi DataLength > 0 (tức là packet đã bị nén)
    return zlib.decompress(data)

def read_varint(data, offset):
    num = 0       
    shift = 0     

    for i in range(5):
        current = data[offset]  
        offset += 1             

        num |= (current & 0x7F) << shift

        if not (current & 0x80):
            return num, offset

        shift += 7  

    raise ValueError("VarInt is too big")


if __name__ == '__main__':
    # offset dùng để track vị trí đọc trong buffer
    offset = 0

    # 1. đọc PacketLength
    # PacketLength là VarInt đầu tiên trong packet
    # nó cho biết độ dài của phần còn lại phía sau (DataLength + Data)
    packet_length, offset = read_varint(data, offset)

    # 2. đọc DataLength
    # DataLength cho biết:
    #   = 0  → packet không bị nén
    #   > 0  → packet đã bị nén (cần decompress)
    data_length, offset = read_varint(data, offset)

    # 3. lấy phần data thực sự
    # chỉ lấy đúng packet_length byte tiếp theo
    # KHÔNG được dùng toàn bộ buffer vì có thể chứa nhiều packet
    compressed_data = data[offset: offset + packet_length]
    # 4. xử lý theo DataLength

    if data_length == 0:
        #không nén
        # cấu trúc lúc này:
        # [PacketLength][0][PacketID][Data]

        inner_offset = 0

        # đọc PacketID trực tiếp từ compressed_data
        packet_id, inner_offset = read_varint(compressed_data, inner_offset)

        # phần còn lại là packet_data
        packet_data = compressed_data[inner_offset:]

    else:
        #có nén
        # cấu trúc:
        # [PacketLength][DataLength][Compressed Data]
        # cần giải nén trước rồi mới đọc PacketID

        decompressed_data = decompressed(compressed_data)

        # sau khi decompress sẽ có dạng:
        # [PacketID][Data]
        inner_offset = 0

        packet_id, inner_offset = read_varint(decompressed_data, inner_offset)

        packet_data = decompressed_data[inner_offset:]

    # Result
    # packet_id: id của packet
    # packet_data: nội dung packet (raw bytes)
```