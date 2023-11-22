install:
	poetry install
	pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
	pip install easyocr
install_without_cuda:
	poetry install
	pip install easyocr
update:
	poetry update
	pip install --upgrade torch torchvision easyocr
loc_badge:
	@git ls-files | grep '\.py' | xargs wc -l | grep -oE '[0-9]+' | tail -1 | xargs -I {} -t echo "https://img.shields.io/badge/total_lines-{}-blue?color=%235429FE"
