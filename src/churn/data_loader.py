"""Module nạp và kiểm định cấu trúc dữ liệu (Data Loading & Schema Validation)."""
import os
import pandas as pd
from typing import List

REQUIRED_COLUMNS = [
    "subscriber_id",
    "data_usage_mb_7d",
    "data_usage_mb_30d",
    "recharge_amount_14d",
    "recharge_amount_60d",
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "contract_type",
    "churn",
]


def load_dataset(file_path: str) -> pd.DataFrame:
    """Nạp file CSV dữ liệu và kiểm tra các điều kiện tiên quyết.
    
    Args:
        file_path: Đường dẫn tới file CSV.
        
    Returns:
        DataFrame đã nạp và kiểm tra tính hợp lệ.
        
    Raises:
        FileNotFoundError: Nếu file không tồn tại.
        ValueError: Nếu thiếu các cột dữ liệu bắt buộc hoặc dữ liệu rỗng.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Tập dữ liệu không tồn tại: {file_path}")

    df = pd.read_csv(file_path)
    if df.empty:
        raise ValueError(f"Tập dữ liệu bị rỗng: {file_path}")

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Tập dữ liệu thiếu các cột bắt buộc: {missing_cols}")

    return df


def validate_schema(df: pd.DataFrame, expected_columns: List[str]) -> bool:
    """Xác thực schema của DataFrame so với danh sách cột kỳ vọng."""
    return all(col in df.columns for col in expected_columns)
