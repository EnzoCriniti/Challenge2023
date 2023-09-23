from flask import Flask, render_template, request, jsonify
import requests
import json
from classificador import classify_messages
from transformers import pipeline

app = Flask(__name__)

# Inicialize o pipeline de análise de sentimentos uma única vez
classifier = pipeline('sentiment-analysis')

@app.route('/getSentiment')
def get_sentiment():
    sentimento = classify_messages(classifier)
    return jsonify({"sentimento": sentimento})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sendMessage', methods=['POST'])
def send_message():
    # Pega a mensagem do usuário
    data = request.get_json()  
    user_message = data['message']
    
    # Armazenando mensagem no json chat.json
    with open('chat.json', 'r+', encoding='utf-8') as file:
        data = json.load(file)
        mensagens = data['mensagens']
        mensagens.append(user_message)
        file.seek(0)
        json.dump(data, file)    
    
    # Obtenha o sentimento da mensagem do usuário
    sentiment_response = classify_messages(classifier)
    
    # Define a URL da API
    api_url = "http://backend:3000/sendMessage"
        
    # Envia a mensagem para a API
    response = requests.post(api_url, json={"message": user_message, "sentiment": sentiment_response})

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        result = response.json()['botResponse']
        
    else:
        result = "Erro ao comunicar com a API"
    
    # Retorna a resposta para o usuário
    return jsonify({"response": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

