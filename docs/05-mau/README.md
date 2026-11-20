# Cách chuẩn bị dữ liệu

Phần dưới là mẫu bán hàng ban đầu cho giai đoạn sau. MVP Telegram hiện hành dùng hai Excel đã cung cấp và 5 ID trong kế hoạch; không yêu cầu người duyệt. `product-catalog.csv` trống là mẫu cũ, không phải toàn bộ catalog hiện có. Dữ liệu thật đã xuất tại `data/cleaned/`.

Điền `business-input.md`, thêm sản phẩm vào `product-catalog.csv` và ghi chính sách trong `sales-policies.md`.

Catalog hiện chỉ có tiêu đề, chưa có sản phẩm. Dùng UTF-8; mỗi dòng là một mã sản phẩm/quy cách duy nhất. `price` là số chưa định dạng (không ghi dấu phân cách hàng nghìn); `currency` là mã tiền như VND khi nguồn xác nhận. Trường chưa biết để trống, không ghi 0 thay thế.

`source_url` có thể là URL chính thức hoặc mã tài liệu nội bộ truy ngược được. Ngày dùng ISO 8601. `approval_status` dùng `draft` hoặc `approved`; chỉ bản có người duyệt, nguồn và còn hiệu lực mới được dùng cho khách. Thiếu `valid_until` không có nghĩa giá/tồn kho luôn còn đúng: phải có quy tắc cập nhật được chủ dữ liệu xác nhận.

Nguồn giá/tồn kho cần cập nhật theo cách doanh nghiệp vận hành. Không đưa dữ liệu khách, API key hoặc tài liệu nhạy cảm vào Git; dữ liệu cục bộ đặt trong `data/private/` khi cần.
