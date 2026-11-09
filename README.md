# Lab 1: Dự án Thực hành Quản lý Source Code & Scaffold MLOps Chuẩn Doanh nghiệp

**Lab 1: Tổng quan Data Science & Quản lý Source Code trong MLOps**.  
Dự án này là một phiên bản rút gọn, độc lập và hoàn chỉnh của hệ thống dự báo thuê bao rời mạng (**Telecom Churn Prediction System**), được thiết kế chuẩn mực theo mô hình công nghiệp.

---

## 1. Cấu trúc Thư mục Dự án

```text
lab-1/
├── README.md                      # Hướng dẫn chi tiết từng bước thực hành
├── Makefile                       # Tự động hóa make install, lint, format, test, train
├── pyproject.toml                 # Định nghĩa package và dependencies chuẩn PEP 621
├── requirements.txt               # Danh sách thư viện Python
├── .gitignore                     # Tường lửa đa tầng chặn data/models/secrets
├── .gitattributes                 # Chuẩn hóa ký tự xuống dòng LF và bộ lọc nbstripout
├── .pre-commit-config.yaml        # Bộ hook kiểm tra tự động trước commit
├── .env.example                   # Mẫu khai báo biến môi trường an toàn
├── configs/
│   └── train_churn.yaml           # Cấu hình siêu tham số và đường dẫn dữ liệu
├── data/
│   ├── .gitkeep
│   └── fixtures/
│       └── sample_churn.csv       # Dữ liệu synthetic viễn thông mẫu (20 bản ghi)
├── notebooks/
│   ├── 01_churn_eda.ipynb         # Notebook phân tích khám phá (đã strip outputs)
│   └── 01_churn_eda.py            # Script Python song hành qua Jupytext
├── src/
│   └── churn/
│       ├── __init__.py
│       ├── data_loader.py         # Nạp và kiểm tra schema contract
│       ├── features.py            # Trích xuất đặc trưng RFM Velocity
│       ├── utils.py               # Tiện ích SHA-256 Checksum và Git Lineage
│       └── train.py               # Huấn luyện mô hình và tự động xuất Manifest
├── tests/
│   ├── __init__.py
│   └── test_features.py           # Unit tests kiểm định các hàm biến đổi đặc trưng
├── models/
│   └── manifests/
│       └── model_manifest.yaml    # Bản kê khai Model Lineage chuẩn kiểm toán
└── docs/
    ├── adr/
    │   └── 0001-batch-scoring-architecture.md # Bản ghi quyết định kiến trúc
    └── sample_merge_request.md    # Template Merge Request chuẩn doanh nghiệp
```

---

## 2. Hướng dẫn Từng Bước Thực hành trên Lớp (Step-by-step Hands-on)

### Bước 1: Khởi tạo Kho Git và Cấu hình Định danh Cá nhân
Di chuyển terminal vào thư mục `lab-1/` và khởi tạo Git repository:

```bash
cd "MLOPs_Data Sciencetist/exercise-1/lab-1"
git init -b main

# Thiết lập danh tính người tạo commit cục bộ (Local Scope)
git config user.name "Nguyen Van A"
git config user.email "nguyenvana@example.com"

# Kiểm tra trạng thái cấu hình
git config --list --local
```

### Bước 2: Thiết lập Bộ lọc Jupyter Notebook & Kích hoạt Pre-commit
Thiết lập bộ lọc clean filter `nbstripout` và cài đặt `pre-commit`:

```bash
# 1. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 2. Cài đặt bộ lọc nbstripout dựa trên cấu hình trong .gitattributes
nbstripout --install --attributes .gitattributes

# 3. Kích hoạt hook tự động pre-commit
pre-commit install
```

### Bước 3: Kiểm chứng Khả năng Chặn Dữ liệu Lớn của `.gitignore`
Kiểm tra xem rule trong `.gitignore` có hoạt động chính xác không bằng lệnh `git check-ignore -v`:

```bash
# Thử kiểm tra xem file CSV tự do có bị chặn không:
git check-ignore -v --no-index data/raw/large_churn_dump.csv
# -> Output trả về rule: .gitignore:data/raw/*

# Thử kiểm tra xem file fixtures có được ngoại lệ cho phép không:
git check-ignore -v --no-index data/fixtures/sample_churn.csv
# -> Output trả về rule có dấu !: .gitignore:!data/fixtures/*
```

### Bước 4: Chạy Unit Tests Kiểm định Hàm Biến đổi Đặc trưng
Sử dụng Makefile hoặc chạy trực tiếp Pytest:

```bash
make test
# Hoặc chạy lệnh trực tiếp:
PYTHONPATH=src pytest -v tests/
```
Toàn bộ 4 bài test case sẽ vượt qua 100% với màu xanh (`PASSED`).

### Bước 5: Chạy Pipeline Huấn luyện & Sinh Model Artifact Manifest
Thực thi script huấn luyện mô hình Random Forest trên dữ liệu synthetic:

```bash
make train
# Hoặc chạy lệnh trực tiếp:
PYTHONPATH=src python3 src/churn/train.py --config configs/train_churn.yaml
```

Quan sát tệp Model Manifest tự động được sinh ra tại `models/manifests/model_manifest.yaml`:
```bash
cat models/manifests/model_manifest.yaml
```
Bạn sẽ thấy đầy đủ thông tin về:
- Mã băm Git Commit SHA hiện tại.
- Trạng thái `working_tree_dirty` (true/false).
- Mã băm SHA-256 của tập dữ liệu huấn luyện.
- Các chỉ số đánh giá PR-AUC, ROC-AUC và kết luận Quality Gate.

### Bước 6: Thực hiện Commit Khởi tạo Dự án Chuẩn Conventional Commits
Đưa toàn bộ dự án vào Staging Area và tạo commit nguyên tử đầu tiên:

```bash
git add .
git commit -m "chore(scaffold): initialize enterprise churn prediction repository"
```

Xem đồ thị commit trực quan:
```bash
git log --oneline --graph --decorate
```

---

## 3. Các Lệnh Tự động hóa Thông dụng (Makefile Cheatsheet)

| Lệnh | Ý nghĩa |
| :--- | :--- |
| `make install` | Cài đặt trọn bộ package và thư viện phát triển |
| `make test` | Chạy toàn bộ Unit Tests trong thư mục `tests/` |
| `make lint` | Kiểm tra vi phạm chuẩn code PEP 8 với Flake8 |
| `make format` | Tự động căn chỉnh format code với Ruff |
| `make train` | Huấn luyện mô hình và cập nhật tệp Manifest |
| `make clean` | Xóa các thư mục cache `.pytest_cache`, `__pycache__` |

---

## 4. Tiêu chí Hoàn thành (Definition of Done)
1. Thư mục được khởi tạo thành Git repo với nhánh chính `main`.
2. `make test` chạy thành công 4/4 bài test.
3. `make train` chạy thành công và xuất ra tệp `models/manifests/model_manifest.yaml` có chứa mã băm SHA-256 dữ liệu và Git SHA.
4. Lịch sử commit tuân thủ quy ước Conventional Commits (`chore:`, `feat:`, `test:`).
