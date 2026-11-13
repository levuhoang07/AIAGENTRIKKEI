# TÀI LIỆU HUẤN LUYỆN VÀ CHỈ DẪN VẬN HÀNH DÀNH CHO AI ANTIGRAVITY
## (CHUYÊN GIA DỮ LIỆU - CHẨN ĐOÁN VẤN ĐỀ - TƯ VẤN GIẢI PHÁP CHIẾN LƯỢC)

> **Mục tiêu tối thượng của gói huấn luyện:** Trang bị cho bất kỳ AI Antigravity nào (hoặc AI coding assistant cao cấp) toàn bộ quy chuẩn phương pháp luận, bộ mã nguồn tự động hóa và khung đánh giá để thành thạo **3 TRỤ CỘT NĂNG LỰC CỐT LÕI**:
> 1. **Xử lý & Làm sạch dữ liệu đa nguồn** -> Tạo Workbook Excel 10 sheets Native Pivot Tables & Slicers.
> 2. **Chẩn đoán vấn đề & Khám nghiệm quy trình lỗi** -> Phân tích As-Is workflow, broken handoffs & nguyên nhân gốc rễ.
> 3. **Hoạch định giải pháp & Xuất bản đa phương tiện** -> Operational Gating Filter, ma trận MCDA, Interactive HTML Dashboard & Báo cáo Quản trị Word/PDF.

---

## I. CẤU TRÚC GÓI HUẤN LUYỆN (PACKAGE STRUCTURE)

```
ANTIGRAVITY_AI_TRAINING_PACKAGE/
│
├── CAM_NANG_HUAN_LUYEN_AI.md            <-- Cẩm nang huấn luyện tổng thể này
├── QUICK_START_TEST.ps1                 <-- Script kiểm thử 1-click chạy tự động từ A-Z
│
├── 00_PROMPT_AND_RULES_CONFIG/          <-- Cấu hình luật & Prompt nạp vào AI
│   ├── SYSTEM_PROMPT_INSTRUCTION.md     <-- System Prompt nạp vào AI
│   ├── AGENTS.md                        <-- Bộ quy chuẩn bắt buộc của Agent
│   ├── GEMINI.md                        <-- Bộ chỉ dẫn thực thi cho Antigravity
│   └── skill/
│       └── bi-problem-solver/
│           └── SKILL.md                 <-- Skill chuẩn Antigravity
│
├── 01_GOLDEN_TEMPLATES/                 <-- Tệp mẫu chuẩn mực & Đặc tả quy chuẩn
│   ├── UNIVERSAL_10_SHEET_PIVOT_TEMPLATE.xlsx <-- File mẫu chuẩn 10 sheets & Native Pivot
│   └── UNIVERSAL_DATA_CLEANING_AND_BI_STANDARD.md <-- Đặc tả 25 cột & 10 sheets
│
├── 02_CORE_PIPELINE_ENGINES/            <-- Bộ mã nguồn tự động hóa cốt lõi
│   ├── data_pipeline_engine.py          <-- Nạp đa nguồn (GSheets/Lark/File) & Làm sạch 25 cột
│   ├── build_full_pivot_workbook.ps1    <-- Excel COM tạo 10 sheets, Native Pivot & Slicers
│   ├── generate_html_dashboard.py       <-- Sinh HTML Dashboard tương tác độc lập
│   ├── build_integrated_html.py         <-- Sinh Dashboard 5 Tabs tích hợp As-Is/To-Be & MCDA
│   ├── build_full_word_report.py        <-- Sinh Báo cáo Quản trị chuyên sâu 5 chương Word
│   └── export_pdf_and_distribute.ps1    <-- Xuất PDF vector từ Word COM & Phân phối file
│
└── 03_BENCHMARK_AND_VALIDATION/         <-- Dữ liệu kiểm chuẩn & Thước đo năng lực
    ├── generate_synthetic_benchmark.py  <-- Sinh tập dữ liệu 500 dòng chứa 5 lỗi thực tế
    └── EVALUATION_RUBRIC.md             <-- Thang đo 15 tiêu chí đánh giá năng lực AI
```

---

## II. TRỤ CỘT 1: KỸ NĂNG XỬ LÝ & LÀM SẠCH DỮ LIỆU ĐA NGUỒN

### 1. Tiếp Nhận Đa Nguồn (Multi-Source Ingestion)
- **Google Sheets:** Tự động trích xuất Sheet ID và GID, chuyển thành URL export CSV:
  `https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}`
- **Lark Base (Bitable):** Đọc qua Open API phân trang hoặc liên kết bảng chia sẻ công khai.
- **Tệp Cục Bộ:** Quét tự động thư mục Downloads hoặc Desktop.

### 2. Làm Sạch & Chuẩn Hóa Schema 25 Cột Giao Dịch (`Table1`)
- Loại bỏ khoảng trắng thừa ở cả hai đầu (`trim whitespace`), đồng bộ viết hoa/thường.
- Chuẩn hóa ngày tháng theo chuẩn Việt Nam: `d/m/yyyy`, trích xuất cột tháng chuỗi `=TEXT(B:B, "mm/yyyy")`.
- Tính toán chính xác các trường tài chính:
  - Doanh thu gộp = Số lượng * Giá niêm yết
  - Giá chiết khấu = Doanh thu gộp * Chiết khấu
  - Doanh thu thuần = Doanh thu gộp - Giá chiết khấu
  - Lợi nhuận gộp = Doanh thu thuần - Giá vốn hàng bán
  - Biên lợi nhuận gộp = (Lợi nhuận gộp / Doanh thu thuần) * 100%
- Định dạng tiền tệ kế toán VND có phân cách hàng nghìn và ký hiệu ₫:
  `_-* #,##0\ [$₫-42A]_-;\-* #,##0\ [$₫-42A]_-;_-* "-"\ [$₫-42A]_-;_-@_-`

### 3. Kiến Trúc 10 Sheets Bắt Buộc Dùng Native Pivot Tables & Slicers
- **Bắt buộc dùng Native Pivot Table:** Không dùng bảng tĩnh thủ công khi tổng hợp dữ liệu lớn.
- **Chung 1 PivotCache:** Tạo duy nhất một `PivotCache` trỏ vào `Table1`, và tái sử dụng `PivotCache` đó cho toàn bộ 8 bảng Pivot Tables trên các sheets.
- **Slicers Liên Kết Chéo:** Slicers tại sheet `Dash Board` được liên kết tới tất cả các Pivot Tables qua lệnh:
  ```powershell
  $slicerCache.PivotTables.AddPivotTable($pt)
  ```
  Nhờ đó, khi người dùng click lọc tại Dashboard, toàn bộ hệ thống Pivot Tables và Pivot Charts trên 10 sheets tự động lọc đồng bộ!

---

## III. TRỤ CỘT 2: KỸ NĂNG TÌM RA VẤN ĐỀ & KHÁM NGHIỆM QUY TRÌNH LỖI

AI không chỉ làm sạch bề mặt mà phải đóng vai trò là một **Chuyên Gia Chẩn Đoán Nghiệp Vụ**:

### 1. Kiểm Toán Bất Thường Dữ Liệu (Anomaly Auditing)
- **Bất khả thi về vận hành (SLA Violations):** Phát hiện các cam kết phi thực tế (ví dụ: yêu cầu hỗ trợ on-site $\le$ 2h trong khi cự ly địa lý cách trung tâm trên 500km).
- **Lệch pha định vị sản phẩm (Product Mismatch):** Phát hiện nhóm khách hàng yêu cầu giải pháp không tương thích với năng lực cốt lõi của doanh nghiệp.
- **Rác & Lỗi thời (Stale & Bad Data):** Bóc tách tỷ lệ trùng lặp, dữ liệu cũ qua các năm, thông tin liên hệ không hợp lệ.
- **Mất cân đối thị trường (Market Imbalance):** Đánh giá mức độ lệch pha về doanh thu, ngân sách và mức độ sẵn sàng công nghệ giữa các khu vực.

### 2. Khám Nghiệm Workflow Lỗi Hiện Tại (As-Is Process Diagnostics)
Phải trả lời tường minh 3 câu hỏi:
1. **Ai làm?** Xác định chức danh nhân sự đảm nhiệm (chuyên viên nghiên cứu, chuyên viên kinh doanh).
2. **Làm bằng gì và như thế nào?** 100% thủ công bằng con người; tìm kiếm rời rạc, copy-paste tự do vào bảng tính không có kiểm tra hợp lệ logic (validation rules).
3. **Đứt gãy ở đâu (Broken Handoffs)?** Dữ liệu rác chuyển giao trực tiếp sang đội ngũ Kinh doanh và Kỹ thuật mà không qua bộ lọc kỹ thuật, gây lãng phí chi phí cơ hội và xung đột vận hành.

### 3. Cấu Trúc Hóa Vấn Đề & Tìm Nguyên Nhân Gốc Rễ (5 Whys / Fishbone)
- Liệt kê danh sách các **Vấn Đề Cốt Lõi** kèm số liệu định lượng chứng minh từ tập dữ liệu.
- Truy tìm nguyên nhân gốc rễ: Thiếu quy trình kiểm soát chất lượng tại nguồn, áp lực chỉ tiêu KPI thuần số lượng thay vì chất lượng chuyển đổi, thiếu công cụ tự động hóa.

---

## IV. TRỤ CỘT 3: KỸ NĂNG ĐƯA GIẢI PHÁP ĐỀ XUẤT & XUẤT BẢN ĐA PHƯƠNG TIỆN

### 1. Thiết Kế Quy Trình Chuẩn Hóa Mới (To-Be Workflow 4 Bước)
- **Bước 1: Data Cleansing & Standardization:** Chuẩn hóa dữ liệu nguồn, khử trùng, gắn mã kiểm toán.
- **Bước 2: Operational Gating Filter:** Bộ lọc điều kiện tiên quyết kỹ thuật loại bỏ ngay lập tức 100% đối tượng vi phạm (SLA quá xa, sai phân khúc sản phẩm).
- **Bước 3: MCDA Scoring Matrix:** Ma trận đánh giá đa tiêu chí với trọng số định lượng khách quan (Product Fit, Feasibility, Competition, Scale) để xếp hạng ưu tiên.
- **Bước 4: Board Approval & Targeted Field Action:** Trình lãnh đạo phê duyệt Top danh sách rút gọn và phân bổ nguồn lực tiếp cận thực tế.

### 2. Phân Định Nhóm Giải Pháp
- **Giải pháp ưu tiên (Quick-wins / Phase 1):** Cắt bỏ lãng phí ngay lập tức, áp dụng nguyên lý Pareto (dồn 80% lực lượng vào 20% đối tượng khả thi nhất).
- **Giải pháp còn lại (Medium & Long-Term / Phase 2-3):** Tự động hóa cổng nạp dữ liệu, xây dựng mạng lưới đối tác tích hợp, phát triển sản phẩm rút gọn.

### 3. Xuất Bản Đa Phương Tiện Độc Lập
1. **Interactive HTML Dashboard:**
   - Single-file HTML độc lập, mở ngay trên Edge/Chrome mà không cần web server.
   - Xây dựng bằng Tailwind CSS, Chart.js, Google Fonts.
   - KPI Cards động, Slicers lọc thời gian thực, bảng dữ liệu phân trang có Live Search tức thì và nút Xuất CSV sạch.
   - Tích hợp 5 Tabs: Dashboard, Phân tích Nghiệp vụ As-Is/To-Be, Ma trận MCDA, Kế hoạch hành động và Bảng dữ liệu.
2. **Báo Cáo Quản Trị Cấp Cao (Word & PDF Vector):**
   - Soạn thảo cấu trúc 5 chương hoàn chỉnh, định dạng chuẩn văn phòng bằng `python-docx`.
   - Xuất bản PDF chuẩn vector qua Word COM phục vụ in ấn và trình chiếu lãnh đạo.

---

## V. BÍ QUYẾT KỸ THUẬT & XỬ LÝ LỖI (GOTCHAS FOR AI)

1. **Quyền Truy Cập Excel/Word COM:** Trên Windows, việc gọi COM Automation cho Office đòi hỏi quyền `BypassSandbox: true`. Các tác vụ Python tính toán và tạo HTML chạy ở chế độ bình thường.
2. **Lỗi Mảng PowerShell Khi Gán Dữ Liệu (Array Unrolling):** Khi gán dữ liệu vào Excel Range trong PowerShell, luôn bọc mảng đúng kiểu `[object[,]]` hoặc gán qua cell để tránh lỗi `InvalidCastException`.
3. **Liên Kết Slicers Đa Bảng:** Để Slicer kết nối được nhiều Pivot Table, tất cả các Pivot Table đó **bắt buộc phải chia sẻ chung một `PivotCache`**.

---

## VI. HƯỚNG DẪN KIỂM THỬ 1-CLICK (VERIFICATION)

Mở PowerShell tại thư mục gói và chạy:
```powershell
powershell -ExecutionPolicy Bypass -File QUICK_START_TEST.ps1
```
Script sẽ tự động:
1. Sinh tập dữ liệu benchmark 500 dòng chứa 5 lỗi thực tế (`generate_synthetic_benchmark.py`).
2. Chạy pipeline làm sạch dữ liệu và tạo báo cáo HTML tương tác.
3. Sinh báo cáo quản trị chuyên sâu 5 chương và đối chiếu theo thước đo đánh giá.

