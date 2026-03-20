FROM python:3.12-slim
WORKDIR /app
COPY scripts/requirements.txt scripts/
RUN pip install --no-cache-dir -r scripts/requirements.txt
COPY scripts/ scripts/
COPY docs/ docs/
ENTRYPOINT ["python3", "scripts/resume_pdf.py"]
