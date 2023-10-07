install:
	poetry install
	pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
	pip install easyocr pytesseract
install_without_cuda:
	poetry install
	pip install easyocr pytesseract
update:
	poetry update
	pip install --upgrade torch torchvision pytesseract easyocr