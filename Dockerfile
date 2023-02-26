FROM python:3.10-alpine
WORKDIR /app

ARG BUILD_VERSION=0.1.0
ARG GIT_COMMIT=unknown

LABEL org.opencontainers.image.version="${BUILD_VERSION}"\
      org.opencontainers.image.revision="${GIT_COMMIT}"

COPY . .
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]