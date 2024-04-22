# Text-extraction Service

Python service created with FastAPI to Extraxt Text from PDf, DOC and DOCX File

CLone this repo

## Installation

```bash
sudo docker build -t my-fastapi-app .
```

## Environment Variables
```python
SENDER_APP_PASSWORD=xxxxxx
SENDER_EMAIL=xxxxxxxxx
```
Create App for password to send email to notify user.

## Run service

```bash
sudo docker run -d -p 8000:8000 
    -e "SENDER_APP_PASSWORD=xxxxxx" 
    -e "SENDER_EMAIL=xxxxxxx" 
    my-fastapi-app .
```

## Verify Servive On
```http://127.0.0.1:8000/docs```

