FROM python:3.11
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    ffmpeg \
    gcc \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libdrm2 \
    libxshmfence1 \
    libasound2 \
    libx11-xcb1 \
    libxext6 \
    libxfixes3 \
    libgl1 \
    libxcb1 \
    fonts-liberation \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install lxml
RUN pip install wheel
RUN pip install --upgrade pip setuptools
RUN apt-get update && apt-get install -y build-essential
RUN python3 --version
RUN git clone https://github.com/Silgimusicbot/SilgiUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python -m playwright install chromium
CMD ["python3", "main.py"]
