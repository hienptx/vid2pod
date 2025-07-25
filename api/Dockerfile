FROM python:3.11-slim

WORKDIR /app

# Install build dependencies for whisper.cpp
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Clone and build whisper.cpp
# RUN git clone https://github.com/ggerganov/whisper.cpp.git && \
#     cd whisper.cpp && make

# # Download whisper.cpp model (base.en)
# RUN mkdir -p models && \
#     wget -O models/ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
