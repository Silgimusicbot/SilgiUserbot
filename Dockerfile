FROM python:3.11
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    ffmpeg \
    gcc \
    wget \
    gnupg \
    ca-certificates \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libgtk-4-1 \
    libgstreamer1.0-0 \
    libgraphene-1.0-0 \
    libwoff1 \
    libwoff2-1 \
    libwoff2dec0 \
    libgstallocators-1.0-0 \
    libgstapp-1.0-0 \
    libgstbase-1.0-0 \
    libgstpbutils-1.0-0 \
    libgstaudio-1.0-0 \
    libgsttag-1.0-0 \
    libgstvideo-1.0-0 \
    libgstgl-1.0-0 \
    libgstcodecparsers-1.0-0 \
    libgstfft-1.0-0 \
    libavif15 \
    libharfbuzz-icu0 \
    libenchant-2-2 \
    libsecret-1-0 \
    libhyphen0 \
    libmanette-0.2-0 \
    libgles2 \
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
