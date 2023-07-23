install:
	poetry install
	pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
	pip install easyocr pytesseract
	pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
	pip install paddleocr
update:
	poetry update
	pip install --upgrade torch torchvision torchaudio easyocr pytesseract paddlepaddle paddleocr