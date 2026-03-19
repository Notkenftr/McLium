## 1. McLium được chia thành 3 Layer<br>
**Layer 1 (L1):** Đây là tầng thấp nhất và cũng khó sài nhất. Api của McLium sẽ cho phép bạn
edit từng byte trong packet hay là file mca.<br>
**Layer 2 (L2):** Layer 2 sẽ được Wrapped lên Layer 1, nó sẽ giảm đi độ control của bạn nhưng
vẫn cho bạn khả năng tùy chỉnh sâu<br>
**Layer 3 (L3):** Đây là Layer dễ sài nhất với nhiều api được Wrapped từ Layer 2. Đổi lại bạn sẽ không
có khả năng tùy chỉnh sâu các packet, mca v.v 

## 2. Về docs 
**Docs** của bọn mình cũng được chia thành 2 loại là: Beginner và Expert<br>
Nếu bạn mới bắt đầu với McLium bọn mình khuyên bạn nên đọc beginner vì đa số ở Expert 
là về các api ở **L1**

## 3. Cấu trúc docs
Bọn mình có cấu trúc docs như sau
``` 
[P1. Giới thiệu tính năng]
[P2. List những api sẽ import]
[P3.n Hướng dẫn sử dụng Module/Api/v.v]
[P3.n Code mẫu]
[P3.n Bảng ghi chú về từng field hay param được sử dụng]
[P3.n+? Các tính năng khác]
```
Lưu ý:
- Đa số giải thích về các hoạt động bọn mình sẽ comment trong **Code mẫu** chứ không ghi ở ngoài.

## 4. Bắt đầu 
### Để bắt đầu với McLium mình khuyên bạn nên đọc theo trình tự sau(toàn bộ file docs đều được đặt trong ``./vietnamese/Beginer``):<br>
1. How to make a plugin<br>
1.1: Hello World<br>
1.2: Plugin.yml<br>
1.3: SubCommandModule<br>
1.4: SubCommandOneLineModule
1.5: McLiumTaskModule<br>
2. How to using L3McProtocol<br>
2.1: PacketStructure<br>
2.2: PacketList<br>
2.4: How to make a custom packet with L3PacketBuilder<br>
3. How to using L3ProtocolSession<br>
3.1: What is ProtocolSession<br>
3.2: Server connection process<br>
3.3: Connect to the server<br>
3.4: Sending Packet with L3PacketBuilder<br>
3.5: Auto Session Lifecycle<br>
3.6: Handling Event<br>

### Nếu bạn muốn tùy chỉnh sâu hơn thì có thể đọc qua theo trình tự này (Toàn bộ file docs đều được đặt trong ``./vietnamese/Intermediate``):<br>
1. How to using L2 McProtocol<br>
1.2: _Field and ProtocolFieldType<br>
1.3: Craft your packet<br>
1.4: L2PacketBuilderWrappedApi<br>
1.5: How to using PacketFlow<br>
2. How to using L2ProtocolSession<br>
2.1: Create your first login process.<br>
2.2: Auto Session Lifecycle<br>
2.3: Receiving Packet<br>
2.4: Handling Event<br>
2.5: Make first bot<br>

### Nếu bạn đã thông thạo L3 và L2 mà cũng muốn có khả năng tùy biến sâu hơn thì hãy đến với L1.
**Lưu ý:** L1 được thiết kế để pentest, custom packet v.v. bạn có thể craft packet v.v bằng L1 và send bằng các api ở tầng cao hơn như L2 L3. Để sử dụng L1 bạn cần hiểu rõ Minecraft java protocol vì đó là nền tảng để bạn có thể craft các custom packet.
1. L1 McProtocol<br>
1.1: utils api / getter<br>
1.2: setter<br>
1.3: insert byte<br>
1.4: set hooker<br>
1.5: custom field byte<br>
1.6: fast write<br>
1.9: build<br>
1.10: build no length<br>
1.11: async build<br>
1.12: encode field hooker<br>
1.13: field length<br>
1.14: inject bytearray to index<br>
2. L1PacketBuilderWrappedApi<br>
2.1: Custom your length<br>
2.2: rebuild<br>
2.3: fake field<br>
2.4: field inject method<br>
3. ProtocolSession<br>
3.1: L1Event<br>
3.2: Packet inject<br>
3.3: APIs help to analyze packets from the server.<br>
3.4: Write your first login flow<br>
3.5: Change to Play State<br>
3.6: Overwrite api<br>
3.7: set hooker<br>
4. Mc4j<br>
4.1 What is Mc4J<br>