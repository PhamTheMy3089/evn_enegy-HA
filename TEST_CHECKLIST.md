# Checklist Test Integration EVN Power Insights

## Trước khi test

- [ ] Đã copy thư mục `custom_components/evn_power_insights` vào Home Assistant
- [ ] Đã có thông tin tài khoản EVN (Username/Password)
- [ ] Đã có Mã khách hàng hợp lệ (11–13 ký tự, thường bắt đầu bằng `P`)
- [ ] Home Assistant đã được restart sau khi copy files

## Test Config Flow

1. **Vào Settings > Devices & Services > Add Integration**
   - [ ] Tìm thấy "EVN Power Insights" trong danh sách
   - [ ] Click vào integration và form hiển thị đúng

2. **Nhập mã khách hàng**
   - [ ] Mã khách hàng hợp lệ được chấp nhận
   - [ ] Mã khách hàng sai hiển thị lỗi "unknown" hoặc "error_ma_kh_deny"

3. **Xác nhận chi nhánh EVN**
   - [ ] Thông tin EVN branch hiển thị đúng
   - [ ] Trường hợp không hỗ trợ hiển thị lỗi "not_supported"

4. **Nhập thông tin đăng nhập**
   - [ ] Username/Password đúng: integration được tạo thành công
   - [ ] Username/Password sai: hiển thị lỗi "invalid_auth"
   - [ ] Nếu khu vực không yêu cầu ngày bắt đầu hóa đơn (vd: EVNCPC), có thể để trống

## Test Sensors

Sau khi integration được cấu hình:

1. **Kiểm tra sensor được tạo**
   - [ ] Vào Developer Tools > States
   - [ ] Tìm sensor `sensor.<customer_id>_energy_total`

2. **Kiểm tra dữ liệu**
   - [ ] Sensor có giá trị (không phải "unknown")
   - [ ] Dữ liệu được cập nhật theo chu kỳ mặc định (3 giờ)
   - [ ] Giá trị hiển thị đúng với dữ liệu EVN

## Test Logs

1. **Kiểm tra logs**
   - [ ] Vào Settings > System > Logs
   - [ ] Tìm các dòng có chứa `evn_power_insights`
   - [ ] Không có lỗi nghiêm trọng (ERROR)

## Test Unload/Reload

1. **Test unload integration**
   - [ ] Vào Settings > Devices & Services
   - [ ] Tìm integration "EVN Power Insights"
   - [ ] Click vào và chọn "Delete"
   - [ ] Integration được xóa thành công
   - [ ] Sensor biến mất

2. **Test reload integration**
   - [ ] Sau khi unload, add lại integration
   - [ ] Integration hoạt động bình thường

## Ghi chú

- Integration sử dụng polling mỗi 3 giờ
- Nếu API trả về lỗi, sensor sẽ giữ giá trị cũ hoặc hiển thị "unavailable"
