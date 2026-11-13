# Đối chiếu hồ sơ thị trường

Kính gửi Trưởng phòng Phát triển Kinh doanh

Nguồn — AI301_De04_Du_Lieu_Mau_1000_Leads_Cleaned.xlsx, sheet `Dữ liệu nguồn `.

| Địa bàn | Hồ sơ | Khớp WMS hoàn toàn | SLA được ghi nhận khả thi | Mã hồ sơ lặp |
|---|---:|---:|---:|---:|
| DB-01 | 320 | 299 | 309 | 0 |
| DB-02 | 250 | 219 | 233 | 0 |
| DB-03 | 230 | 195 | 28 | 0 |
| DB-04 | 200 | 0 | 0 | 0 |

Các chỉ số là số đếm nhãn trong workbook. Phân bố kỳ, nguồn, cờ trùng và dòng tham chiếu nằm trong comparison.json.

## Điểm MCDA ghi trong workbook

Điểm và kết luận dưới đây được trích theo ô nguồn. Điểm số hiển thị tối đa ba chữ số thập phân.

| Địa bàn | Khớp WMS | Triển khai | Cạnh tranh | Quy mô | Tổng điểm | Kết luận nguồn |
|---|---|---|---|---|---|---|
| DB-01 | 5 (`'Ma Trận MCDA'!C4`) | 5 (`'Ma Trận MCDA'!D4`) | 3.5 (`'Ma Trận MCDA'!E4`) | 5 (`'Ma Trận MCDA'!F4`) | 4.7 (`'Ma Trận MCDA'!G4`) | HẠNG 1 - ƯU TIÊN SỐ 1 MỞ RỘNG (Top 1) (`'Ma Trận MCDA'!H4`) |
| DB-02 | 4.5 (`'Ma Trận MCDA'!C5`) | 4 (`'Ma Trận MCDA'!D5`) | 4.5 (`'Ma Trận MCDA'!E5`) | 4 (`'Ma Trận MCDA'!F5`) | 4.275 (`'Ma Trận MCDA'!G5`) | HẠNG 2 - ƯU TIÊN SỐ 2 MỞ RỘNG (Top 2) (`'Ma Trận MCDA'!H5`) |
| DB-03 | 3 (`'Ma Trận MCDA'!C6`) | 1.5 (`'Ma Trận MCDA'!D6`) | 3 (`'Ma Trận MCDA'!E6`) | 3.5 (`'Ma Trận MCDA'!F6`) | 2.625 (`'Ma Trận MCDA'!G6`) | LOẠI BỎ (Không đạt ngưỡng hỗ trợ on-site SLA <= 2h) (`'Ma Trận MCDA'!H6`) |
| DB-04 | 1 (`'Ma Trận MCDA'!C7`) | 1 (`'Ma Trận MCDA'!D7`) | 4 (`'Ma Trận MCDA'!E7`) | 1 (`'Ma Trận MCDA'!F7`) | 1.6 (`'Ma Trận MCDA'!G7`) | LOẠI BỎ (Không đạt ngưỡng độ khớp giải pháp WMS) (`'Ma Trận MCDA'!H7`) |

## Quyết định và điều kiện bổ sung

Cần xác minh căn cứ chấm và điều kiện sàng lọc trước khi xác nhận đề xuất của workbook. Kế hoạch khảo sát chờ quyết định.

- Xác nhận cách tính điểm từng tiêu chí và điều kiện sàng lọc.
- Bổ sung căn cứ cạnh tranh và xác nhận năng lực triển khai theo địa bàn.
- Xác nhận quy tắc xử lý kỳ khác nhau và nguồn lặp.
