# Vận hành dự kiến

Tài liệu chuẩn bị, chưa có hệ thống production.

MVP hiện hành là Telegram nội bộ, Python/SQLite/Gemini, 5 hồ sơ sầu riêng, không cổng duyệt. Xem `windows-local.md` và kế hoạch Telegram. Checklist bán hàng bên dưới dành cho giai đoạn sau, không là điều kiện chặn bộ thử.

## Trước khi chạy thật

- Xác nhận dữ liệu sản phẩm/chính sách, người duyệt và lịch cập nhật.
- Chốt kênh tiếp nhận nhân viên, giờ trực và hành vi ngoài giờ.
- Kiểm thử các trường hợp trong `docs/03-san-pham/kich-ban-danh-gia.md`.
- Xác nhận nơi lưu, quyền truy cập, thời hạn lưu/xóa dữ liệu và cách lấy đồng ý.
- Cấu hình khóa phía server, giới hạn chi phí/tần suất, giám sát lỗi và phương án quay về phiên bản trước.

## Khi phát hiện trả lời sai giá hoặc sai chính sách

Tạm ngừng trả lời phần dữ kiện bị ảnh hưởng, dùng phản hồi chưa thể xác nhận và hướng bàn giao đã cấu hình. Xác định mã nguồn/phiên bản dữ liệu, sửa tại nguồn, nạp lại và chạy lại kịch bản lỗi trước khi bật lại. Không ghi PII vào biên bản sự cố.

## Khi tích hợp lỗi

Phân biệt lỗi LLM, nguồn dữ liệu và bàn giao. Kiểm tra trạng thái hệ thống bằng log đã che dữ liệu; không báo khách rằng giao dịch thành công khi chưa có xác nhận. Retry thao tác ghi phải chống trùng.

## Theo dõi

Đo lỗi, độ trễ, chi phí, câu trả lời không có nguồn và bàn giao thất bại. Chỉ thu thập phần dữ liệu cần thiết; ngưỡng cảnh báo và chủ sở hữu vận hành được chốt khi triển khai.
