# BỘ TIÊU CHÍ ĐÁNH GIÁ NĂNG LỰC AI (EVALUATION RUBRIC)

Bảng tiêu chí gồm 15 chỉ số định lượng đánh giá năng lực của một AI khi xử lý dữ liệu và giải quyết bài toán kinh doanh.

| Trụ Cột | STT | Tiêu Chí Đánh Giá | Yêu Cầu Đạt Chuẩn (Benchmark) | Thang Điểm |
|:---|:---:|:---|:---|:---:|
| **Trụ Cột 1: Xử Lý Dữ Liệu** | 1 | Đa Nguồn Ingestion | Tự động tải từ Google Sheets URL, Lark Base API hoặc file cục bộ | 10 |
| | 2 | Chuẩn Hóa Schema 25 Cột | Đầy đủ 25 cột chuẩn, định dạng ngày `d/m/yyyy`, tháng `mm/yyyy`, đóng gói vào `Table1` | 10 |
| | 3 | Native Pivot Tables | Sử dụng 100% Native Pivot Table chia sẻ chung 1 `PivotCache` trỏ vào `Table1` | 10 |
| | 4 | Slicers Tương Tác | Slicer trên Dashboard liên kết chéo (`AddPivotTable`) điều khiển đồng bộ 10 sheets | 10 |
| | 5 | Định Dạng Kế Toán | Tiền tệ format VND chuẩn kế toán `#,##0 ₫`, tỷ lệ % `0.00%`, độ hài lòng `0.0000` | 10 |
| **Trụ Cột 2: Tìm Ra Vấn Đề** | 6 | Kiểm Toán Bất Thường | Phát hiện lỗi SLA khoảng cách, dữ liệu lỗi thời, trùng lặp, thông tin hỏng | 10 |
| | 7 | Khám Nghiệm As-Is Workflow | Phân tích rõ chủ thể (ai làm), mức độ can thiệp thủ công bằng tay 100% | 10 |
| | 8 | Nhận Diện Broken Handoffs | Chỉ rõ điểm gãy bàn giao giữa Nghiên cứu thị trường $\rightarrow$ Kinh doanh $\rightarrow$ Kỹ thuật | 10 |
| | 9 | Cấu Trúc 7 Vấn Đề Cốt Lõi | Liệt kê chi tiết 7 vấn đề cốt lõi kèm số liệu định lượng chứng minh từ tập dữ liệu | 10 |
| | 10 | Phân Tích Nguyên Nhân Gốc | Áp dụng kỹ thuật 5 Whys / Fishbone chỉ ra căn nguyên từ quy trình, chính sách và công cụ | 10 |
| **Trụ Cột 3: Đưa Giải Pháp** | 11 | Operational Gating Filter | Thiết lập bộ lọc điều kiện tiên quyết loại bỏ ngay lập tức các thực thể vi phạm SLA/sản phẩm | 10 |
| | 12 | Ma Trận Chấm Điểm MCDA | Xây dựng công thức trọng số đa tiêu chí (Product Fit, Feasibility, Competition, Scale) | 10 |
| | 13 | Phân Định Nhóm Giải Pháp | Phân định rõ ràng: Giải pháp ưu tiên (Quick Wins/Pareto) vs Giải pháp trung & dài hạn | 10 |
| | 14 | Interactive HTML Dashboard | Sinh tệp HTML độc lập (Tailwind CSS, Chart.js, Slicers thời gian thực, Live Search, Xuất CSV) | 10 |
| | 15 | Báo Cáo Quản Trị Word/PDF | Soạn thảo báo cáo 5 chương chuyên sâu bằng Word và xuất bản PDF vector chuẩn văn phòng | 10 |
| **TỔNG ĐIỂM** | | | **Đạt chuẩn xuất sắc khi $\ge 135/150$ điểm (90%)** | **150** |