FROM python:3.8
ENV APP_HOME /app
ENV PORT 8000

WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y antiword

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
