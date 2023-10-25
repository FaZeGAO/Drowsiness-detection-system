FROM python:3.9.2-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y libasound2-plugins festival nano htop \
    ffmpeg \
    libasound2-dev \
    alsa-utils\
    mpg321\
    lame

COPY festvox-ellpc11k_1.95-1_all.deb /app/

RUN dpkg -i festvox-ellpc11k_1.95-1_all.deb

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi==0.100.0\
    uvicorn==0.23.1\
    pydantic==2.1.1

CMD ["uvicorn", "aplicacion:app", "--host", "0.0.0.0", "--port", "80"]