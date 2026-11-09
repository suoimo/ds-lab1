# ADR 001: Lựa chọn Kiến trúc Batch Scoring Hàng tuần Thay vì Real-time API

## Trạng thái: ĐÃ PHÊ DUYỆT (ACCEPTED)
**Ngày quyết định:** 2026-05-15  
**Hội đồng thẩm định:** Enterprise MLOps Technical Council  
**Người đề xuất:** Lead Data Scientist

---

## 1. Bối cảnh & Động lực Kỹ thuật
Bộ phận Marketing và Chăm sóc Khách hàng yêu cầu danh sách các thuê bao có rủi ro rời mạng cao nhất để triển khai các gói cước ưu đãi và cuộc gọi chăm sóc hàng tuần.

Có 2 phương án kiến trúc được đưa ra thảo luận:
1. **Phương án 1 (Real-time Scoring API):** Suy luận theo thời gian thực mỗi khi có sự kiện phát sinh (nạp thẻ, cuộc gọi, thay đổi gói cước).
2. **Phương án 2 (Weekly Batch Scoring):** Dự báo định kỳ vào Chủ nhật hàng tuần cho toàn bộ thuê bao đang hoạt động.

---

## 2. Quyết định Kiến trúc
Chúng tôi quyết định lựa chọn **Phương án 2: Weekly Batch Scoring** kết hợp lưu trữ kết quả vào Feature Store / Data Warehouse để phục vụ các hệ thống nghiệp vụ (CRM, SMS Gateway).

---

## 3. Lý do Lựa chọn & Trade-offs
1. **Bản chất Nghiệp vụ:** Kênh gọi điện của tổng đài viên và chiến dịch gửi tin nhắn SMS chạy theo kế hoạch tuần. Không có hành động nào của con người đòi hỏi phản hồi dưới 1 giây.
2. **Chi phí Vận hành Hạ tầng:** Cụm phục vụ Real-time API 24/7 đòi hỏi dự phòng hạ tầng Kubernetes, chi phí ước tính cao gấp 8 lần so với một Batch Job chạy trong 2 giờ mỗi tuần.
3. **Độ ổn định & Kiểm soát Chất lượng:** Batch Scoring cho phép chạy toàn bộ bộ kiểm thử Data Quality Checks và phát hiện Data Drift trước khi chuyển giao danh sách cho kinh doanh.

---

## 4. Hệ quả & Kế hoạch Tiếp theo
- **Hệ quả tích cực:** Hạ tầng gọn nhẹ, dễ bảo trì, dễ truy vết (audit trail) với mã commit Git và checksum dữ liệu cố định.
- **Hạn chế:** Không bắt kịp ngay lập tức những hành vi biến động đột ngột phát sinh giữa tuần.
- **Kế hoạch tương lai:** Khi ra mắt tính năng tin nhắn in-app theo thời gian thực, sẽ bổ sung thêm kiến trúc Event-Driven Real-time API riêng biệt.
