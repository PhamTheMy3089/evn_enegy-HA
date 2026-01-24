# Hướng dẫn cài đặt EVN Power Insights Integration

## Yêu cầu

- Home Assistant phiên bản 2022.7.0 trở lên
- HACS đã được cài đặt (nếu cài qua HACS)

## Cài đặt qua HACS

### Bước 1: Thêm Custom Repository

1. Mở Home Assistant
2. Vào **HACS** (Home Assistant Community Store)
3. Click vào menu **3 chấm** ở góc trên bên phải
4. Chọn **Custom repositories**
5. Thêm thông tin:
   - **Repository**: URL của repository GitHub này
   - **Category**: Chọn **Integration**
6. Click **Add**

### Bước 2: Cài đặt Integration

1. Trong HACS, vào tab **Integrations**
2. Tìm **EVN Power Insights**
3. Click vào integration
4. Click **Download**
5. Chọn **Restart Home Assistant** khi được hỏi

### Bước 3: Cấu hình Integration

1. Sau khi Home Assistant khởi động lại, vào **Settings** > **Devices & Services**
2. Click **Add Integration**
3. Tìm và chọn **EVN Power Insights**
4. Nhập **Mã khách hàng** (11–13 ký tự, thường bắt đầu bằng `P`)
5. Xác nhận thông tin chi nhánh EVN
6. Nhập **Username**, **Password**, và **Ngày bắt đầu hóa đơn**
   - Lưu ý: Một số khu vực (ví dụ EVNCPC) không yêu cầu **Ngày bắt đầu hóa đơn**
7. Click **Submit**

## Cài đặt thủ công

### Bước 1: Copy files

1. Copy toàn bộ thư mục `custom_components/evn_power_insights` vào thư mục `custom_components` của Home Assistant
2. Cấu trúc sẽ là: `config/custom_components/evn_power_insights/`

### Bước 2: Restart Home Assistant

1. Vào **Developer Tools** > **YAML**
2. Click **Restart** hoặc restart Home Assistant qua Settings

### Bước 3: Cấu hình Integration

Làm theo các bước tương tự như phần "Cài đặt qua HACS" - Bước 3

## Kiểm tra cài đặt

Sau khi cấu hình xong, bạn sẽ thấy:

- Sensor mới trong **Developer Tools** > **States**:
  - `sensor.<customer_id>_energy_total` (Tổng điện năng)

## Xử lý lỗi

### Lỗi "Cannot connect"
- Kiểm tra kết nối internet
- Kiểm tra lại mã khách hàng

### Lỗi "Invalid auth"
- Kiểm tra lại Username/Password
- Đảm bảo tài khoản EVN còn hoạt động

### Lỗi "Not supported"
- Khu vực/chi nhánh EVN chưa được hỗ trợ

### Lỗi "No monitor"
- Công tơ chưa hỗ trợ ghi xa hằng ngày

## Hỗ trợ

Nếu gặp vấn đề, vui lòng tạo issue trên GitHub repository.
