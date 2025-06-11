FROM python:3.11
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    libxshmfence1 \
    libx11-xcb1 \
    libdrm2 \
    libxfixes3 \
    libxext6 \
    libxrender1 \
    libxi6 \
    ffmpeg \
    && apt-get clean
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
RUN playwright install chromium
CMD ["python3", "main.py"]
