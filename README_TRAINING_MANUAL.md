# Chạy AI301 Đề 04

Luồng Task 2 dùng Python 3.10 trở lên và không cần cài thêm thư viện. Đây là Agent điều phối theo quy tắc, gọi hai công cụ Python trong cùng lần chạy. Dữ liệu và quy tắc trong bộ audit là giả lập. Cần đối chiếu cấu trúc và quy tắc với bộ giảng viên cấp trước khi nghiệm thu bộ thi.

```powershell
python ./02_CORE_PIPELINE_ENGINES/task2_market_agent.py --input ./bo-du-lieu --rules ./quy-tac.json --output ./ket-qua-lan-01
./QUICK_START_TEST.ps1
```

Để đối chiếu trực tiếp workbook leads, cài `openpyxl` vào môi trường Python rồi chạy:

```powershell
python ./02_CORE_PIPELINE_ENGINES/task2_market_agent.py --input ../AI301_De04_Du_Lieu_Mau_1000_Leads_Cleaned.xlsx --output ./ket-qua-excel
```

Nhánh Excel đọc sheet `Dữ liệu nguồn`, tổng hợp bốn địa bàn, trích điểm và kết luận ghi sẵn trong `Ma Trận MCDA` với tham chiếu ô. Mã hồ sơ khảo sát được đối chiếu với nguồn để xác định nhóm khách. Các mục thiếu được đánh dấu cần kiểm tra hoặc bổ sung. Nhánh Excel giữ riêng đề xuất ghi trong workbook và quyết định đã xác minh. Luồng JSON dùng `--rules` để chạy đánh giá theo các quy tắc ngưỡng đã cấu hình.

Thư mục kết quả phải mới và nằm ngoài thư mục nguồn. Một lần chạy thành công tạo `comparison.json` (bảng chi tiết cho 4 địa bàn), `report.md` (báo cáo và kế hoạch khảo sát), và `trace.json` (tệp đã đọc, SHA-256, lần gọi công cụ, bản ghi bị loại hoặc trùng và trạng thái chạy).

## Cấu trúc dữ liệu tạm thời

- `manifest.json` có `areas` (4 mã địa bàn duy nhất) và `documents` (danh sách tệp JSON tương đối trong thư mục nguồn).
- Mỗi tệp nguồn chứa một mảng bản ghi với `area`, `kind`, `source`, `period`, `locator` và `metrics`. Năm nhóm `kind` là `market`, `competitor`, `feedback`, `product`, `capacity`. Mỗi quan sát trong `metrics` có `value` dạng số và `unit`. Dữ kiện áp dụng chung cần được ánh xạ tới từng địa bàn có liên quan, giữ cùng tham chiếu gốc.
- Tệp quy tắc chứa `version`, `metrics` và `survey`. Mỗi tiêu chí khai báo `operator` (`>=` hoặc `<=`), `threshold`, `weight`, `unit`, `period`, `kinds` và tùy chọn `gate`. `survey` ánh xạ mã địa bàn sang `group`, `verify`, `owner` do nhóm nghiệp vụ xác nhận.
- Tham khảo các tệp đầu vào và quy tắc trong [bộ audit giả lập](03_BENCHMARK_AND_VALIDATION/task2_audit). Nếu bộ chính thức dùng Excel, tài liệu văn bản hoặc quy tắc khác, cần bổ sung bộ đọc hoặc cơ chế tính tương ứng. Luồng hiện tại đọc dữ kiện đã cấu trúc, chưa trích xuất trực tiếp từ Word/PDF/Excel.

## Thiết kế và bàn giao

Mục tiêu là xác định hai địa bàn đáng khảo sát thêm từ hồ sơ được cấp và chỉ rõ chỗ còn thiếu căn cứ. Đầu vào gồm bộ hồ sơ của bốn địa bàn, tiêu chí và năng lực triển khai.

| Bước | Đầu vào | Công việc và lý do giao cho Agent | Đầu ra | Phụ trách |
|---|---|---|---|---|
| Tiếp nhận | Hồ sơ và quy tắc được cấp | Đối chiếu cấu trúc, xác nhận bản quy tắc và ánh xạ nguồn | Bộ đầu vào đã xác nhận | Chuyên viên nghiên cứu |
| Tổng hợp | Hồ sơ đã cấu trúc | Agent đối chiếu kỳ và đơn vị, gộp quan sát lặp cùng nguồn và phát hiện giá trị trái nhau để giảm sai lệch khi tổng hợp | Dữ kiện có nguồn và tín hiệu cần kiểm tra | Agent, chuyên viên nghiên cứu chịu trách nhiệm |
| Đánh giá | Dữ kiện và quy tắc | Agent áp dụng ngưỡng và tính điểm nhất quán trên cả bốn địa bàn | Điểm, điều kiện bắt buộc và đề xuất sơ bộ | Agent, nhóm Phát triển Kinh doanh chịu trách nhiệm |
| Bàn giao | Bảng đánh giá và thông tin khảo sát | Agent sinh báo cáo từ kết quả chung để tránh lệch giữa bảng và đề xuất | Báo cáo và kế hoạch khảo sát | Agent, Trưởng phòng duyệt |

Quy trình thủ công có ba điểm cần xử lý. Kỳ thống kê khác nhau làm lệch so sánh. Số liệu lặp từ cùng nguồn làm tăng mức tin cậy hoặc quy mô giả tạo. Chú trọng quy mô có thể đưa địa bàn có nhu cầu không khớp sản phẩm hoặc vượt khả năng hỗ trợ vào danh sách khảo sát.

Chuyên viên nghiên cứu xác minh bản ghi thiếu, xung đột hoặc lệch kỳ/đơn vị bằng cách kiểm lại nguồn và vị trí đã ghi. Trưởng phòng kiểm tra kết quả áp dụng ngưỡng, xử lý đồng điểm ở ranh giới chọn và duyệt kế hoạch trước khi tiếp cận khách. Bản hiện tại dùng điểm nhị phân theo trọng số và tạm dừng đề xuất khi còn địa bàn chưa rõ khả năng cạnh tranh. Các quy ước này cần được xác nhận theo đề thi.

## Audit nghiệm thu

[Kế hoạch khảo sát DB-02](KE_HOACH_KHAO_SAT_DB02.md) chi tiết hóa nhóm ứng viên từ workbook mẫu, nội dung cần xác minh và phân công đề xuất. Báo cáo Excel phân biệt nhóm ứng viên từ dữ liệu nguồn với nhóm đã có mã hồ sơ trong sheet kế hoạch.

[Kết quả audit giả lập](03_BENCHMARK_AND_VALIDATION/task2_audit/audit.json) lưu kỳ vọng và kết quả thực tế cho ca thông thường, thiếu dữ liệu, ranh giới ngưỡng, mâu thuẫn và bộ mới đổi thứ hạng. Mỗi ca có báo cáo, bảng so sánh và nhật ký thực thi riêng.

---

# Tài liệu tham khảo của gói huấn luyện cũ

Các đường dẫn, mẫu và kết luận minh họa bên dưới thuộc luồng BI cũ. Dùng phần hướng dẫn đầu tài liệu khi chạy Task 2.
## (ANTIGRAVITY AI MASTER REPLICATION & TRAINING MANUAL)

> **Mục tiêu của gói huấn luyện:** Trang bị cho bất kỳ AI Antigravity nào (hoặc các AI Agent lập trình cao cấp) toàn bộ quy chuẩn, tri thức nghiệp vụ, bộ mã nguồn tự động hóa và file mẫu để **sao chép và tái tạo chính xác 100% kết quả**: Làm sạch dữ liệu đa nguồn (Google Sheets, Lark Base, Excel thô) -> Tạo Workbook Excel 10 sheets Native Pivot Tables & Slicers -> Xuất Bảng điều khiển HTML tương tác độc lập -> Soạn thảo Báo cáo Quản trị cấp cao (Word & PDF).

---

## 1. CẤU TRÚC GÓI HUẤN LUYỆN (PACKAGE STRUCTURE)

Toàn bộ gói huấn luyện được đóng gói độc lập trong thư mục `ANTIGRAVITY_AI_TRAINING_PACKAGE` trên Desktop:

```
ANTIGRAVITY_AI_TRAINING_PACKAGE/
│
├── README_TRAINING_MANUAL.md            <-- Tài liệu chỉ dẫn tổng thể này
├── QUICK_START_TEST.ps1                 <-- Script kiểm thử 1-click chạy tự động từ A-Z
│
├── 00_PROMPT_AND_RULES_CONFIG/          <-- Cấu hình luật & Prompt nạp vào AI
│   ├── SYSTEM_PROMPT_INSTRUCTION.md     <-- System Prompt chuẩn để nạp vào AI
│   ├── AGENTS.md                        <-- Bộ luật vĩnh viễn (Agent Rule Standard)
│   ├── GEMINI.md                        <-- Bộ chỉ dẫn thực thi cho Antigravity
│   └── skill/
│       └── bi301-data-pipeline/
│           └── SKILL.md                 <-- Skill chính thức để cài vào Antigravity
│
├── 01_GOLDEN_TEMPLATES/                 <-- Tệp mẫu chuẩn mực & Đặc tả kỹ thuật
│   ├── sample_template.xlsx             <-- File chuẩn gốc BI301 (Table1, 10 sheets, Slicers)
│   ├── BI301_Quy_Chuan_Lam_Sach_Du_Lieu.docx <-- Đặc tả quy chuẩn Word
│   ├── BI301_Quy_Chuan_Lam_Sach_Du_Lieu.pdf  <-- Đặc tả quy chuẩn PDF
│   └── BI301_Data_Cleaning_Template_Standard.md <-- Đặc tả 25 cột & 10 sheets
│
├── 02_CORE_PIPELINE_ENGINES/            <-- Bộ mã nguồn tự động hóa cốt lõi
│   ├── data_pipeline_engine.py          <-- Nạp đa nguồn (GSheets/Lark/File) & Làm sạch 25 cột
│   ├── build_full_pivot_workbook.ps1    <-- Excel COM tạo 10 sheets, Native Pivot & Slicers
│   ├── generate_html_dashboard.py       <-- Sinh HTML Dashboard tương tác độc lập
│   ├── build_integrated_html.py         <-- Sinh Dashboard 5 Tabs tích hợp As-Is/To-Be & MCDA
│   ├── build_full_word_report.py        <-- Sinh Báo cáo Quản trị chuyên sâu 5 chương Word
│   └── export_pdf_and_distribute.ps1    <-- Xuất PDF vector từ Word COM & Phân phối file
│
└── 03_BENCHMARK_DATA_AND_OUTPUTS/       <-- Dữ liệu kiểm chuẩn & Kết quả mẫu chuẩn
    ├── raw_inputs/                      <-- Dữ liệu đầu vào thô cần làm sạch
    │   ├── AI301_De04_Du_Lieu_Mau_1000_Leads.xlsx (1.000 dòng dữ liệu thô bán lẻ/logistics)
    │   └── Nam_Viet_100_Leads_Standardized_v2.xlsx (100 dòng dữ liệu thô chuỗi Mẹ & Bé)
    └── standard_outputs/                <-- Kết quả đầu ra mẫu chuẩn đạt 100% tiêu chí
        ├── AI301_De04_Du_Lieu_Mau_1000_Leads_Cleaned.xlsx (File Excel 10 sheets hoàn chỉnh)
        ├── AI301_Executive_Integrated_Dashboard.html (Dashboard HTML 5 tabs tương tác)
        ├── AI301_Bao_Cao_Nghiep_Vu_Giai_Phap_Toan_Dien.docx (Báo cáo Word 5 chương)
        └── AI301_Bao_Cao_Nghiep_Vu_Giai_Phap_Toan_Dien.pdf (Báo cáo PDF chuẩn in ấn)
```

---

## 2. QUY CHUẨN VÀNG BI301 (THE GOLDEN STANDARDS)

### A. Cấu Trúc 10 Sheets Tiêu Chuẩn Trong File Excel Hoàn Thiện
Bất kỳ file Excel nào được hoàn thiện bởi AI đều phải có đúng 10 sheets sau:
1. `Dữ liệu nguồn `: Chứa dữ liệu sạch 25 cột được đóng gói trong **Excel Table (`Table1`)**.
2. `Doanh thu theo TP`: Pivot Table + Pivot Chart phân tích theo Tỉnh/Thành phố.
3. `Tỷ lệ hài lòng KH`: Pivot Table + Pivot Chart phân tích Điểm hài lòng TB (format `0.0000`).
4. `Tổng hợp Doanh thu `: Pivot Table tóm tắt KPI hệ thống + đếm khách hàng duy nhất (`=COUNTA(UNIQUE(...))`).
5. `Doanh thu theo khu vực `: Pivot Table + Pivot Chart phân tích theo Miền Bắc, Miền Trung, Miền Nam.
6. `Doanh thu theo kênh bán `: Pivot Table + Pivot Chart phân tích theo 3 kênh Omnichannel.
7. `Doanh thu theo phân loại sản ph`: Pivot Table + Pivot Chart theo 4 nhóm ngành hàng chính.
8. `Dash Board`: Executive Dashboard trực quan tổng hợp KPI cards, 7 biểu đồ Pivot Charts và Slicers tương tác.
9. `Doanh thu theo phân khúc KH `: Pivot Table + Pivot Chart theo Khách hàng cá nhân, VIP, B2B.
10. `Doanh thu theo tháng`: Pivot Table + Pivot Chart chuỗi thời gian theo Tháng (`mm/yyyy`).

### B. Quy Chuẩn 25 Cột Dữ Liệu Nguồn (`Table1`)
| STT | Tên Cột | Kiểu Dữ Liệu | Number Format | Công Thức / Quy Tắc Chuẩn Hóa |
|:---:|:---|:---|:---|:---|
| 1 | `Mã order` | Chuỗi | `General` | Mã chuẩn: `CC-ORD-xxxxxx` (viết hoa, không khoảng trắng thừa). |
| 2 | `Ngày ord` | Ngày | `[$-1010000]d/m/yyyy;@` | Định dạng chuẩn ngày/tháng/năm: `d/m/yyyy`. |
| 3 | `Tháng ` | Chuỗi tính toán | `[$-1010000]d/m/yyyy;@` | `=TEXT(B:B, "mm/yyyy")` hoặc `=TEXT([@[Ngày ord]], "mm/yyyy")`. |
| 4 | `Mã KH` | Chuỗi | `General` | Mã khách hàng chuẩn: `KH-M&B-xxxxx`. |
| 5 | `Vùng miền ` | Phân loại | `General` | 3 miền: `Miền Bắc`, `Miền Trung`, `Miền Nam`. |
| 6 | `Thành phố` | Phân loại | `General` | Viết hoa, có dấu chuẩn tiếng Việt (Hà Nội, Cần Thơ, Bắc Ninh, Bình Dương...). |
| 7 | `Phân khúc khách hàng ` | Phân loại | `General` | 3 phân khúc: `Khách hàng cá nhân`, `Thành viên thân thiết (VIP)`, `Khách hàng doanh nghiệp (B2B)`. |
| 8 | `Kênh bán hàng ` | Phân loại | `General` | 3 kênh: `Cửa hàng trực tiếp (In-Store)`, `Website / App Online`, `Sàn TMĐT (Shopee/Lazada/TikTok)`. |
| 9 | `Danh mục nhóm sản phẩm ` | Phân loại | `General` | 4 nhóm: `Tã bỉm & Vệ sinh`, `Sữa & Dinh dưỡng bé`, `Thời trang & Đồ dùng sơ sinh`, `Xe đẩy & Ghế ngồi`. |
| 10 | `Danh mục nhóm sản phẩm con ` | Phân loại | `General` | Đúng theo ngành hàng (Khăn ướt, Tã dán/quần, Sữa bột, Bột ăn dặm, Xe đẩy...). |
| 11 | `Mã SP` | Chuỗi | `General` | Mã SKU: `CC-Pxxxx`. |
| 12 | `Tên sản phẩm ` | Chuỗi | `General` | Tên sản phẩm rõ ràng, kèm quy cách/dung tích. |
| 13 | `Số lượng ` | Số nguyên | `General` | Số lượng mua >= 1. |
| 14 | `Giá niêm yết ` | Tiền tệ | `_-* #,##0\ [$₫-42A]_-;...` | Đơn giá niêm yết chuẩn VND có ký hiệu ₫. |
| 15 | `Chiết khấu ` | Tỷ lệ % | `0%` | Tỷ lệ chiết khấu (0%, 5%, 10%, 15%...). |
| 16 | `Doanh thu gộp ` | Tiền tệ | `_-* #,##0\ [$₫-42A]_-;...` | `= [Số lượng] * [Giá niêm yết]` |
| 17 | `Giá chiết khấu ` | Tiền tệ | `_-* #,##0\ [$₫-42A]_-;...` | Đổi tên từ `Discount_Amount_VND`. `= [Doanh thu gộp] * [Chiết khấu]` |
| 18 | `Doanh thu  thuần ` | Tiền tệ | `_-* #,##0\ [$₫-42A]_-;...` | `= [Doanh thu gộp] - [Giá chiết khấu]` |
| 19 | `Giá vốn hàng bán ` | Tiền tệ | `_-* #,##0\ [$₫-42A]_-;...` | Giá vốn COGS chuẩn VND. |
| 20 | `Lợi nhuận gộp` | Tiền tệ | `_-* #,##0\ [$₫-42A]_-;...` | `= [Doanh thu  thuần ] - [Giá vốn hàng bán ]` |
| 21 | `Biên lợi nhuận gộp ` | Tỷ lệ % | `0.00%` | `=(Table1[[#This Row],[Lợi nhuận gộp]]/Table1[[#This Row],[Doanh thu  thuần ]])*100%` |
| 22 | `Tgian ship(Day)` | Số nguyên | `General` | Số ngày giao hàng (0, 1, 2, 3...). |
| 23 | `Hoàn trả` | Phân loại | `General` | Chuẩn hóa: `Không` hoặc `Có` (không để trống, không viết 0/1). |
| 24 | `Mức độ hài lòng ` | Điểm số | `General` | Thang điểm từ 1 đến 5. |
| 25 | `Phương thức thanh toán ` | Phân loại | `General` | `Tiền mặt / COD`, `Ví MoMo`, `Thẻ tín dụng / Ghi nợ`, `Chuyển khoản ngân hàng`. |

### C. Quy Tắc Native Pivot Tables & Slicers
* **Bắt Buộc Dùng Native Pivot Table:** Không bao giờ tạo bảng tổng hợp bằng văn bản tĩnh hoặc các hàm SUMIF rời rạc khi xử lý dữ liệu lớn.
* **Chung 1 PivotCache:** Tất cả 8 bảng Pivot Tables trên các sheets phải được tạo từ **cùng 1 đối tượng `PivotCache`** trỏ đến `Table1`.
* **Slicers Liên Kết Chéo:** Slicers được tạo trên sheet `Dash Board`. Bằng cách dùng chung `PivotCache`, code có thể gọi:
  ```powershell
  $slicerCache.PivotTables.AddPivotTable($pt)
  ```
  để kết nối 1 Slicer đến toàn bộ các Pivot Tables. Khi người dùng click lọc ở Dashboard, toàn bộ hệ thống biểu đồ và bảng phân tích trên 10 sheets tự động lọc đồng bộ!

---

## 3. MỞ RỘNG NGUỒN VÀO & ĐẦU RA BÁO CÁO HTML

### A. Đa Nguồn Đầu Vào (Multi-Source Inputs)
1. **Google Sheets:**
   * Tự động nhận diện URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/...`
   * Chuyển đổi thành link trích xuất CSV trực tiếp:
     `https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}`
   * Nạp trực tiếp vào `pandas.read_csv()`.
2. **Lark Base (Bitable):**
   * Hỗ trợ đọc qua Lark Open API (`https://open.larksuite.com/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records`) hoặc xuất link bảng công khai.
3. **File Cục Bộ:**
   * Tự động quét file mới nhất trong thư mục `C:\Users\PC\Downloads\` và `C:\Users\PC\OneDrive\Desktop\`.

### B. Đầu Ra Bảng Điều Khiển HTML Tương Tác Độc Lập
* **Độc Lập Hoàn Toàn:** Không cần máy chủ web (Node.js, Flask, Apache). Người dùng chỉ cần nhấp đúp file `.html` là mở ngay trên Microsoft Edge hoặc Chrome.
* **Giao Diện Hiện Đại:** Sử dụng Tailwind CSS, Google Fonts (`Plus Jakarta Sans`), Chart.js.
* **Tích Hợp Slicers Thời Gian Thực:** Lọc theo Vùng miền, Trạng thái (Đạt/Loại), Dòng sản phẩm.
* **Bảng Dữ Liệu Thông Minh:** Live Search tìm kiếm tức thì mọi cột, phân trang động (15/25/50 dòng), nút **Export CSV sạch**.
* **5 Tabs Tích Hợp Nghiệp Vụ:**
  * Tab 1: Executive Dashboard (KPI Cards & 7 Biểu đồ tự động cập nhật).
  * Tab 2: Phân Tích Nghiệp Vụ & Workflow Lỗi (Hồ sơ Hưng Phát WMS, 7 vấn đề cốt lõi, so sánh As-Is vs To-Be).
  * Tab 3: Ma Trận Chấm Điểm MCDA (Trọng số 4 tiêu chí & xếp hạng 5 phân vùng thị trường).
  * Tab 4: Kế Hoạch 20 Chuỗi Thực Địa (Chiến dịch Go-To-Market tại TP.HCM & Miền Nam).
  * Tab 5: Bảng Dữ Liệu 1.000 Leads (Tra cứu, phân trang, lọc và xuất CSV).

---

## 4. KHUNG PHÂN TÍCH NGHIỆP VỤ QUẢN TRỊ TÍCH HỢP (WORD & PDF)

Khi biên soạn báo cáo phân tích quản trị, AI cần tích hợp đầy đủ khung nghiệp vụ sau:
* **Hồ Sơ Doanh Nghiệp:** Công ty Cổ phần Công nghệ & Giải pháp WMS Hưng Phát (Quận 1, TP.HCM). Cung cấp 3 gói giải pháp: WMS Cloud Standard, WMS Pro Enterprise, WMS Quản lý Hạn dùng & Date. Khách hàng mục tiêu: Chuỗi bán lẻ 5 - 50 cửa hàng, 2 - 6 tổng kho.
* **7 Vấn Đề Cốt Lõi:**
  1. 202 leads vi phạm SLA on-site <= 2h (khoảng cách 500 - 900km).
  2. 200 leads sai phân khúc sản phẩm (DB-04 là sản xuất thô/cảng biển).
  3. 78 leads trùng lặp; 114 leads dùng số liệu cũ năm 2021.
  4. 145 số điện thoại lỗi; 92 email không tồn tại.
  5. Lệch pha khả năng chi trả giữa các vùng miền.
  6. Thiếu bộ tiêu chí định lượng chấm điểm leads (MCDA).
  7. Lãng phí 40% nguồn lực đội ngũ Sales và Kỹ thuật.
* **Workflow Lỗi Hiện Tại (As-Is):**
  * *Chủ thể:* Chuyên viên nghiên cứu thị trường & BDE.
  * *Bản chất:* 100% thủ công bằng tay, copy-paste từ web vào Excel không có ràng buộc dữ liệu.
  * *Đứt gãy bàn giao (Broken Handoff):* Chuyển trực tiếp dữ liệu rác sang Sales/Kỹ thuật mà không qua bộ lọc Gating Filter kỹ thuật.
* **Quy Trình Chuẩn Hóa Mới (To-Be 4 Bước):**
  * *Bước 1:* Data Cleaning & Standardization.
  * *Bước 2:* Operational Gating Filter (Loại bỏ 402 leads vi phạm).
  * *Bước 3:* MCDA Scoring Matrix (Trọng số: 35% Product Fit, 30% SLA Feasibility, 20% Competition, 15% Scale).
  * *Bước 4:* Board Approval & 20 Selected Leads Field Survey.

---

## 5. BÍ QUYẾT KỸ THUẬT & XỬ LÝ LỖI (GOTCHAS FOR AI)

Bất kỳ AI nào vận hành trên hệ điều hành Windows và môi trường Antigravity Sandbox cần nắm vững các nguyên tắc sau:
1. **Quyền Truy Cập Excel COM / Word COM:**
   * Môi trường Sandbox chuẩn chặn gọi COM server của Microsoft Office (`E_ACCESSDENIED 0x80070005`).
   * *Giải pháp:* Khi chạy script PowerShell điều khiển Excel COM (`build_full_pivot_workbook.ps1`) hoặc Word COM (`export_pdf_and_distribute.ps1`), AI phải chạy với quyền `BypassSandbox: true`. Các bước tính toán bằng Python thì giữ nguyên `BypassSandbox: false`.
2. **Lỗi Mảng PowerShell Khi Gán Dữ Liệu Lớn (Array Unrolling):**
   * Trong PowerShell, khi gán mảng 2 chiều vào Excel Range, PowerShell thường unroll mảng 1 dòng thành giá trị vô hướng (scalar), dẫn đến lỗi `InvalidCastException: System.Double to System.String`.
   * *Giải pháp:* Sao chép trực tiếp qua trung gian tệp hoặc dùng hàm `$range.Value2 = $data` có bọc đúng kiểu `[object[,]]`.
3. **Format Tiền Tệ Kế Toán Tiếng Việt Trong Excel:**
   * Định dạng chuẩn kế toán VND:
     `_-* #,##0\ [$₫-42A]_-;\-* #,##0\ [$₫-42A]_-;_-* "-"\ [$₫-42A]_-;_-@_-`
4. **Liên Kết Slicers Với Nhiều Pivot Tables:**
   * Để 1 Slicer điều khiển được nhiều Pivot Table, tất cả các Pivot Table đó **bắt buộc phải cùng chia sẻ chung 1 `PivotCache`**. Không được tạo `PivotCache` riêng lẻ cho từng bảng.

---

## 6. HƯỚNG DẪN NẠP VÀO MỘT AI ANTIGRAVITY MỚI (DEPLOYMENT)

Để trang bị năng lực này cho một AI Antigravity khác:
1. **Cách 1 - Cài đặt Skill:**
   * Sao chép thư mục `00_PROMPT_AND_RULES_CONFIG/skill/bi301-data-pipeline/` vào thư mục `skills/` của workspace hoặc user (`~/.gemini/antigravity/builtin/skills/`).
   * AI sẽ tự động kích hoạt skill `bi301-data-pipeline` khi người dùng yêu cầu xử lý file.
2. **Cách 2 - Nạp qua AGENTS.md / GEMINI.md:**
   * Sao chép trực tiếp 2 tệp `AGENTS.md` và `GEMINI.md` trong thư mục `00_PROMPT_AND_RULES_CONFIG/` vào thư mục gốc của workspace làm việc mới.
   * AI sẽ tuân thủ tuyệt đối quy chuẩn này trong mọi tác vụ.
3. **Chạy Thử Nghiệm Kiểm Chuẩn (Verification):**
   * Mở PowerShell tại thư mục gói và chạy:
     ```powershell
     powershell -ExecutionPolicy Bypass -File QUICK_START_TEST.ps1
     ```
   * Hệ thống sẽ tự động chạy toàn bộ pipeline trên file dữ liệu mẫu 1.000 leads và xuất bản đầy đủ 4 tệp đầu ra để kiểm chứng chất lượng.

