"""Script huấn luyện mô hình Churn Baseline và tự động xuất Model Artifact Manifest."""
import argparse
import os
import yaml
import pandas as pd
from datetime import datetime, timezone
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score
from churn.data_loader import load_dataset
from churn.features import build_feature_pipeline
from churn.utils import compute_file_sha256, get_git_commit_sha, is_git_working_tree_dirty


def run_training(config_path: str):
    """Quy trình huấn luyện và xuất bản kê khai Model Artifact Manifest."""
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    data_path = cfg["dataset"]["raw_path"]
    print(f"[*] Đang nạp dữ liệu từ: {data_path}")
    raw_df = load_dataset(data_path)

    # 1. Tính mã băm SHA-256 dữ liệu phục vụ Data Lineage
    data_sha256 = compute_file_sha256(data_path)
    print(f"[*] Dataset SHA-256: {data_sha256}")

    # 2. Xây dựng pipeline trích xuất đặc trưng
    df = build_feature_pipeline(raw_df)

    feature_cols = [
        "data_velocity_7d_30d",
        "recharge_velocity_14d_60d",
        "tenure_months",
        "monthly_charges",
        "total_charges",
    ]
    X = df[feature_cols]
    y = df["churn"]

    # 3. Huấn luyện mô hình Random Forest
    rf = RandomForestClassifier(
        n_estimators=cfg["model"].get("n_estimators", 50),
        max_depth=cfg["model"].get("max_depth", 4),
        random_state=cfg["model"].get("random_state", 42),
    )
    rf.fit(X, y)
    probs = rf.predict_proba(X)[:, 1]

    pr_auc = float(average_precision_score(y, probs))
    roc_auc = float(roc_auc_score(y, probs))
    print(f"[*] Đánh giá Mô hình: PR-AUC = {pr_auc:.4f} | ROC-AUC = {roc_auc:.4f}")

    # 4. Kiểm tra Git Lineage
    git_sha = get_git_commit_sha()
    is_dirty = is_git_working_tree_dirty()
    print(f"[*] Git Lineage: SHA = {git_sha[:8]} | Working Tree Dirty = {is_dirty}")

    # 5. Khởi tạo và ghi Model Manifest
    manifest_cfg = cfg.get("manifest", {})
    manifest_out = manifest_cfg.get("output_path", "models/manifests/model_manifest.yaml")
    os.makedirs(os.path.dirname(manifest_out), exist_ok=True)

    manifest_data = {
        "model_metadata": {
            "model_name": manifest_cfg.get("model_name", "enterprise_prepaid_churn_rf"),
            "model_version": manifest_cfg.get("model_version", "v1.0.0"),
            "framework": "scikit-learn",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
        "source_code_lineage": {
            "git_commit_sha": git_sha,
            "working_tree_dirty": is_dirty,
            "pipeline_entrypoint": f"python3 src/churn/train.py --config {config_path}",
        },
        "data_lineage": {
            "dataset_path": data_path,
            "dataset_sha256": data_sha256,
            "total_records": len(df),
        },
        "evaluation_metrics": {
            "pr_auc": round(pr_auc, 4),
            "roc_auc": round(roc_auc, 4),
            "quality_gate_passed": bool(pr_auc >= 0.70),
        },
    }

    with open(manifest_out, "w", encoding="utf-8") as f:
        yaml.dump(manifest_data, f, default_flow_style=False, sort_keys=False)
    print(f"[+] Đã xuất Model Manifest chuẩn kiểm toán tại: {manifest_out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Huấn luyện mô hình Churn và xuất Model Manifest")
    parser.add_argument(
        "--config",
        default="configs/train_churn.yaml",
        help="Đường dẫn file cấu hình YAML",
    )
    args = parser.parse_args()
    run_training(args.config)
