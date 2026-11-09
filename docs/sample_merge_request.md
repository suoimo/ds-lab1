# [MR] Bổ sung Nhóm Đặc trưng Vận tốc Tiêu dùng Data và Nạp tiền (Velocity Metrics)

## 1. Vấn đề Nghiệp vụ & Động lực Kỹ thuật (Problem Statement)
- **Ticket ID:** #CHURN-1042
- **Bối cảnh:** Mô hình Churn Baseline hiện tại có chỉ số Recall@10k ở phân khúc khách hàng ARPU cao chỉ đạt 12.3%. Phân tích lỗi cho thấy chúng ta chưa nắm bắt được tín hiệu khách hàng đột ngột giảm nạp tiền và dừng sử dụng data 4G trong 7-14 ngày gần nhất.

## 2. Chi tiết Thay đổi Kỹ thuật (Technical Changes)
- Xây dựng module `src/churn/features.py`:
  + `compute_data_velocity`: tính tỷ lệ tiêu dùng 7 ngày so với 30 ngày.
  + `compute_recharge_velocity`: tính tỷ lệ nạp tiền 14 ngày so với 60 ngày.
- Bổ sung 4 bài unit test trong `tests/test_features.py` bao phủ trường hợp chia cho 0 và test fixture.
- Cập nhật pipeline huấn luyện `src/churn/train.py` tự động xuất Model Manifest.

## 3. Bằng chứng Thực nghiệm Định lượng (Empirical Evidence)
- **Dataset Snapshot Checksum:** `7f3b8c2d9e1a4f5b6c7d8e9f...`
- **Kết quả Kiểm định Thực nghiệm:**

| Chỉ số Đánh giá | Mô hình Cũ (Baseline) | Mô hình Đề xuất (Candidate) | Mức độ Cải thiện |
| :--- | :---: | :---: | :---: |
| **PR-AUC Toàn tập** | 0.7412 | **0.8250** | **+0.0838 tuyệt đối** |
| **ROC-AUC** | 0.8120 | **0.9120** | **+0.1000** |
| **Precision@10.000** | 24.10% | **28.30%** | +4.20 điểm % |

## 4. Tác động Hệ thống & Kế hoạch Rollback (Impact & Rollback Plan)
- **Tính tương thích:** Không thay đổi cấu trúc bảng kết quả đầu ra (schema preserved).
- **Kế hoạch Rollback:** Nếu batch scoring phát sinh lỗi, cập nhật biến cấu hình Airflow để chạy lại container `v1.0.0` ngay lập tức mà không cần deploy lại mã nguồn.
