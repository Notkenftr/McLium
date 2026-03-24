# Làm thế nào để tạo plugin đầu tiên của bro
## Trước tiên chúng ta cần biết mclium có mấy dạng plugin
### 1. OneLine 
Đây là dạng cơ bản nhất được, plugin của bạn sẽ được gọi qua kiểu như sau
```bash 
mclium {inline_command_name} {args}
```
ví dụ ở đây mình có plugin example với args là --address và --port 
```bash 
mclium example --address localhost --port 25565
```

**Ưu điểm**
- Sử dụng nhanh chóng 
- Phù hợp với các plugin nhẹ không có depend lớn 
**Nhược điểm**
- Đối với các plugin sử dụng api từ plugin khác, nếu plugin khác đó nặng thì sẽ mở khá tốn thời gian 

### 2. Subcommand
Đây là dạng plugin thứ 2, cái này sẽ được gọi sau khi mclium đã load toàn bộ plugin. Ví dụ:
```bash
mclium
```
đợi load xong 
```bash
McLium > {subcommand_name} {args}
```
ví dụ ở đây mình có plugin example với args là --address và --port 

```bash
McLium > example --address localhost --port 25565
```

**Ưu điểm:**
- Có thể sử dụng được các api từ plugin khác mà không gặp rắc rối 
- Ổn định vì nó đã load gần như mọi thứ của McLium 
**Nhược điểm:**
- Startup chậm (càng nhiều plugin load càng chậm)

### 3. Task
Đây là dạng plugin thứ 3. Có tác dụng chạy nền. Nó sẽ được load sau khi chạy mclium

## Tiếp theo là plugin.yml 
mẫu:
```yaml
main: 'entry_point.Main'
name: "example"
description: "this is example plugin"
version: 1.0.0
author: ["kenftr"]

require_libraries: []

depend: []
softdepend: []

metadata:
  type: "utils"
  category: "utils"

```
main: là nơi mà mclium sẽ call class đó 
name: tên plugin của bạn 
description: giới thiệu sơ lược 
version: phiên bản 
author: người tạo ra plugin 

require_libraries: cần thư viện python gì 

depend: cần plugin nào load trước
softdepend: cũng như depend nhưng nếu không load được plugin cần hoặc không có plugin cần sẽ không bị disable plugin

metadata: các data phụ ( dành cho các nền tảng share plugin v.v nếu có )
