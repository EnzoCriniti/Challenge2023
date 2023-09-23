# Dockerfile (backend/Dockerfile)

FROM python:3.9

WORKDIR /app-backend

# Copia o conteúdo do diretório atual (onde o Dockerfile está localizado) para o diretório de trabalho /app-backend
COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]

