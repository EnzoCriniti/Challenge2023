from flask import Flask, request, jsonify, make_response
from translate import Translator
from database import CustomElasticsearchORM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

host = 'http://challenge2023fiap_elasticsearch_1:9200'
username = 'elastic'
password = '123'

orm = CustomElasticsearchORM(host, username, password)

translator_pt_en = Translator(provider='mymemory', from_lang='pt', to_lang='en')
translator_en_pt = Translator(provider='mymemory', from_lang='en', to_lang='pt')

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

def get_most_similar_response(user_input, empathia):
    try:
        # Obtenha os resultados do Elasticsearch
        results = orm.get_document_by_similarity("supportbot", user_input, empathia, n=3)
        
        # Organizando as respostas e suas pontuações em listas separadas
        responses = [list(item.values())[0][1] for item in results]
        es_scores = [list(item.values())[0][2] for item in results]
        
        # Calculando a similaridade do cosseno entre a entrada do usuário e as respostas da API
        vectorizer = TfidfVectorizer().fit_transform([user_input] + responses)
        cosine_similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()
        
        # Ponderando as similaridades: 0.5 * similaridade_cosseno + 0.5 * similaridade_elasticsearch
        weighted_similarities = [0.5 * cosine + 0.5 * es for cosine, es in zip(cosine_similarities, es_scores)]
        
        # Encontrando a resposta com a maior similaridade ponderada
        best_response_index = weighted_similarities.index(max(weighted_similarities))
        best_response = responses[best_response_index]
        
        return safe_translate(best_response, 'en-pt')

    except Exception as e:
        print(f"Erro: {e}")  
        return "Desculpe mas ainda não fui treinado para responder a esse tipo de pergunta."

@app.route('/sendMessage', methods=['POST'])
def send_message():
    print('Recebi uma requisição!')
    user_message = request.json.get('message')
    empathia = request.json.get('sentiment')

    translated_message = safe_translate(str(user_message), 'pt-en')
    
    bot_response = get_most_similar_response(translated_message, empathia)

    return jsonify({'botResponse': bot_response})
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
