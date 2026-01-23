# EVN Power Insights cho Home Assistant

[English](README_en.md) | Tiếng Việt

Tích hợp này lấy dữ liệu điện năng tiêu thụ từ các cổng EVN theo khu vực và hiển thị trên Home Assistant thông qua các sensor. Hỗ trợ cài đặt qua UI, tự động nhận diện tổng công ty EVN dựa trên mã khách hàng.

## Tính năng
- Theo dõi nhiều mã khách hàng trên cùng một HA.
- Tự động xác định chi nhánh EVN.
- Sensor chuẩn Energy (tổng điện năng) để dùng trong Energy Dashboard.
- Hỗ trợ 5 tổng công ty EVN: EVNHANOI, EVNHCMC, EVNNPC, EVNCPC, EVNSPC.

## Yêu cầu
- Home Assistant 2022.7.0 trở lên.
- Công tơ điện tử đo xa có dữ liệu theo ngày.
- Tài khoản EVN hợp lệ (username/password).

## Cài đặt
### Cài qua HACS (khuyến nghị)
1. HACS → Integrations → Explore & download repositories.
2. Tìm `EVN Power Insights` → Download.
3. Khởi động lại Home Assistant.

### Cài thủ công
1. Copy `custom_components/evn_power_insights` vào thư mục `custom_components` của HA.
2. Khởi động lại Home Assistant.

## Thiết lập
1. Settings → Devices & Services → Add Integration → `EVN Power Insights`.
2. Nhập `Mã khách hàng` (11–13 ký tự, thường bắt đầu bằng `P`).
3. Xác nhận thông tin chi nhánh EVN.
4. Nhập `Username`, `Password`, và `Ngày bắt đầu hóa đơn` (chỉ yêu cầu ở một số khu vực; ví dụ EVNCPC không cần).

## Sensor và Energy Dashboard
Sensor được giữ lại để dùng cho Energy Dashboard:
- `Tổng điện năng` (chuẩn Energy)

Thêm vào Energy Dashboard:
1. Settings → Energy → Add consumption.
2. Chọn entity `Tổng điện năng` (kWh).

## Giới hạn
- Dữ liệu cập nhật theo chu kỳ (mặc định 3 giờ), không tức thì.

## Hỗ trợ
Vui lòng tạo issue tại repo hoặc xem hướng dẫn trong `SECURITY.md`.

## Nguồn tham khảo
- https://github.com/trvqhuy/nestup_evn/tree/main
