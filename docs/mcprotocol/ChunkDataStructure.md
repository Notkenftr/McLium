### Chunk Data Structure

| Tên trường (Field Name) | Kiểu dữ liệu (Field Type) | Ghi chú (Notes) |
| :--- | :--- | :--- |
| **Heightmaps** | Prefixed Array of Heightmap | Xem cấu trúc `Heightmap` trong Chunk Format. |
| **Data** | Prefixed Array of Byte | Xem cấu trúc `Data` (các chunk section) trong Chunk Format. |
| **Block Entities** | Prefixed Array | Một mảng chứa các Block Entity (Thực thể khối). Cấu trúc của từng phần tử trong mảng như sau: |
| ↳ _Packed XZ_ | Unsigned Byte | Tọa độ nén tương đối so với Chunk chứa nó. Giá trị hợp lệ từ 0-15.<br>**Mã hóa:** `((blockX & 15) << 4) \| (blockZ & 15)`<br>**Giải mã:** `x = packed_xz >> 4`, `z = packed_xz & 15` |
| ↳ _Y_ | Short | Độ cao Y (tọa độ thực tế trong thế giới/world). |
| ↳ _Type_ | VarInt | Loại của Block Entity (ID). |
| ↳ _Data_ | NBT | Dữ liệu của Block Entity. Các tag `x`, `y`, và `z` đã được lược bỏ (vì đã gửi ở các trường trên). |