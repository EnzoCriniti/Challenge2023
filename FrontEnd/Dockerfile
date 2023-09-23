# Dockerfile (frontend/Dockerfile)

FROM python:3.9

WORKDIR /app-frontend

# Copia o conteúdo do diretório atual (onde o Dockerfile está localizado) para o diretório de trabalho /app-backend
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]
