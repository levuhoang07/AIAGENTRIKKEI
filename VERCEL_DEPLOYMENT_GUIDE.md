# HƯỚNG DẪN TRIỂN KHAI NỀN TẢNG WEB LÊN VERCEL
## Hệ Thống Thẩm Định Dữ Liệu & Đánh Giá Thị Trường Mở Rộng WMS (AI301 - Đề Số 04)

Tài liệu này cung cấp toàn bộ quy trình từ kiểm thử cục bộ, đưa mã nguồn lên GitHub, đến việc cấu hình triển khai hoàn toàn tự động lên nền tảng đám mây **Vercel** để hệ thống vận hành online 24/7.

---

### 1. Kiến Trúc Vận Hành Trên Vercel

```
                                  +------------------------------------+
                                  |         NGƯỜI DÙNG TRUY CẬP        |
                                  |    https://hungphat-wms.vercel.app  |
                                  +-----------------+------------------+
                                                    |
                                                    v
                                      +-------------+-------------+
                                      |    VERCEL GLOBAL EDGE     |
                                      +-------------+-------------+
                                                    |
                       +----------------------------+----------------------------+
                       | (Static Asset / CDN)                                    | (API Call / Serverless)
                       v                                                         v
          +------------+------------+                              +-------------+-------------+
          |      public/index.html   |                              |         api/index.py        |
          |  (Giao diện SaaS Mockup  |                              |  (FastAPI Serverless Engine)|
          |    Tailwind + Chart.js)  |                              +-------------+-------------+
          +-------------------------+                                            |
                                                                   +-------------+-------------+
                                                                   |  STRICT SCHEMA GATE (26C) |
                                                                   |   - Check 26 cột bắt buộc |
                                                                   |   - Lọc Gating SLA & WMS  |
                                                                   |   - Tính toán MCDA Top 2  |
                                                                   +---------------------------+
```

* **Frontend (Edge CDN):** Tệp `public/index.html` được phân phối qua CDN toàn cầu của Vercel, thời gian tải trang < 100ms.
* **Backend (Serverless Function):** Tệp `api/index.py` chạy trên Python Runtime của Vercel. Tiếp nhận dữ liệu phân tích, xử lý 100% trong RAM qua `io.BytesIO` (không ghi đĩa vật lý), đảm bảo tuân thủ cơ chế Read-Only Filesystem của Serverless.
* **Định tuyến (`vercel.json`):** Điều hướng mọi request `/api/*` về `api/index.py`, các tệp tĩnh còn lại phục vụ trực tiếp từ `public/`.

---

### 2. Các Tệp Cốt Lõi Phục Vụ Deploy

| Tệp / Thư mục | Vai trò trong hệ thống |
| :--- | :--- |
| `vercel.json` | Cấu hình router serverless và static rewrite cho Vercel. |
| `requirements.txt` | Khai báo các thư viện Python: `fastapi`, `pandas`, `openpyxl`, `python-multipart`, `numpy`. |
| `api/index.py` | Entrypoint serverless chứa toàn bộ logic API và xử lý dữ liệu. |
| `api/default_data.json` | Bộ nhớ đệm phân tích sẵn giúp Vercel phản hồi lần đầu trong 5ms (tránh trễ cold-start). |
| `public/index.html` | Giao diện Web Dashboard SaaS chuẩn UX/UI theo thiết kế mẫu. |
| `public/AI301_De04_Master_1000_Leads.xlsx` | File Excel mẫu 1.000 leads phục vụ người dùng tải về trực tiếp. |
| `.gitignore` | Loại trừ các thư mục cache, môi trường ảo và tệp rác khi đẩy lên Git. |

---

### 3. Quy Trình 3 Bước Triển Khai Lên Vercel

#### Bước 1: Khởi tạo Git và Đẩy Mã Nguồn Lên GitHub

Mở terminal (PowerShell hoặc Git Bash) tại thư mục dự án `d:\antigravity\Bai-tap-giua-ki` và chạy các lệnh sau:

```bash
# 1. Khởi tạo Git repository cục bộ
git init

# 2. Thêm toàn bộ mã nguồn vào staging
git add .

# 3. Tạo commit đầu tiên
git commit -m "feat: complete hung phat wms market analytics platform for vercel"

# 4. Đổi tên nhánh chính thành main
git branch -M main

# 5. Liên kết với kho chứa GitHub của bạn (Thay URL bên dưới bằng URL repo của bạn)
git remote add origin https://github.com/<TEN_GITHUB_CUA_BAN>/<TEN_REPO_CUA_BAN>.git

# 6. Đẩy mã nguồn lên GitHub
git push -u origin main
```

#### Bước 2: Kết Nối và Deploy Trên Vercel

1. Truy cập [https://vercel.com](https://vercel.com) và đăng nhập (khuyên dùng tài khoản GitHub).
2. Tại màn hình Dashboard Vercel, bấm nút **"Add New..."** $\rightarrow$ chọn **"Project"**.
3. Chọn kho chứa GitHub bạn vừa tạo ở Bước 1 và bấm **"Import"**.
4. Cấu hình triển khai:
   * **Project Name:** Đặt tên mong muốn (ví dụ: `hungphat-wms-market-analytics`).
   * **Framework Preset:** Giữ mặc định `Other`.
   * **Root Directory:** Giữ mặc định `./`.
   * **Build and Output Settings:** Không cần thay đổi gì (Vercel tự động nhận diện `vercel.json`).
5. Bấm nút **"Deploy"**.

#### Bước 3: Hoàn Tất & Kiểm Tra Hoạt Động Online

* Quá trình build và provision serverless function của Vercel thường mất khoảng **30 - 50 giây**.
* Khi màn hình hiển thị lời chúc mừng **"Congratulations!"**, bạn sẽ nhận được đường dẫn web chính thức dạng:
  👉 `https://hungphat-wms-market-analytics.vercel.app`
* Bấm vào đường dẫn để trải nghiệm trực tiếp hệ thống.

---

### 4. Kịch Bản Kiểm Thử Sau Khi Deploy Thành Công

1. **Kiểm tra tải trang ban đầu:**
   * Mở website $\rightarrow$ Toàn bộ 7 card phân tích số liệu, biểu đồ spline, gauge phân loại SLA và bảng xếp hạng Top 2 (`DB-01: 4.70`, `DB-02: 4.28`) hiển thị ngay tức thì.
2. **Kiểm tra tính năng Tìm kiếm Live:**
   * Gõ thử vào ô tìm kiếm ở góc trên: `Điện máy`, `REC-0015`, hoặc `DB-01` $\rightarrow$ Bảng tự động lọc theo thời gian thực.
3. **Kiểm tra tính năng Tải File Mẫu:**
   * Bấm nút **"Tải Tệp Mẫu 1.000 Leads"** trên Sidebar $\rightarrow$ Trình duyệt tải ngay file `.xlsx` chuẩn 10 sheets.
4. **Kiểm tra Chốt Chặn Dữ Liệu Nghiêm Ngặt (Strict Schema Gate):**
   * Kéo thả một file Excel bất kỳ hoặc file thiếu cột vào màn hình $\rightarrow$ Hệ thống tự động chặn lại với mã **HTTP 422**, hiện Modal cảnh báo màu đỏ liệt kê cụ thể các cột bị thiếu, không làm sai lệch số liệu phân tích.
5. **Kiểm tra Nạp File Hợp Lệ:**
   * Kéo thả file `AI301_De04_Master_1000_Leads.xlsx` vào trang $\rightarrow$ Toàn bộ biểu đồ và chỉ số tự động được tính toán lại trong 0.3 giây kèm thông báo thành công.

---

### 5. Chạy Kiểm Thử Cục Bộ Trước Khi Deploy (Local Development)

Nếu muốn kiểm tra hoặc chỉnh sửa cục bộ trên máy tính trước khi đẩy lên GitHub:

* **Cách 1 (Khuyên dùng):** Bấm đúp chuột vào file `START_WEB_DASHBOARD.ps1` trong thư mục gốc. Script sẽ tự động bật máy chủ FastAPI và mở trình duyệt tại `http://127.0.0.1:8000`.
* **Cách 2:** Chạy trực tiếp qua dòng lệnh:
  ```bash
  python 02_CORE_PIPELINE_ENGINES/web_server.py
  ```
  hoặc:
  ```bash
  python -m uvicorn api.index:app --host 127.0.0.1 --port 8000 --reload
  ```

