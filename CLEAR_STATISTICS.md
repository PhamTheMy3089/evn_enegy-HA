# Hướng dẫn Clear Statistics cũ

Sau khi cập nhật integration lên version mới với logic ghi statistics mới, bạn cần **xóa statistics cũ** để tránh hiển thị sai dữ liệu.

## Cách 1: Xóa qua Developer Tools (Khuyến nghị)

1. Vào `Settings` → `Developer Tools` → `Statistics`
2. Tìm statistic có tên: `evn_power_insights:pe15000350389_energy_backdate`
   - Hoặc tìm bằng tên hiển thị: `EVN Power Insights: PE15000350389 EVN Energy (theo thoi diem do)`
3. Bấm vào statistic đó
4. Bấm nút **"Clear statistics"** hoặc **"Remove"**
5. Xác nhận xóa

## Cách 2: Xóa qua Energy Dashboard

1. Vào `Settings` → `Energy`
2. Tìm nguồn: `EVN Power Insights: PE15000350389 EVN Energy (theo thoi diem do)`
3. Bấm **"Remove"** để xóa nguồn khỏi Energy Dashboard
4. Sau khi clear statistics (Cách 1), thêm lại nguồn vào Energy Dashboard

## Cách 3: Xóa qua SQL (Nâng cao)

Nếu bạn có quyền truy cập database Home Assistant:

```sql
DELETE FROM statistics WHERE statistic_id = 'evn_power_insights:pe15000350389_energy_backdate';
DELETE FROM statistics_meta WHERE statistic_id = 'evn_power_insights:pe15000350389_energy_backdate';
```

**Lưu ý:** Thay `pe15000350389` bằng customer_id của bạn (chữ thường).

## Sau khi clear

1. **Restart Home Assistant**
2. Đợi integration cập nhật dữ liệu (khoảng 3 giờ hoặc restart coordinator)
3. Kiểm tra Energy Dashboard xem dữ liệu đã hiển thị đúng chưa

## Kiểm tra

- Vào `Developer Tools` → `Statistics`
- Tìm statistic mới
- Xem các bản ghi có timestamp đúng không (00:00 và 23:59:59 mỗi ngày)
- Vào Energy Dashboard xem biểu đồ có hiển thị full ngày không
