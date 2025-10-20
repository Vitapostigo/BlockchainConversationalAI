FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/vitapostigo00/BlockchainConversationalAI.git .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 13333

CMD ["uvicorn", "mcpServer:app", "--host", "0.0.0.0", "--port", "13333", "--reload"]