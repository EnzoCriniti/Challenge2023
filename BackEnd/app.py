from flask import Flask, request, jsonify, make_response
from translate import Translator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

app = Flask(__name__)

#openai.api_key = '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'

translator_pt_en = Translator(provider='mymemory', from_lang='pt', to_lang='en')
translator_en_pt = Translator(provider='mymemory', from_lang='en', to_lang='pt')

# Carregando os dados do arquivo JSON
with open('data.json', 'r') as file:
    data = json.load(file)

def safe_translate(message, type):
    # Dividindo a mensagem em segmentos de 500 caracteres ou menos
    segments = [message[i:i+500] for i in range(0, len(message), 500)]
    
    if type == 'pt-en':
        # Traduzindo cada segmento individualmente
        translated_segments = [translator_pt_en.translate(segment) for segment in segments]
    else:
        # Traduzindo cada segmento individualmente
        translated_segments = [translator_en_pt.translate(segment) for segment in segments]
    # Combinando os segmentos traduzidos
    return ''.join(translated_segments)

def get_most_similar_response(user_input):
    all_patterns = [pattern for intent in data["intents"] for pattern in intent["patterns"]]
    vectorizer = TfidfVectorizer().fit_transform(all_patterns + [user_input])
    vectors = vectorizer.toarray()

    cosine_similarities = cosine_similarity(vectors[-1:], vectors[:-1])
    index_of_most_similar = cosine_similarities.argmax()

    for intent in data["intents"]:
        if all_patterns[index_of_most_similar] in intent["patterns"]:
            return safe_translate(intent["responses"][0], 'en-pt')  # Aqui, estamos retornando a primeira resposta. Você pode escolher uma resposta aleatória ou implementar outra lógica.

    return "Desculpe, eu não entendi."

@app.route('/sendMessage', methods=['POST'])
def send_message():
    print('Recebi uma requisição!')
    user_message = request.json.get('message')
    sentimento = request.json.get('sentimental')
    # Traduzindo a mensagem para inglês
    translated_message = safe_translate(str(user_message), 'pt-en')
    
    # Aqui você pode processar a mensagem do usuário e gerar uma resposta.
    # Por simplicidade, vamos apenas retornar uma resposta padrão.
    bot_response = get_most_similar_response(translated_message)

    return jsonify({'botResponse': bot_response})
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
