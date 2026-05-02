# Changelog

## v0.1.3
- Sửa lỗi statistics: bỏ `await` khỏi `async_add_external_statistics` (không còn là coroutine trong HA 2026.x).
- Thêm `unit_class="energy"` vào `StatisticMetaData` để tránh deprecation warning HA 2026.11.
- Sửa lỗi ngày hiển thị sai: nếu API trả về `to_date = hôm nay` (ví dụ 11 AM), tự động lùi về `t-1`.

## v0.1.1
- Sửa lỗi Energy Dashboard lệch 1 ngày: ghi statistics tại `to_date` (ngày đo thực tế) thay vì `from_date` (ngày đầu kỳ).
- Sửa lỗi timestamp statistics phải là đầu giờ (HH:00:00) — HA từ chối giá trị 23:59:59.
- Thêm `mean_type=StatisticMeanType.NONE` vào `StatisticMetaData` để tránh deprecation warning HA 2026.11.
- Thêm brand icon (`brand/icon.png`, `brand/icon@2x.png`) cho HA 2026.3+ (không cần submit lên home-assistant/brands).

## v0.1.0
- Sửa tài liệu: cập nhật chu kỳ polling từ 3 giờ sang 24 giờ (README, TEST_CHECKLIST).
- Thêm proactive token refresh cho EVNNPC, EVNCPC, EVNSPC (tránh lỗi 401 âm thầm).
- Thêm tính năng Reconfigure: người dùng có thể cập nhật Username/Password mà không cần xóa integration.
- Bổ sung translation strings cho reconfigure step (en/vi).

## v0.0.9
- Đổi scan interval từ 3 giờ sang 24 giờ (phù hợp với dữ liệu EVN chỉ cập nhật 1 lần/ngày).
- Chỉ update sensor và ghi statistics khi dữ liệu thay đổi (tránh ghi trùng lặp).
- Thêm logging chi tiết để debug external statistics.

## v0.0.8
- Sửa logic backdate statistics: ghi vào cuối ngày trước (23:59:59) và đầu ngày hiện tại (00:00).
- Mỗi ngày sẽ có 2 bản ghi (00:00 và 23:59:59) giúp Energy Dashboard hiển thị full ngày đúng cách.
- Tooltip sẽ hiển thị đúng khoảng thời gian (00:00 - 23:59:59) thay vì chỉ 1 thời điểm.

## v0.0.7
- Sửa logic backdate statistics: ghi vào from_date (ngày bắt đầu kỳ đo) thay vì to_date.
- Ghi 2 bản ghi: ngày trước from_date và from_date để Energy hiển thị delta vào đúng ngày tiêu thụ.
- Đảm bảo start timestamp là 00:00 để hiển thị full ngày.

## v0.0.6
- Sửa format statistic_id cho external statistics theo chuẩn source:unique_id.

## v0.0.5
- Sửa lỗi thiếu import ID_ECON_TOTAL_NEW trong sensor.py.

## v0.0.4
- Sửa logic external statistics dùng chỉ số công tơ thực (econ_total_new) thay vì derived_total.
- Energy Dashboard giờ hiển thị đúng lượng tiêu thụ theo delta giữa các ngày.

## v0.0.3
- Sửa cảnh báo state_class cho sensor tiêu thụ giữa 2 lần cập nhật.
- Sửa statistic_id khi ghi thống kê backdate.

## v0.0.2
- Tính điện năng theo chênh lệch số công tơ và ghi thống kê theo thời điểm đo.
- Bổ sung sensor Energy dùng cho Energy Dashboard.

## v0.0.1
- Phát hành ban đầu của tích hợp EVN Power Insights.
