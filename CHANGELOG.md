# Changelog

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
