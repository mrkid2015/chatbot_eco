# Báo cáo làm sạch hai file Excel

## Đầu ra

- `data/cleaned/ECO_Du_lieu_san_pham.cleaned.xlsx`
- `data/cleaned/DB-Chatbot-Chan-Doan-Sau-Benh.cleaned.xlsx`
- `data/cleaned/eco_agro.sqlite`: kho dữ liệu chuẩn hóa phục vụ thiết kế và xây bản thử; chưa phải runtime bot.
- `data/cleaned/normalized-records.jsonl`: bản ghi theo entity, có nguồn gốc.
- `data/cleaned/data-quality-issues.csv` và `.json`: vấn đề theo mã bản ghi, trường, file/sheet/dòng.
- `data/cleaned/pilot-message-preview.json`: xem trước các phần thông tin cho 5 ID, không gửi Telegram.
- `data/cleaned/manifest.json`: hash nguồn, số lượng, phạm vi và kết quả xuất.

Hai file gốc giữ nguyên byte, đã kiểm tra SHA-256. Không gộp các sản phẩm chỉ vì trùng mã đăng ký. Không tự sửa tên hoạt chất, liều, thành phần hoặc ý nghĩa nhánh chẩn đoán.

## Đã làm sạch

Đọc tất cả 11 sheet của hai workbook, gồm hướng dẫn và nhật ký. Bỏ hàng chỉ có định dạng trống và tách 3 hàng tiêu đề/hướng dẫn của file sản phẩm ra khỏi dữ liệu. Tạo `DATA_DICTIONARY` để giữ hướng dẫn từng trường. Chuẩn hóa Unicode NFC, khoảng trắng, xuống dòng; chuẩn hóa quy cách như `500ml` → `500 mL`, `20KG` → `20 kg`. Tổng 27 thay đổi ô được ghi chi tiết tại `data/private/audit/cell-changes.json`.

Mỗi dòng xuất có `source_file`, `source_sheet`, `source_row`. Mã đăng ký giữ kiểu chuỗi để không mất số 0 đầu. Ô thiếu vẫn thiếu, không suy diễn thành 0 hoặc Không.

Nội dung trả lời được tách thành các mục dấu hiệu, canh tác, hoạt chất, PHI, sản phẩm ECO hỗ trợ, khi cần kỹ sư; đồng thời giữ nguyên văn toàn bộ đáp án trong database. Bản hiển thị đổi ký hiệu có/không/cần xác minh thành chữ, không xóa mất ý nghĩa của icon. Phần chưa có cấu trúc giữ trong mục `original`, không tự tạo nội dung kỹ thuật.

## Số lượng và vấn đề

| Hạng mục | Kết quả |
|---|---|
| Sản phẩm | 26, không trùng mã SP; tất cả trạng thái nguồn Nháp |
| Phần kỹ thuật còn trống | Cả 26 thiếu `cach_dung`, `lieu_sau_rieng`, `cong_dung_chatbot`, `nguoi_duyet_ngay` — tổng 104 ô |
| Ghi chú cần kiểm tra sẵn có | 24 sản phẩm; giữ nguyên để đối chiếu |
| Trùng mã đăng ký | 2 cặp: SP-003/SP-002 và SP-021/SP-024; không coi là bản ghi trùng |
| Combo | 2 dòng ví dụ; 5 thành phần có liều thiếu đơn vị |
| Liên kết sản phẩm combo | `ECO SIÊU THẤM` chưa khớp catalog; không tự đồng nhất với `THẤM HỮU CƠ` |
| Hỏi đáp | 2 câu, cả hai chưa có câu trả lời |
| Đánh giá khách hàng | 0 dòng dữ liệu |
| Hồ sơ sâu bệnh | 143 ID duy nhất, 10 nhóm cây |
| Chất lượng nguồn sâu bệnh | 57 hồ sơ CHUAN, 86 hồ sơ THO; không tự biến THO thành chuẩn kỹ thuật |
| Nhóm triệu chứng / câu phân biệt | 7 nhóm / 16 câu |
| Bao phủ nhóm nguồn | 28/143 hồ sơ có trong danh sách ứng viên, 115 chưa có luồng nhóm tương ứng |
| Nhật ký chat | 96 tin, tách khỏi toàn bộ kho kiến thức làm sạch |

### Logic cần viết lại khi build

- `Q-XIMU-02`, nhánh Không: văn bản ghi loại `SB-XIMU-PHYTO`, JSON ghi loại `SB-MIT-THOI-GOC`. Giữ cả hai để đối chiếu, không âm thầm chọn bên nào.
- Có 3 câu không mã hóa nhánh Không trong JSON. Cả 16 câu chưa mã hóa rõ nhánh Không rõ/Chưa đào. Không rõ không được coi là Không.
- `G-XIMU-THAN` khai báo Cam sành và Na Thái nhưng không có hồ sơ ứng viên cho hai cây này.
- Một số câu ghi “kết luận” từ một dấu hiệu, trong khi nguồn cũng nói có thể đồng nhiễm. Bản thử cần tổng hợp bằng chứng, giữ trường hợp chưa đủ dữ kiện, không kết luận chỉ vì còn 1 ID sau khi thu nhỏ phạm vi.
- Nhãn `ACTIVE` là trạng thái của file do người dùng đưa, không phải bằng chứng nghiên cứu/pháp lý đã được xác minh. Không thêm cổng duyệt cho bản thử; vẫn giữ dữ kiện thiếu/mâu thuẫn để trả lời trung thực.
- Các viện dẫn MRL/đăng ký/PHI được bảo toàn theo nguồn, chưa được đối chiếu văn bản hiện hành. Dấu [không] không được tự diễn giải thành mọi ý nghĩa như cấm dùng hoặc không phát hiện.

## Cách tái tạo và kiểm tra

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/inspect-workbooks.py
.\.venv\Scripts\python.exe -X utf8 scripts/clean-eco-data.py
.\.venv\Scripts\python.exe -X utf8 scripts/verify-cleaned-data.py
```

Script làm sạch tái tạo các file trong `data/cleaned/`, không sửa workbook gốc. Không chỉnh sửa trực tiếp DB/bản xuất làm nơi lưu cập nhật lâu dài; cơ chế version/migration được mô tả trong `data-model.md` và sẽ triển khai khi build. `data/private/` chứa audit toàn bộ nguồn, gồm nhật ký; không đưa lên GitHub.
