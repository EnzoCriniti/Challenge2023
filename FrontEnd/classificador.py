import json

def classify_messages(classifier):
    
    with open('chat.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        mensagens = data['mensagens']
        
        score_positivo = 0
        score_negativo = 0
        score_neutro = 0
        
        for mensagem in mensagens:
            resultado = classifier(mensagem)[0]
            print(resultado)
            
            if resultado["label"] == "POSITIVE":
                if resultado["score"] >= 0.6:
                    score_positivo += 1
                else:
                    score_neutro += 1
            else:
                if resultado["score"] >= 0.6:
                    score_negativo += 1
                else:
                    score_neutro += 1
        
        # Avaliação geral
        if score_positivo > max(score_negativo, score_neutro):
            return "POSITIVO"
        elif score_negativo > max(score_positivo, score_neutro):
            return "NEGATIVO"
        else:
            return "NEUTRO"


