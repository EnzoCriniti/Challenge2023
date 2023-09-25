from flask import Flask, render_template, request, jsonify
import requests
import json
from classificador import classify_messages
from transformers import pipeline
import spacy
from collections import Counter


app = Flask(__name__)

# Inicialize o pipeline de análise de sentimentos uma única vez
classifier = pipeline('sentiment-analysis')

# Carregando o modelo de linguagem em português
nlp = spacy.load('pt_core_news_sm')

def is_complex_message(message: str) -> bool:
    """
    Verifica se uma mensagem é complexa com base em regras predefinidas e análise NLP.

    Args:
    - message (str): A mensagem a ser analisada.

    Returns:
    - bool: Verdadeiro se a mensagem for complexa, falso caso contrário.
    """

    # Análise NLP da mensagem
    doc = nlp(message)

    # Regra 1: Verifica o número de pontos de interrogação.
    if message.count('?') > 1:
        return True

    # Regra 2: Verifica se a mensagem é muito longa.
    if len(doc) > 20:
        return True

    # Regra 3: Verifica a complexidade da estrutura gramatical da mensagem.
    pos_counts = Counter(token.pos_ for token in doc)
    if pos_counts.get('VERB', 0) > 2 or pos_counts.get('NOUN', 0) > 4:
        return True

    # Regra 4: Verifica se a mensagem contém entidades nomeadas (por exemplo, nomes de pessoas, lugares, organizações).
    if len(doc.ents) > 2:
        return True

    # Regra 5: Verifica se a mensagem não contém palavras-chave típicas de perguntas.
    question_words = ["quem", "o que", "onde", "quando", "por que", "como"]
    if not any(token.text.lower() in question_words for token in doc):
        return False

    # Regra 6: Verifica se a mensagem contém subordinadas (indicativo de complexidade na sentença).
    if any(token.dep_ in ['ccomp', 'xcomp'] for token in doc):
        return True

    # Se nenhuma das regras acima se aplicar, considere a mensagem como simples.
    return False

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
    type_chat = data['type']
    
    with open('chat.json', 'r+', encoding='utf-8') as file:
        data = json.load(file)
        mensagens = data['mensagens']
        mensagens.append(user_message)
        file.seek(0)  # Volte ao início do arquivo
        json.dump(data, file)
        file.truncate()  # Remova qualquer conteúdo após a posição atual no arquivo

    
    # Obtenha o sentimento da mensagem do usuário
    sentiment_response = classify_messages(classifier)
    desc = {'NEGATIVO': "3", 'NEUTRO': "2", 'POSITIVO': "1"}
    sentiment_response = desc[sentiment_response] 

    # Define a URL da API
    api_url = "http://backend:3000/sendMessage"
        
    # Envia a mensagem para a API
    response = requests.post(api_url, json={"message": user_message, "sentiment": sentiment_response})

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        result = response.json()['botResponse']
        # Obtém a complexidade da mensagem
        is_complex = is_complex_message(user_message)
        print(is_complex)
    else:
        result = "Erro ao comunicar com a API"
    
    # Retorna a resposta para o usuário
    return jsonify({"response": result, "type": type_chat, "isComplex": is_complex})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

