"""Module tính toán các đặc trưng hành vi và viễn thông (RFM Velocity Features)."""
import pandas as pd
import numpy as np


def compute_data_velocity(df: pd.DataFrame, eps: float = 1e-6) -> pd.DataFrame:
    """Tính toán tỷ lệ vận tốc tiêu dùng dữ liệu: 7 ngày gần nhất so với 30 ngày.
    
    Formula:
        expected_7d = (data_usage_mb_30d / 30.0) * 7.0
        data_velocity_7d_30d = data_usage_mb_7d / (expected_7d + eps)
        
    Args:
        df: DataFrame chứa cột 'data_usage_mb_7d' và 'data_usage_mb_30d'.
        eps: Số nhỏ tránh lỗi chia cho 0.
        
    Returns:
        DataFrame bổ sung cột 'data_velocity_7d_30d'.
    """
    df = df.copy()
    if "data_usage_mb_7d" not in df.columns or "data_usage_mb_30d" not in df.columns:
        raise ValueError("DataFrame thiếu các cột dữ liệu tiêu dùng bắt buộc!")

    # Chuẩn hóa giá trị âm về 0 (nếu có lỗi ghi nhận)
    df["data_usage_mb_7d"] = df["data_usage_mb_7d"].clip(lower=0)
    df["data_usage_mb_30d"] = df["data_usage_mb_30d"].clip(lower=0)

    # Tính tỷ lệ vận tốc tiêu dùng
    expected_30d_share = (df["data_usage_mb_30d"] / 30.0) * 7.0
    df["data_velocity_7d_30d"] = df["data_usage_mb_7d"] / (expected_30d_share + eps)
    return df


def compute_recharge_velocity(df: pd.DataFrame, eps: float = 1e-6) -> pd.DataFrame:
    """Tính toán tỷ lệ nạp tiền: 14 ngày gần nhất so với 60 ngày.
    
    Formula:
        expected_14d = (recharge_amount_60d / 60.0) * 14.0
        recharge_velocity_14d_60d = recharge_amount_14d / (expected_14d + eps)
        
    Args:
        df: DataFrame chứa cột 'recharge_amount_14d' và 'recharge_amount_60d'.
        eps: Số nhỏ tránh lỗi chia cho 0.
        
    Returns:
        DataFrame bổ sung cột 'recharge_velocity_14d_60d'.
    """
    df = df.copy()
    if "recharge_amount_14d" not in df.columns or "recharge_amount_60d" not in df.columns:
        raise ValueError("DataFrame thiếu các cột nạp tiền bắt buộc!")

    df["recharge_amount_14d"] = df["recharge_amount_14d"].clip(lower=0)
    df["recharge_amount_60d"] = df["recharge_amount_60d"].clip(lower=0)

    expected_14d = (df["recharge_amount_60d"] / 60.0) * 14.0
    df["recharge_velocity_14d_60d"] = df["recharge_amount_14d"] / (expected_14d + eps)
    return df


def build_feature_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Thực thi pipeline trích xuất toàn bộ đặc trưng cho tập dữ liệu."""
    df_transformed = compute_data_velocity(df)
    df_transformed = compute_recharge_velocity(df_transformed)
    return df_transformed
