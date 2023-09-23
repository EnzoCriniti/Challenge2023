from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Text, Integer, Nested, Search, connections

# Criamos a conexão com a instância do Elasticsearch, assumindo que ela está rodando localmente
connections.create_connection(hosts=['http://elasticsearch:9200'])

# Definimos a estrutura para a Resposta
class Resposta(Document):
    texto = Text(analyzer='standard')
    nivel_empatia = Integer()

# Definimos a estrutura para uma Pergunta
class Pergunta(Document):
    tipo = Text()                            # "Suporte" ou "Estudante"
    texto_pergunta = Text(analyzer='standard')
    respostas = Nested(Resposta)

    class Index:
        name = 'perguntas_respostas'

Pergunta.init()

# Função para criar uma nova pergunta e suas respostas
def criar_pergunta(tipo, texto_pergunta, respostas):
    pergunta = Pergunta(tipo=tipo, texto_pergunta=texto_pergunta)
    for resp_text, emp_nivel in respostas:
        pergunta.respostas.append(Resposta(texto=resp_text, nivel_empatia=emp_nivel))
    pergunta.save()

# Função para buscar perguntas similares
def busca_similaridade(tipo, query):
    s = Search(index=Pergunta._index._name).filter('term', tipo=tipo).query("match", texto_pergunta=query)
    response = s.execute()

    for hit in response:
        print(f"Pergunta: {hit.texto_pergunta}")
        for resp in hit.respostas:
            print(f"  - {resp.texto} (Empatia: {resp.nivel_empatia})")
