.PHONY: help install lint format test train clean

help:
	@echo "======================================================================"
	@echo "                   MLOPS LAB-1 AUTOMATION COMMANDS                   "
	@echo "======================================================================"
	@echo "  make install    - Cài đặt package và môi trường dev"
	@echo "  make lint       - Kiểm tra chuẩn cú pháp code với Flake8"
	@echo "  make format     - Tự động chuẩn hóa format với Ruff"
	@echo "  make test       - Chạy bộ Unit Tests với Pytest"
	@echo "  make train      - Chạy pipeline huấn luyện mô hình và xuất Manifest"
	@echo "  make clean      - Dọn dẹp cache, bytecode và artifacts tạm"

install:
	pip install --upgrade pip
	pip install -e ".[dev]"

lint:
	flake8 src tests --max-line-length=100 --extend-ignore=E203,W503

format:
	ruff format src tests

test:
	PYTHONPATH=src pytest -v tests/

train:
	PYTHONPATH=src python3 src/churn/train.py --config configs/train_churn.yaml

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
