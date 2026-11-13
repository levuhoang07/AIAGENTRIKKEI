# Kế hoạch khảo sát DB-01 (Đông Nam Bộ Mở Rộng)

**Trình Trưởng phòng Phát triển Kinh doanh duyệt.**  
Địa bàn **DB-01 (Bình Dương - Đồng Nai - Bà Rịa Vũng Tàu)** được xếp **HẠNG 1 – ƯU TIÊN SỐ 1 MỞ RỘNG (Top 1)** với tổng điểm MCDA đạt **4.70/5.0** (Điểm trích xuất tại sheet `Ma Trận MCDA`, ô H4).

---

## 1. Mục tiêu khảo sát
1. Xác minh thực địa quy mô kho hàng, mức độ sẵn sàng hạ tầng CNTT và khả năng tích hợp giải pháp Hưng Phát WMS (Module Quản trị Đa kho, Kiểm kê Barcode/RFID và Quản lý Hạn dùng).
2. Kiểm tra cam kết SLA hỗ trợ on-site $\le$ 2h trên các tuyến giao thông huyết mạch (Quốc lộ 13 - Bình Dương, Xa lộ Hà Nội - Đồng Nai, Cao tốc Long Thành).
3. Tuyển chọn 10 doanh nghiệp hạt nhân có quy mô và ngân sách chi trả cao nhất để ký kết hợp đồng triển khai mẫu (Pilot Phase 1).

---

## 2. Phân bổ hồ sơ & Trọng tâm xác minh theo mô hình bán lẻ

Tổng số **320 hồ sơ khách hàng tiềm năng** tại DB-01 được phân nhóm chi tiết từ sheet `Dữ liệu nguồn`:

| Nhóm khách hàng từ sheet Dữ liệu nguồn | Số hồ sơ | Trọng tâm thông tin cần xác minh | Phụ trách đề xuất |
|---|:---:|---|---|
| **Chuỗi Bán lẻ Điện máy & Gia dụng** | 54 | Quản lý Serial/IMEI, luân chuyển giữa tổng kho và showroom, tích hợp bảo hành điện tử | Trưởng phòng Kinh doanh & Kỹ sư Giải pháp WMS |
| **Chuỗi Bán lẻ Nông sản & Thực phẩm sạch** | 54 | Quản lý hạn sử dụng (Date), kiểm soát kho lạnh, nhiệt độ bảo quản và tỷ lệ hủy hao hụt | Chuyên viên Tư vấn Giải pháp WMS |
| **Chuỗi Thời trang & Phụ kiện** | 53 | Quản lý tồn kho theo Size/Color (Ma trận SKU), kiểm kê không dây bằng công nghệ RFID | Chuyên viên Kinh doanh B2B |
| **Siêu thị & Đại siêu thị Tiện lợi** | 53 | Tốc độ quét mã tại điểm bán, đồng bộ tồn kho đa kênh (Omnichannel O2O) thời gian thực | Kỹ sư Giải pháp & Đối tác Tích hợp |
| **Chuỗi Mẹ & Bé Cao cấp** | 53 | Truy xuất nguồn gốc xuất xứ hàng nhập khẩu, quản lý combo/quà tặng khuyến mãi | Chuyên viên Kinh doanh B2B |
| **Chuỗi Bán lẻ Dược phẩm & Mỹ phẩm** | 53 | Chuẩn GSP, theo dõi số lô kiểm định, cảnh báo cận date và phân quyền dược sĩ | Chuyên viên Tư vấn WMS Chuyên ngành |
| **TỔNG CỘNG** | **320** | **100% hồ sơ được kiểm chứng kỳ Quý 1–2/2024, không trùng lặp nguồn** | |

---

## 3. Lịch trình công tác thực địa 5 ngày (Field Action Timeline)

* **Ngày 1 (Thủ Dầu Một & Bến Cát, Bình Dương):** Khảo sát 3 chuỗi tổng kho điện máy và đại siêu thị tiện lợi; đo đạc thời gian di chuyển thực tế từ trạm kỹ thuật TP.HCM đến Bình Dương.
* **Ngày 2 (Dĩ An & Thuận An, Bình Dương):** Làm việc với 3 chuỗi bán lẻ nông sản và thực phẩm tươi; demo trực tiếp tính năng quét mã Barcode di động và phân loại Date tự động.
* **Ngày 3 (Biên Hòa & Long Thành, Đồng Nai):** Thẩm định 2 chuỗi thời trang và dược phẩm; khảo sát khả năng lắp đặt cổng an ninh EAS và đầu đọc RFID cố định.
* **Ngày 4 (TP. Vũng Tàu & Bà Rịa):** Phỏng vấn trực tiếp Giám đốc Vận hành 2 chuỗi bán lẻ phục vụ du lịch và thực phẩm đóng gói; làm rõ yêu cầu kết nối API với hệ thống ERP hiện có.
* **Ngày 5 (Họp tổng kết tại Văn phòng Trung tâm):** Tổng hợp biên bản khảo sát thực địa, hoàn thiện bảng chấm điểm kỹ thuật 10 chuỗi hạt nhân và soạn thảo dự thảo hợp đồng cung cấp dịch vụ.

---

## 4. Dự toán ngân sách & Nhân sự phân công (RACI Matrix)

* **Dự toán ngân sách khảo sát:** 28.500.000 VNĐ (Bao gồm chi phí di chuyển 5 ngày xe chuyên dụng, công tác phí 4 nhân sự, thiết bị demo phần cứng RFID cầm tay).
* **Bảng phân công trách nhiệm (RACI):**
  * *Responsible (Thực hiện):* 02 Chuyên viên Phát triển Kinh doanh + 01 Kỹ sư Giải pháp WMS (On-site demo).
  * *Accountable (Chịu trách nhiệm chính):* Trưởng phòng Phát triển Kinh doanh.
  * *Consulted (Tham vấn):* Trưởng phòng Kỹ thuật & Hạ tầng SLA.
  * *Informed (Báo cáo nhận thông tin):* Ban Giám đốc (CEO & COO).

---

## 5. Đầu ra bàn giao sau đợt khảo sát
1. Bảng hồ sơ thẩm định chi tiết 20 doanh nghiệp ứng viên tại DB-01.
2. Biên bản kiểm tra hạ tầng mạng, diện tích kho và khả năng kết nối thiết bị.
3. Dự thảo hợp đồng triển khai WMS thử nghiệm (POC) cho 03 khách hàng cam kết ngân sách $\ge 500$ triệu VNĐ.
4. Tờ trình Ban Giám đốc phê duyệt thành lập Trạm Dịch vụ Kỹ thuật Vệ tinh tại Bình Dương để bảo đảm SLA $\le$ 2h lâu dài.

