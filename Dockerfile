FROM python:3.8.5-slim-buster as builder
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.8.5-slim-buster as app
WORKDIR /app/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY *.py /app/
CMD ["gunicorn", "--bind", "127.0.0.1:3000", "app:flask_app"]