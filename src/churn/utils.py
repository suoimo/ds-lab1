"""Tiện ích tính toán Checksum, Hashing và truy vết Git phục vụ Data & Model Lineage."""
import hashlib
import os
import subprocess


def compute_file_sha256(file_path: str) -> str:
    """Tính toán mã băm SHA-256 của tệp tin theo từng khối 64KB (chunk-based).
    
    Args:
        file_path: Đường dẫn tệp tin cần tính hash.
        
    Returns:
        Chuỗi băm hexa 64 ký tự của file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_git_commit_sha() -> str:
    """Lấy mã băm Git commit SHA hiện tại của kho mã nguồn."""
    try:
        res = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return res
    except Exception:
        return "UNKNOWN_GIT_SHA"


def is_git_working_tree_dirty() -> bool:
    """Kiểm tra xem thư mục làm việc Git có thay đổi chưa commit hay không."""
    try:
        res = subprocess.check_output(
            ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return len(res) > 0
    except Exception:
        return False
