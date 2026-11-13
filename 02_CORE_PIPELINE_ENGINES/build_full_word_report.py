import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

doc = Document()

# Set page margins
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Palette
NAVY_PRIMARY = RGBColor(27, 54, 93)     # #1B365D
SLATE_BLUE = RGBColor(46, 91, 136)      # #2E5B88
TEXT_DARK = RGBColor(30, 41, 59)        # #1E293B
TEXT_MUTED = RGBColor(100, 116, 139)    # #64748B
CRIMSON_RED = RGBColor(185, 28, 28)     # #B91C1C
EMERALD_GREEN = RGBColor(4, 120, 87)    # #047857

HEX_HEADER_BG = "1B365D"
HEX_ROW_ALT = "F8FAFC"
HEX_BORDER = "CBD5E1"

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

# Title
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(4)
r_title = p_title.add_run("BÁO CÁO PHÂN TÍCH TOÀN DIỆN VỀ BỐI CẢNH DOANH NGHIỆP, NGUYÊN NHÂN LỖI WORKFLOW & ĐỀ XUẤT GIẢI PHÁP TỐI ƯU")
r_title.font.name = "Segoe UI"
r_title.font.size = Pt(15)
r_title.font.bold = True
r_title.font.color.rgb = NAVY_PRIMARY

# Subtitle
p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
r_sub = p_sub.add_run("Nghiên cứu điển hình Công ty Cổ phần Giải pháp WMS Hưng Phát trên tập dữ liệu 1.000 hồ sơ khảo sát\n(Tài liệu tích hợp theo chuẩn đặc tả nghiệp vụ AI301)")
r_sub.font.name = "Segoe UI"
r_sub.font.size = Pt(10)
r_sub.font.italic = True
r_sub.font.color.rgb = TEXT_MUTED

# Divider
p_div = doc.add_paragraph()
p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_div.paragraph_format.space_after = Pt(12)
r_div = p_div.add_run("—" * 60)
r_div.font.color.rgb = RGBColor(203, 213, 225)

def add_sec_heading(title):
    h = doc.add_heading(level=1)
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    r = h.add_run(title)
    r.font.name = "Segoe UI"
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = NAVY_PRIMARY
    return h

def add_p(text, bold_prefix=None, space_after=5, italic=False, color=TEXT_DARK):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Segoe UI"
        rb.font.size = Pt(9.5)
        rb.font.bold = True
        rb.font.color.rgb = SLATE_BLUE
    r = p.add_run(text)
    r.font.name = "Segoe UI"
    r.font.size = Pt(9.5)
    r.font.italic = italic
    r.font.color.rgb = color
    return p

# -----------------------------------------------------------------
# PHẦN I: HỒ SƠ DOANH NGHIỆP
# -----------------------------------------------------------------
add_sec_heading("PHẦN I. HỒ SƠ DOANH NGHIỆP: CÔNG TY LÀ AI, KINH DOANH GÌ, KHÁCH HÀNG LÀ AI?")

add_p(
    "Từ dữ liệu 1.000 hồ sơ khảo sát (AI301_De04_Du_Lieu_Mau_1000_Leads.xlsx), Công ty Hưng Phát là doanh nghiệp công nghệ giải pháp B2B có trụ sở chính tại TP. Hồ Chí Minh. Năng lực cốt lõi của công ty là nghiên cứu, phát triển và triển khai hệ thống Quản lý kho hàng thông minh (Warehouse Management System - WMS). Đội ngũ kỹ sư triển khai và hỗ trợ vận hành có chuyên môn sâu nhưng bị ràng buộc bởi định biên nhân sự giới hạn, chỉ đủ sức gánh vác duy nhất một đợt mở rộng địa bàn tập trung.",
    bold_prefix="1. Bản chất doanh nghiệp (Công ty Hưng Phát là công ty gì?): "
)

add_p(
    "Hưng Phát không kinh doanh hàng hóa tiêu dùng bán lẻ, mà kinh doanh các gói giải pháp phần mềm quản trị chuỗi cung ứng và kho bãi, bao gồm 3 phân hệ chủ lực:\n"
    "• Hưng Phát WMS Cloud Standard (382 leads quan tâm, chiếm 38.2%): Gói đám mây tiêu chuẩn dành cho chuỗi bán lẻ quy mô vừa và nhỏ, tối ưu tốc độ triển khai và chi phí đầu tư ban đầu.\n"
    "• Hưng Phát WMS Pro Enterprise (288 leads quan tâm, chiếm 28.8%): Gói giải pháp toàn diện cho các tập đoàn bán lẻ lớn, hỗ trợ đa trung tâm phân phối (Multi-DC), tích hợp phần cứng tự động hóa.\n"
    "• Hưng Phát WMS Cloud Standard - Quản lý Hạn/Date (130 leads quan tâm, chiếm 13.0%): Phân hệ chuyên biệt quản lý nghiêm ngặt lô hàng (Lot/Batch) và vòng đời hạn sử dụng (FEFO/FIFO).",
    bold_prefix="2. Danh mục mặt hàng / giải pháp kinh doanh (Rút ra từ dữ liệu đầu vào): "
)

add_p(
    "Khách hàng mục tiêu của Hưng Phát là các Chuỗi bán lẻ đa điểm (Retail Chains) hiện đại, sở hữu mạng lưới từ 5 đến 50 cửa hàng và vận hành từ 2 đến 6 kho trung chuyển/trung tâm phân phối. Cụ thể bao gồm:\n"
    "• Chuỗi Siêu thị mini & Tiện lợi (117 chuỗi).\n"
    "• Chuỗi Siêu thị mini & Bán lẻ Du lịch (111 chuỗi).\n"
    "• Chuỗi Bán lẻ Nông sản & Thực phẩm tươi (108 chuỗi).\n"
    "• Chuỗi Cung ứng Thực phẩm & Nhà hàng Khách sạn F&B (84 chuỗi).\n"
    "• Chuỗi Thời trang & Phụ kiện (70 chuỗi), Chuỗi Nhà thuốc & Dược phẩm Tây Nam Bộ (64 chuỗi).\n"
    "Dữ liệu khẳng định các Hộ kinh doanh tạp hóa cá thể (70 hộ) và Đại lý thu mua nông sản truyền thống thô sơ (100 đại lý cà phê, tiêu) hoàn toàn không phải khách hàng mục tiêu do không có quy trình WMS.",
    bold_prefix="3. Khách hàng mục tiêu là những ai?: "
)

# -----------------------------------------------------------------
# PHẦN II: VẤN ĐỀ VÀ NGUYÊN NHÂN LỖI WORKFLOW
# -----------------------------------------------------------------
add_sec_heading("PHẦN II. CÁC VẤN ĐỀ DOANH NGHIỆP ĐANG GẶP PHẢI & PHÂN TÍCH WORKFLOW BỊ LỖI")

add_p(
    "Qua rà soát và kiểm toán 1.000 hồ sơ khảo sát, Công ty Hưng Phát đang đối mặt với 7 vấn đề cốt lõi dẫn đến nguy cơ thất bại khi mở rộng thị trường:\n"
    "1. Giới hạn nghiêm ngặt về năng lực thực thi: Đội ngũ kỹ sư tại TP.HCM chỉ đủ đáp ứng duy nhất 1 đợt mở rộng; nếu dàn trải sang cả 4 địa bàn (Đông Nam Bộ, ĐBSCL, Nam Trung Bộ, Tây Nguyên) sẽ lập tức vỡ trận vận hành.\n"
    "2. Quy trình làm việc tự phát, phân tán: Nhân viên tự đọc báo cáo thị trường, tự tìm kiếm thông tin và tự ghép danh sách khách hàng tiềm năng không theo bất kỳ chuẩn mực thống nhất nào.\n"
    "3. Dữ liệu không đồng nhất về thời gian: Trộn lẫn số liệu cũ năm 2021 (200 leads Tây Nguyên), 9T/2023 (134 leads Nam Trung Bộ) với số liệu 2024, gây sai lệch nghiêm trọng khi so sánh ngang hàng.\n"
    "4. Dữ liệu bị trùng lặp và thiếu tính độc lập: 100% hồ sơ tại Tây Nguyên (200 bản ghi) bị sao chép từ cùng một nguồn cũ, tạo ra quy mô thị trường ảo.\n"
    "5. Đánh giá sai lệch trọng tâm thị trường: Nhân viên bị đánh lừa bởi quy mô doanh thu hàng nghìn tỷ của các đại lý nông sản thô mà bỏ qua việc họ không có nhu cầu về giải pháp WMS.\n"
    "6. Bất cân xứng giữa kỳ vọng khách hàng và khả năng cung ứng: 202 chuỗi bán lẻ tại Nam Trung Bộ (Đà Nẵng, Khánh Hòa) yêu cầu bắt buộc On-site SLA <= 2h và trực đêm 24/7, vượt quá năng lực phục vụ của đội ngũ tại TP.HCM cách xa 500-900km.\n"
    "7. Thiếu tính minh bạch và khả năng kiểm chứng: Thiếu mã định danh truy xuất nguồn gốc (Audit Trail), khiến cấp quản lý không thể kiểm tra chéo độ tin cậy của thông tin.",
    bold_prefix="1. Bóc tách 7 vấn đề cốt lõi từ dữ liệu: "
)

add_p(
    "Nguyên nhân gốc rễ xuất phát từ việc quy trình làm việc hiện tại (Workflow As-Is) được thực hiện hoàn toàn thủ công bởi con người mà thiếu sự kiểm soát của hệ thống và bộ lọc tự động:\n"
    "• Tác nhân thực hiện (Ai làm?): Chuyên viên Nghiên cứu thị trường và Nhân viên Phát triển Kinh doanh tự tìm nguồn và tự nhập liệu bằng tay.\n"
    "• Công cụ sử dụng: File bảng tính Excel thô sơ, không cài đặt ràng buộc dữ liệu (Data Validation) hay bộ lọc cắt ngưỡng (Gating Filter).\n"
    "• Lỗi tại khâu chuyển giao: Bộ phận kinh doanh không tham vấn ý kiến kỹ thuật của Đội triển khai về năng lực đáp ứng SLA trước khi đưa khách hàng vào danh sách tiềm năng.\n"
    "• Hậu quả thực tế: Ban Giám Đốc suýt nữa phê duyệt ngân sách hàng tỷ đồng để khảo sát thị trường Tây Nguyên (nơi 100% khách hàng không có nhu cầu WMS) và thị trường Đà Nẵng (nơi 87.8% khách hàng đòi hỏi hỗ trợ tại chỗ bất khả thi).",
    bold_prefix="2. Khai thác nguyên nhân gốc rễ và Workflow bị lỗi (Workflow As-Is): "
)

# -----------------------------------------------------------------
# PHẦN III: ĐỀ XUẤT GIẢI PHÁP TỐI ƯU
# -----------------------------------------------------------------
add_sec_heading("PHẦN III. ĐỀ XUẤT CÁC GIẢI PHÁP ƯU TIÊN VÀ GIẢI PHÁP DÀI HẠN")

add_p(
    "Để tối ưu hóa nguồn lực có hạn và loại bỏ ngay lập tức các rủi ro chết người, Hưng Phát cần thực hiện ngay 3 giải pháp ưu tiên cao nhất:\n\n"
    "• GIẢI PHÁP 1: Thiết lập và kích hoạt ngay Bộ lọc cắt ngưỡng vận hành (Operational Gating Filter)\n"
    "Chạy 2 chốt chặn tự động trên toàn bộ dữ liệu: (1) Loại bỏ 202 hồ sơ tại DB-03 đòi hỏi On-site SLA <= 2h cách xa TP.HCM; (2) Loại bỏ 200 hồ sơ tại DB-04 là đại lý nông sản thô và dữ liệu sao chép cũ 2021. Hành động này giúp công ty tiết kiệm 100% ngân sách khảo sát lãng phí.\n\n"
    "• GIẢI PHÁP 2: Quyết định mở rộng tập trung vào Cực tăng trưởng số 1 - Đông Nam Bộ (DB-01) (Hạng 1 MCDA: 4.70/5.0)\n"
    "Thị trường nằm trong bán kính vàng < 100km (Bình Dương, Đồng Nai, Bà Rịa - Vũng Tàu), 100% hồ sơ (320/320) đạt tiêu chuẩn Gating, doanh thu chuỗi đạt 72.883 tỷ ₫, ngân sách sẵn sàng chi trả WMS đạt 93.18 tỷ ₫. Đội ngũ kỹ thuật có thể di chuyển bằng đường bộ xử lý sự cố trong 3-4h dễ dàng.\n\n"
    "• GIẢI PHÁP 3: Mở rộng đồng hành Cực tăng trưởng số 2 - ĐBSCL (DB-02) (Hạng 2 MCDA: 4.28/5.0)\n"
    "Thị trường miền Tây (Cần Thơ, Tiền Giang, An Giang) có mức độ cạnh tranh rất thấp (4.5/5), 250 chuỗi thực phẩm sạch và nhà thuốc khớp 100% gói giải pháp WMS Quản lý Hạn/Date. Áp dụng mô hình Hybrid: On-site hỗ trợ 2-3 ngày Go-live đầu tiên, sau đó vận hành qua Remote Helpdesk cam kết SLA 30 phút.",
    bold_prefix="1. Các giải pháp ưu tiên hàng đầu (Tối ưu nguồn lực & Khắc phục khẩn cấp): "
)

add_p(
    "Sau khi chốt xong 2 thị trường trọng điểm, Hưng Phát cần triển khai các giải pháp trung và dài hạn để hoàn thiện tổ chức:\n"
    "• Giải pháp dài hạn cho Duyên hải Miền Trung (DB-03): Chỉ xem xét mở rộng thị trường này trong giai đoạn 2 khi công ty đã tích lũy đủ ngân sách để thành lập 'Hub Hỗ trợ Kỹ thuật Vùng tại Đà Nẵng' (đảm bảo cự ly đáp ứng SLA <= 2h).\n"
    "• Giải pháp dài hạn cho Tây Nguyên (DB-04): Chuyển giao các nhu cầu ghi chép đơn giản cho đối tác phần mềm kế toán, đồng thời nghiên cứu phân hệ 'WMS Nông sản xuất khẩu' tinh gọn trước khi tái tiếp cận thị trường này.\n"
    "• Tự động hóa Pipeline dữ liệu đa nguồn: Ứng dụng quy trình tiếp nhận và làm sạch tự động từ Google Sheets, Lark Base và Excel (như hệ sinh thái đã xây dựng) để triệt tiêu vĩnh viễn lỗi làm việc tự phát của nhân viên.",
    bold_prefix="2. Các giải pháp giải quyết những vấn đề còn lại: "
)

# -----------------------------------------------------------------
# PHẦN IV: QUY TRÌNH TRIỂN KHAI TỔNG QUAN 4 BƯỚC
# -----------------------------------------------------------------
add_sec_heading("PHẦN IV. QUY TRÌNH TRIỂN KHAI 4 BƯỚC CHUẨN HÓA (WORKFLOW TO-BE)")

add_p("Quy trình chuẩn hóa 4 bước khép kín thay thế hoàn toàn cách làm việc tự phát, đảm bảo tính minh bạch, có thể kiểm toán chéo và loại bỏ 100% rủi ro vận hành:")

steps_data = [
    ("Bước 1: Làm sạch & Chuẩn hóa dữ liệu nghiên cứu (Data Cleansing & Standardization)",
     "• Khử trùng lặp (Deduplication): Loại bỏ bản ghi sao chép chung nguồn.\n• Đồng nhất mốc thời gian (Time Alignment): Quy chuẩn toàn bộ về năm tài chính 2024.\n• Gắn mã định danh (Tagging & Citation): Cấp mã duy nhất REC-xxxx phục vụ kiểm toán chéo.",
     "Chuyên viên Nghiên cứu thị trường lập bảng; Trưởng nhóm thẩm định.",
     "Bảng 1.000 hồ sơ sạch, đồng bộ và Sổ tay truy vết nguồn (Audit Log)."),
     
    ("Bước 2: Sàng lọc sơ bộ theo ngưỡng khả thi vận hành (Operational Gating Filter)",
     "• Đánh giá khớp sản phẩm (Product Fit Check): Loại bỏ khách hàng lệch WMS.\n• Bộ lọc cắt ngưỡng vận hành (Go/No-Go Gate): Loại bỏ địa bàn đòi hỏi On-site SLA <= 2h vượt trần năng lực công ty.",
     "Trưởng nhóm Triển khai Kỹ thuật phối hợp Chuyên viên Kinh doanh đánh giá; Trưởng phòng Kinh doanh duyệt.",
     "Biên bản đánh giá tính khả thi vận hành, xác định 598 hồ sơ PASS và 402 hồ sơ LOẠI BỎ."),
     
    ("Bước 3: Chấm điểm Ma trận đánh giá đa tiêu chí (MCDA Scoring)",
     "• Thiết lập trọng số 4 nhóm trụ cột: (1) Khớp nhu cầu WMS: 35%; (2) Khả thi triển khai: 30%; (3) Cạnh tranh: 20%; (4) Quy mô chuỗi: 15%.\n• Tính điểm số tổng hợp và xếp thứ tự ưu tiên của 4 địa bàn.",
     "Chuyên viên Kinh doanh tính toán bảng tính; Trưởng phòng Kinh doanh kiểm soát và chốt điểm số.",
     "Bảng ma trận chấm điểm MCDA hoàn chỉnh: Top 1 Đông Nam Bộ (4.70/5), Top 2 ĐBSCL (4.28/5)."),
     
    ("Bước 4: Lập Báo cáo đề xuất lựa chọn & Kế hoạch khảo sát thực địa",
     "• Lập Tờ trình đề xuất lựa chọn 2 địa bàn hạt nhân DB-01 và DB-02.\n• Thiết kế Kế hoạch khảo sát thực địa: Chọn mẫu hạt nhân 20 chuỗi tiêu biểu (Top 10 DB-01 và Top 10 DB-02).\n• Xây dựng bảng hỏi phỏng vấn sâu và xác định tiêu chí nghiệm thu PoC/MOU.",
     "Trưởng phòng Kinh doanh ký trình; Trưởng phòng Triển khai đồng ký xác nhận năng lực; Ban Giám Đốc phê duyệt.",
     "Tờ trình Ban Giám Đốc và Bản kế hoạch khảo sát thực địa 20 chuỗi bán lẻ hạt nhân.")
]

t_steps = doc.add_table(rows=len(steps_data) + 1, cols=4)
t_steps.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_steps)

t_steps_headers = ["Quy Trình & Tên Bước", "Nội Dung Công Việc Chi Tiết", "Bộ Phận & Trách Nhiệm", "Đầu Ra (Deliverables)"]
t_steps_widths = [Inches(1.8), Inches(2.7), Inches(1.5), Inches(1.8)]

hdr_cells = t_steps.rows[0].cells
for i, name in enumerate(t_steps_headers):
    hdr_cells[i].text = name
    set_cell_background(hdr_cells[i], HEX_HEADER_BG)
    set_cell_margins(hdr_cells[i], top=120, bottom=120, left=100, right=100)
    p = hdr_cells[i].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
    for r in p.runs:
        r.font.name = "Segoe UI"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

for r_idx, row_data in enumerate(steps_data, 1):
    row_cells = t_steps.rows[r_idx].cells
    bg = HEX_ROW_ALT if r_idx % 2 == 1 else "FFFFFF"
    for c_idx, val in enumerate(row_data):
        row_cells[c_idx].text = val
        set_cell_background(row_cells[c_idx], bg)
        set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=100, right=100)
        p = row_cells[c_idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [2] else WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY_PRIMARY

for row in t_steps.rows:
    for i, w in enumerate(t_steps_widths):
        row.cells[i].width = w

# Output save
output_docx = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "AI301_Bao_Cao_Nghiep_Vu_Giai_Phap_Toan_Dien.docx")
doc.save(output_docx)
print(f"SUCCESS: Saved comprehensive report to {output_docx}")

