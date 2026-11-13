# Task 1 — Thiết kế quy trình đánh giá thị trường

## Mục tiêu
Hỗ trợ Trưởng phòng Phát triển Kinh doanh chọn hai trong bốn địa bàn để khảo sát trước khi trình Ban Giám đốc. Khi thiếu căn cứ, bàn giao điều kiện cần xác minh.

## Đầu vào
Tài liệu thị trường có nguồn và kỳ thống kê, hồ sơ đối thủ, phản hồi khách hàng, danh mục WMS, năng lực triển khai và bộ tiêu chí giảng viên cấp.

## Quy trình hiện tại
Chuyên viên tiếp nhận báo cáo → đọc và ghi lại số liệu → thu thập thông tin đối thủ → ghép danh sách khách tiềm năng → tổng hợp và bàn giao cho Trưởng phòng.

| Vấn đề | Ảnh hưởng |
|---|---|
| Báo cáo khác kỳ | So sánh quy mô hoặc nhu cầu giữa các địa bàn bị lệch. |
| Số liệu lặp từ cùng nguồn | Một quan sát có thể bị đếm nhiều lần hoặc được coi là nhiều bằng chứng độc lập. |
| Thiên về quy mô | Địa bàn đông khách có thể được ưu tiên dù nhu cầu thiếu phù hợp với WMS. |
| Bỏ sót yêu cầu hỗ trợ tại chỗ | Nhóm có thể khảo sát địa bàn vượt khả năng triển khai hiện tại. |

## Quy trình đề xuất
| Bước | Đầu vào | Công việc | Đầu ra | Phụ trách |
|---|---|---|---|---|
| Tiếp nhận | Hồ sơ và tiêu chí | Xác nhận phạm vi bốn địa bàn và phiên bản tiêu chí | Danh mục nguồn và quy tắc | Chuyên viên nghiên cứu |
| Đối chiếu | Hồ sơ có tham chiếu | Agent đối chiếu kỳ, đơn vị, trùng nguồn và mâu thuẫn. Tự động hóa giúp kiểm tra nhất quán. | Bảng dữ kiện và danh sách cần xác minh | Agent, chuyên viên nghiên cứu |
| Đánh giá | Dữ kiện và tiêu chí | Agent tính kết quả theo quy tắc để có thể chạy lại và kiểm tra từng ngưỡng. | Bảng so sánh bốn địa bàn và đề xuất sơ bộ | Agent, nhóm Phát triển Kinh doanh |
| Soạn bàn giao | Bảng so sánh và thông tin khảo sát | Agent tạo báo cáo từ kết quả chung để giữ nhất quán giữa điểm, đề xuất và kế hoạch. | Báo cáo, kế hoạch và nhật ký | Agent |
| Duyệt | Báo cáo và bằng chứng | Kiểm tra căn cứ, xử lý điểm chưa rõ và duyệt kế hoạch | Quyết định khảo sát hoặc yêu cầu bổ sung | Trưởng phòng Phát triển Kinh doanh |

### Điểm kiểm tra của con người
1. Chuyên viên nghiên cứu xử lý khi dữ kiện thiếu, trùng, lệch kỳ hoặc mâu thuẫn. Mở nguồn theo tham chiếu và đối chiếu giá trị, kỳ, đơn vị và danh tính nguồn. Nếu chưa xác minh được, giữ trạng thái chưa xác định.
2. Trưởng phòng kiểm tra trước khi duyệt, đặc biệt khi đồng điểm ở vị trí thứ hai, thiếu căn cứ hoặc có điều kiện triển khai sát ngưỡng. Tính lại các tiêu chí quyết định từ nguồn và quy tắc, kiểm tra nhóm khách, nội dung xác minh và người phụ trách. Yêu cầu bổ sung trước khi duyệt nếu còn thiếu.

## Đầu ra
Bảng so sánh bốn địa bàn có tham chiếu, đề xuất hai địa bàn hoặc điều kiện cần bổ sung, lý do chưa ưu tiên từng địa bàn còn lại, kế hoạch khảo sát và nhật ký thực thi. Kiến trúc gồm công cụ tổng hợp dữ kiện, công cụ đánh giá theo quy tắc và bước sinh báo cáo từ kết quả chung.
