from elasticsearch import Elasticsearch
from datetime import datetime

class CustomElasticsearchORM:
    def __init__(self, host, username, password):
        self.connection = self.create_connection(host, username, password)

    def create_connection(self, host, username, password):
        es = Elasticsearch(
            hosts=[host],
            basic_auth=(username, password))
        return es

    def create_document(self, index, document):
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        document['timestamp'] = formatted_date  # Adiciona um campo de data/hora ao documento
        res = self.connection.index(index=index, document=document)
        if res['result'] == 'created':
            print(f"Documento inserido com sucesso em {formatted_date}")
        return res['result']
    

    def get_document_by_similarity(self, index, question, empathia, n=3, min_similarity=1.0):
        # Corrige a consulta para usar "match" no campo "question"
        res = self.connection.search(
            index=index, 
            query={"match": {"question": question}})
        # Classifica os resultados com base na similaridade da pergunta
        results = sorted(res['hits']['hits'], key=lambda x: x['_score'], reverse=True)
        # Obtém apenas as respostas com base na empatia fornecida
        filtered_results = [result for result in results if result['_source']['answer'][0].get(empathia)]
        
        # Filtra resultados com similaridade maior ou igual a min_similarity
        filtered_results = [result for result in filtered_results if result['_score'] >= min_similarity]
        
        if not filtered_results:
            raise Exception("Desculpe mas ainda não fui treinado para responder a esse tipo de pergunta.")
        
        # Limita os resultados aos top N
        top_n_results = filtered_results[:n]
        
        # Formata os resultados como um dicionário {índice: [resposta, similaridade]}
        formatted_results = {}
        for idx, result in enumerate(top_n_results, 1):
            resposta = result['_source']['answer'][0][empathia]
            similaridade = result['_score']
            formatted_results[idx] = [resposta, similaridade]
        
        return formatted_results



#if __name__ == "__main__":
    #host = 'http://challenge2023fiap_elasticsearch_1:9200'
    #username = 'elastic'
    #password = '123'

    #orm = CustomElasticsearchORM(host, username, password)

    # Nome do arquivo JSON
    #json_file = 'database.json'

    #with open(json_file, 'r') as file:
        #documents = json.load(file)

    #for document_id, document_data in documents.items():
        #index_name = "supportbot"  # Substitua pelo nome do índice desejado
        #result = orm.create_document(index_name, document_data)
        #print(f"Documento {document_id} inserido com resultado: {result}")

    # Exemplo de uso: Retornar os top 3 documentos com a pergunta "O que é depressão?" com empatia 1
    #results = orm.get_document_by_similarity("supportbot", "Doze mola carai", "1", n=3)
    #print(results)
    #for idx, (resposta, similaridade) in results.items():
        #print(f"Documento {idx}:")
        #print(f"Resposta: {resposta}")
        #print(f"Similaridade: {similaridade}")
        #print()