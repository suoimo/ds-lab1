# %% [markdown]
# # Khám phá Dữ liệu Tiêu dùng & Hành vi Thuê bao (Churn EDA)
#
# Notebook phân tích dữ liệu tiêu dùng dịch vụ viễn thông phục vụ bài toán dự báo rời mạng.
# Được ghép cặp đồng bộ hai chiều với file script `.py:percent` qua Jupytext.

# %%
import pandas as pd
import numpy as np

# %%
# Nạp dữ liệu fixture kiểm thử
data_path = "data/fixtures/sample_churn.csv"
df = pd.read_csv(data_path)
print(f"Kích thước tập dữ liệu mẫu: {df.shape}")
df.head()

# %% [markdown]
# ## 1. Phân phối Tỷ lệ Rời mạng (Churn Rate)

# %%
churn_dist = df["churn"].value_counts(normalize=True)
print("Phân phối nhãn Churn:")
print(churn_dist)

# %% [markdown]
# ## 2. Tính toán Thử nghiệm Vận tốc Tiêu dùng Data (7 ngày vs 30 ngày)

# %%
expected_7d = (df["data_usage_mb_30d"] / 30.0) * 7.0
df["data_velocity_7d_30d"] = df["data_usage_mb_7d"] / (expected_7d + 1e-6)

print("Thống kê mô tả đặc trưng Vận tốc Data:")
print(df[["data_usage_mb_7d", "data_usage_mb_30d", "data_velocity_7d_30d"]].describe())
