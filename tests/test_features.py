"""Unit tests cho các hàm biến đổi đặc trưng hành vi và viễn thông."""
import pytest
import pandas as pd
from churn.features import (
    compute_data_velocity,
    compute_recharge_velocity,
    build_feature_pipeline,
)
from churn.data_loader import load_dataset


def test_compute_data_velocity_normal():
    """Kiểm tra trường hợp dữ liệu tiêu dùng bình thường (vận tốc ~ 1.0)."""
    df = pd.DataFrame({
        "data_usage_mb_7d": [700.0],
        "data_usage_mb_30d": [3000.0],
    })
    res = compute_data_velocity(df)
    assert "data_velocity_7d_30d" in res.columns
    # 700 / ((3000 / 30) * 7) = 700 / 700 = 1.0
    assert pytest.approx(res["data_velocity_7d_30d"].iloc[0], 0.01) == 1.0


def test_compute_data_velocity_zero_division():
    """Kiểm tra xử lý biên khi mẫu số bằng 0 (khách hàng không dùng data trong 30 ngày)."""
    df = pd.DataFrame({
        "data_usage_mb_7d": [0.0],
        "data_usage_mb_30d": [0.0],
    })
    res = compute_data_velocity(df)
    assert "data_velocity_7d_30d" in res.columns
    assert res["data_velocity_7d_30d"].iloc[0] >= 0.0
    assert not pd.isna(res["data_velocity_7d_30d"].iloc[0])


def test_compute_recharge_velocity_normal():
    """Kiểm tra trường hợp nạp tiền thông thường (vận tốc ~ 1.0)."""
    df = pd.DataFrame({
        "recharge_amount_14d": [140.0],
        "recharge_amount_60d": [600.0],
    })
    res = compute_recharge_velocity(df)
    assert "recharge_velocity_14d_60d" in res.columns
    # 140 / ((600 / 60) * 14) = 140 / 140 = 1.0
    assert pytest.approx(res["recharge_velocity_14d_60d"].iloc[0], 0.01) == 1.0


def test_build_feature_pipeline_on_fixture():
    """Kiểm tra chạy toàn bộ pipeline trích xuất đặc trưng trên tập fixture mẫu."""
    df = load_dataset("data/fixtures/sample_churn.csv")
    res = build_feature_pipeline(df)
    assert len(res) == 20
    assert "data_velocity_7d_30d" in res.columns
    assert "recharge_velocity_14d_60d" in res.columns
    assert (res["data_velocity_7d_30d"] >= 0).all()
    assert (res["recharge_velocity_14d_60d"] >= 0).all()
