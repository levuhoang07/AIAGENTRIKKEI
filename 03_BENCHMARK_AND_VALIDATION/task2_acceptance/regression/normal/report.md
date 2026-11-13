# Đề xuất khảo sát thị trường

Kính gửi Trưởng phòng Phát triển Kinh doanh

Địa bàn đề xuất — A, B

## Bảng so sánh

| Địa bàn | Tiêu chí | Dữ kiện gốc và căn cứ | Quy tắc | Đánh giá của Agent | Điểm |
|---|---|---|---|---|---|
| A | criterion_1 | 1 flag (SYNTHETIC-A-market, fixture, row 1, facts.json#1) | >= 1 | pass | 1 |
| A | criterion_2 | 1 flag (SYNTHETIC-A-market, fixture, row 1, facts.json#1) | >= 1 | pass | 1 |
| A | criterion_3 | 1 flag (SYNTHETIC-A-market, fixture, row 1, facts.json#1) | >= 1 | pass | 1 |
| A | criterion_4 | 1 flag (SYNTHETIC-A-market, fixture, row 1, facts.json#1) | >= 1 | pass | 1 |
| A | hours | 1 h (SYNTHETIC-A-capacity, fixture, row 1, facts.json#5) | <= 2 | pass | 1 |
| B | criterion_1 | 1 flag (SYNTHETIC-B-market, fixture, row 1, facts.json#6) | >= 1 | pass | 1 |
| B | criterion_2 | 1 flag (SYNTHETIC-B-market, fixture, row 1, facts.json#6) | >= 1 | pass | 1 |
| B | criterion_3 | 1 flag (SYNTHETIC-B-market, fixture, row 1, facts.json#6) | >= 1 | pass | 1 |
| B | criterion_4 | 0 flag (SYNTHETIC-B-market, fixture, row 1, facts.json#6) | >= 1 | fail | 0 |
| B | hours | 2 h (SYNTHETIC-B-capacity, fixture, row 1, facts.json#10) | <= 2 | pass | 1 |
| C | criterion_1 | 1 flag (SYNTHETIC-C-market, fixture, row 1, facts.json#11) | >= 1 | pass | 1 |
| C | criterion_2 | 1 flag (SYNTHETIC-C-market, fixture, row 1, facts.json#11) | >= 1 | pass | 1 |
| C | criterion_3 | 0 flag (SYNTHETIC-C-market, fixture, row 1, facts.json#11) | >= 1 | fail | 0 |
| C | criterion_4 | 0 flag (SYNTHETIC-C-market, fixture, row 1, facts.json#11) | >= 1 | fail | 0 |
| C | hours | 2.01 h (SYNTHETIC-C-capacity, fixture, row 1, facts.json#15) | <= 2 | fail | 0 |
| D | criterion_1 | 1 flag (SYNTHETIC-D-market, fixture, row 1, facts.json#16) | >= 1 | pass | 1 |
| D | criterion_2 | 0 flag (SYNTHETIC-D-market, fixture, row 1, facts.json#16) | >= 1 | fail | 0 |
| D | criterion_3 | 0 flag (SYNTHETIC-D-market, fixture, row 1, facts.json#16) | >= 1 | fail | 0 |
| D | criterion_4 | 0 flag (SYNTHETIC-D-market, fixture, row 1, facts.json#16) | >= 1 | fail | 0 |
| D | hours | 1.99 h (SYNTHETIC-D-capacity, fixture, row 1, facts.json#20) | <= 2 | pass | 1 |

## Căn cứ ưu tiên

- A — Thuộc hai địa bàn đủ điều kiện có điểm cao nhất. Điểm 5.
- B — Thuộc hai địa bàn đủ điều kiện có điểm cao nhất. Điểm 4.
- C — Không đạt điều kiện bắt buộc. Điểm 2.
- D — Điểm thấp hơn nhóm ưu tiên. Điểm 2.

## Điểm cần con người xử lý

- Trưởng phòng Phát triển Kinh doanh kiểm tra căn cứ và duyệt kế hoạch trước khi tiếp cận khách hàng.

## Kế hoạch khảo sát

- A — Nhóm khách — Synthetic retail chains
- A — Thông tin cần xác minh — On-site response time
- A — Phụ trách — Deployment team
- B — Nhóm khách — Synthetic retail chains
- B — Thông tin cần xác minh — On-site response time
- B — Phụ trách — Deployment team
