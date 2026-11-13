# QUY CHUẨN VẬN HÀNH DỮ LIỆU & GIẢI PHÁP CHIẾN LƯỢC CHO ANTIGRAVITY

Quy chuẩn này là kim chỉ nam bắt buộc cho Antigravity trong mọi tác vụ phân tích, làm sạch dữ liệu, tìm kiếm vấn đề nghiệp vụ và đề xuất giải pháp thực thi:

1. **Trụ Cột 1: Xử Lý & Làm Sạch Dữ Liệu Đa Nguồn**
   - Hỗ trợ đa nguồn đầu vào: Google Sheets (URL/Export CSV), Lark Base (Bitable URL/API), Tệp Excel/CSV cục bộ.
   - Làm sạch, khử trùng lặp, chuẩn hóa kiểu dữ liệu, định dạng kế toán VND (`_-* #,##0\ [$₫-42A]_-;...`), tỷ lệ %, ngày tháng `d/m/yyyy`.
   - Bắt buộc dùng **Native Pivot Tables** nguyên bản chia sẻ chung một `PivotCache` trỏ tới `Table1` tại sheet dữ liệu nguồn.
   - Cấu trúc 10 sheets chuẩn mực tích hợp Pivot Charts và **Slicers lọc tương tác đa chiều** tại Dashboard.

2. **Trụ Cột 2: Tìm Ra Vấn Đề & Khám Nghiệm Quy Trình Lỗi**
   - Kiểm toán toàn diện tính toàn vẹn dữ liệu, phát hiện các bất thường kinh doanh (vi phạm cam kết SLA, lệch pha định vị sản phẩm, dữ liệu rác, chênh lệch thị trường).
   - Khám nghiệm quy trình lỗi hiện tại (As-Is Workflow): Phân tích rõ chủ thể (ai làm), mức độ can thiệp thủ công (manual entry, copy-paste tự do), và các điểm đứt gãy bàn giao (*broken handoffs*) gây lãng phí chi phí cơ hội.
   - Cấu trúc hóa các Vấn Đề Cốt Lõi và tìm ra Nguyên nhân gốc rễ (Root Causes) bằng phương pháp 5 Whys.

3. **Trụ Cột 3: Đưa Giải Pháp Đề Xuất & Xuất Bản Đa Kênh**
   - Thiết kế Quy trình chuẩn hóa mới (To-Be Workflow 4 bước): Làm sạch $\rightarrow$ Bộ lọc điều kiện tiên quyết (Operational Gating Filter) $\rightarrow$ Ma trận chấm điểm đa tiêu chí (MCDA Scoring Matrix) $\rightarrow$ Kế hoạch hành động thực địa.
   - Phân định rõ ràng: Giải pháp ưu tiên triển khai ngay (Quick-wins / Pareto) vs Giải pháp trung và dài hạn.
   - Xuất bản đa phương tiện tự động:
     * **Interactive HTML Dashboard:** File HTML độc lập, tích hợp Tailwind CSS, Chart.js, Slicers thời gian thực, Live Search, phân trang động và nút Xuất CSV.
     * **Báo cáo Quản trị chuyên sâu (Word & PDF):** 5 chương chuẩn mực phục vụ ban lãnh đạo ra quyết định.
