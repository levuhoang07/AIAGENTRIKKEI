# QUY CHUẨN NĂNG LỰC DỮ LIỆU & GIẢI PHÁP QUẢN TRỊ DÀNH CHO AGENT

TẤT CẢ các tác vụ phân tích dữ liệu, xử lý bảng tính, lập báo cáo kinh doanh và tư vấn giải pháp từ nay trở về sau PHẢI TUÂN THỦ 100% THEO 3 TRỤ CỘT NĂNG LỰC CỐT LÕI DƯỚI ĐÂY:

---

## TRỤ CỘT 1: KỸ NĂNG XỬ LÝ & LÀM SẠCH DỮ LIỆU ĐA NGUỒN (DATA ENGINEERING & CLEANSING)

### A. Đa Nguồn Tiếp Nhận Dữ Liệu Đầu Vào (Multi-Source Ingestion)
- **Google Sheets:** Tự động chuyển đổi link chia sẻ thành endpoint trích xuất dữ liệu:
  `https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}` để nạp trực tiếp vào pipeline.
- **Lark Base (Bitable):** Tự động tiếp nhận URL bảng chia sẻ hoặc kết nối qua Open API trích xuất danh sách bản ghi về DataFrame.
- **Tệp Cục Bộ (Local Files):** Tự động theo dõi, quét và nạp các tệp `.xlsx`, `.xls`, `.csv` mới nhất trong thư mục `Downloads` hoặc `Desktop`.

### B. Kiểm Toán & Làm Sạch Dữ Liệu (Data Auditing & Cleansing)
- Tự động khử trùng lặp (Deduplication) dựa trên khóa định danh duy nhất.
- Chuẩn hóa kiểu dữ liệu: Ngày tháng định dạng chuẩn `d/m/yyyy`, chuỗi thời gian `mm/yyyy`, loại bỏ toàn bộ ký tự rác, dấu cách ẩn (`trim whitespace`), đồng bộ viết hoa/thường.
- Chuẩn hóa phân loại danh mục bằng tiếng Việt chuẩn có dấu, nhất quán.
- Tính toán chính xác các trường dẫn xuất: Doanh thu gộp, Giá chiết khấu, Doanh thu thuần, Giá vốn hàng bán, Lợi nhuận gộp, Biên lợi nhuận gộp (`0.00%`).
- Đóng gói dữ liệu sạch vào đối tượng bảng Excel Table (`Table1`) có gắn tiêu đề và bộ lọc tự động.

### C. Kiến Trúc 10 Sheets Bắt Buộc Sử Dụng Native Pivot Table
Khi tổng hợp, phân tích đa chiều dữ liệu lớn, **BẮT BUỘC sử dụng Native Pivot Table** (Pivot Table nguyên bản) và tuyệt đối không dùng bảng tĩnh thủ công:
1. `Dữ liệu nguồn `: Sheet chứa bảng dữ liệu sạch `Table1` (25 cột chuẩn hóa).
2. `Doanh thu theo TP`: Pivot Table + Pivot Chart theo Tỉnh/Thành phố.
3. `Tỷ lệ hài lòng KH`: Pivot Table + Pivot Chart phân tích Mức độ hài lòng TB (format số thập phân `0.0000`).
4. `Tổng hợp Doanh thu `: Pivot Table tóm tắt KPI toàn hệ thống + đếm thực thể duy nhất (`=COUNTA(UNIQUE(...))`).
5. `Doanh thu theo khu vực `: Pivot Table + Pivot Chart phân tích theo Vùng miền.
6. `Doanh thu theo kênh bán `: Pivot Table + Pivot Chart phân tích theo Kênh bán hàng / Phân phối.
7. `Doanh thu theo phân loại sản ph`: Pivot Table + Pivot Chart phân tích theo Nhóm ngành hàng / Dòng sản phẩm.
8. `Dash Board`: Bảng điều khiển trung tâm với KPI Cards, 7 biểu đồ Pivot Charts và **Slicers tương tác**.
9. `Doanh thu theo phân khúc KH `: Pivot Table + Pivot Chart phân tích theo Phân khúc khách hàng / Đối tượng mục tiêu.
10. `Doanh thu theo tháng`: Pivot Table + Pivot Chart chuỗi thời gian theo Tháng (`mm/yyyy`).

* **Quy tắc dùng chung PivotCache:** Tất cả các Pivot Tables trên các sheets phải được tạo từ **cùng một đối tượng `PivotCache`** kết nối với `Table1`.
* **Slicers Liên Kết Chéo:** Gắn Slicers tại sheet `Dash Board` và liên kết chéo (`PivotTables.AddPivotTable`) đến toàn bộ các Pivot Tables trên 10 sheets để khi lọc tại Slicer, toàn bộ hệ thống bảng và biểu đồ tự động cập nhật đồng bộ.
* **Định Dạng Kế Toán Chuẩn:**
  - Tiền tệ: Luôn dùng format kế toán VND có phân cách hàng nghìn và ký hiệu ₫:
    `_-* #,##0\ [$₫-42A]_-;\-* #,##0\ [$₫-42A]_-;_-* "-"\ [$₫-42A]_-;_-@_-`
  - Typography: Phông chữ đồng bộ `Aptos Narrow` hoặc `Segoe UI`.

---

## TRỤ CỘT 2: KỸ NĂNG TÌM RA VẤN ĐỀ & KHÁM NGHIỆM QUY TRÌNH (PROBLEM DISCOVERY & ROOT CAUSE DIAGNOSTICS)

Khi đối diện với bất kỳ tập dữ liệu nào, AI không chỉ dừng lại ở việc tính tổng mà phải có năng lực **chẩn đoán vấn đề nghiệp vụ sâu sắc**:

### A. Phát Hiện Bất Thường Dữ Liệu & Vi Phạm Quy Chuẩn (Data & Business Anomaly Detection)
- **Vi phạm tính khả thi vận hành:** Phát hiện các cam kết không khả thi (ví dụ: SLA phục vụ kỹ thuật on-site $\le$ 2h nhưng khoảng cách địa lý quá xa).
- **Lệch pha định vị sản phẩm:** Phát hiện tệp khách hàng hoặc giao dịch không phù hợp với năng lực cung ứng của doanh nghiệp.
- **Rác dữ liệu & Lỗi thời:** Bóc tách tỷ lệ trùng lặp thông tin liên hệ, dữ liệu lỗi thời qua nhiều năm, số điện thoại sai cú pháp, email không tồn tại.
- **Chênh lệch phân bổ nguồn lực:** Đánh giá sự phân bổ bất hợp lý về doanh thu, chi phí, công nợ hoặc cơ hội giữa các vùng miền/phân khúc.

### B. Khám Nghiệm Workflow Lỗi Hiện Tại (As-Is Process Diagnostics)
Bắt buộc phân tích tường minh 3 khía cạnh:
1. **Chủ thể thực hiện:** Ai làm? Vai trò chức danh nào đảm nhiệm? Máy móc hay con người?
2. **Bản chất thao tác:** Mức độ can thiệp thủ công (manual entry, copy-paste tự do từ nguồn không kiểm chứng, thiếu bộ lọc logic kiểm tra hợp lệ tại nguồn).
3. **Điểm đứt gãy bàn giao (*Broken Handoffs*):** Xác định chính xác khâu chuyển giao giữa các phòng ban (ví dụ: Thu thập thông tin $\rightarrow$ Kinh doanh $\rightarrow$ Kỹ thuật triển khai) bị tắc nghẽn ở đâu, tạo ra lãng phí nguồn lực và chi phí cơ hội như thế nào.

### C. Khái Quát Hóa Vấn Đề Cốt Lõi & Tìm Nguyên Nhân Gốc Rễ
- Cấu trúc hóa các phát hiện thành danh sách các **Vấn Đề Cốt Lõi** có số liệu định lượng chứng minh.
- Phân tích **Nguyên nhân gốc rễ (Root Causes)** bằng phương pháp 5 Whys hoặc biểu đồ xương cá (Fishbone), chỉ rõ nguyên nhân từ quy trình, công cụ, con người hay chính sách chỉ tiêu (KPI).

---

## TRỤ CỘT 3: KỸ NĂNG ĐƯA GIẢI PHÁP ĐỀ XUẤT & XUẤT BẢN ĐA PHƯƠNG TIỆN (SOLUTION ENGINEERING & ACTIONABLE DELIVERABLES)

Mọi phân tích đều phải dẫn đến các quyết định hành động cụ thể, khả thi và có thể đo lường:

### A. Thiết Kế Quy Trình Chuẩn Hóa Mới (To-Be Standardized Process)
Xây dựng quy trình 4 giai đoạn khép kín:
- **Giai đoạn 1 (Làm sạch & Chuẩn hóa):** Khử trùng, định danh kiểm toán, đồng bộ hóa dữ liệu.
- **Giai đoạn 2 (Bộ lọc điều kiện tiên quyết - Operational Gating Filter):** Đặt ra các tiêu chí "qua/loại" (Pass/Fail) cứng để loại bỏ ngay lập tức 100% các thực thể không khả thi, ngăn chặn rác tràn vào các khâu sau.
- **Giai đoạn 3 (Ma trận chấm điểm đa tiêu chí - MCDA Scoring Matrix):** Xây dựng bộ trọng số định lượng (ví dụ: Mức độ phù hợp, Tính khả thi, Cường độ cạnh tranh, Quy mô tiềm năng) để xếp hạng khách quan thứ tự ưu tiên.
- **Giai đoạn 4 (Phê duyệt & Triển khai thực địa):** Trình ban lãnh đạo danh sách rút gọn có điểm số cao nhất để phân bổ nguồn lực tiếp cận thực tế.

### B. Phân Định Rõ Ràng Các Nhóm Giải Pháp
- **Giải pháp ưu tiên (Quick-wins / Phase 1):** Cắt bỏ ngay lãng phí, áp dụng nguyên lý Pareto (tập trung 80% lực lượng vào 20% đối tượng tiềm năng nhất).
- **Giải pháp còn lại (Medium & Long-term / Phase 2-3):** Mở rộng hệ sinh thái đối tác, số hóa tự động hóa quy trình, phát triển phiên bản sản phẩm rút gọn.

### C. Xuất Bản Đa Phương Tiện Độc Lập
1. **Interactive HTML Dashboard:**
   - Single-file HTML độc lập hoàn toàn, không cần web server (mở trực tiếp trên Edge/Chrome).
   - Xây dựng bằng Tailwind CSS, Chart.js, Google Fonts.
   - KPI Cards động, Slicers lọc thời gian thực, bảng dữ liệu phân trang có Live Search tức thì và nút Xuất CSV sạch.
   - Tích hợp các tab phân tích nghiệp vụ, lưu đồ As-Is vs To-Be và ma trận MCDA.
2. **Báo Cáo Quản Trị Cấp Cao (Word & PDF Vector):**
   - Soạn thảo cấu trúc 5 chương hoàn chỉnh, văn phong học thuật và quản trị cấp cao.
   - Xuất PDF chuẩn vector văn phòng qua Word COM phục vụ in ấn và trình chiếu lãnh đạo.
