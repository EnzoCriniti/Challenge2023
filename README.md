# ChatBot Web App with Elasticsearch:

Este projeto consiste em uma aplicação web que utiliza Docker para orquestrar os containers de frontend, backend, Elasticsearch e Nginx. A aplicação permite que os usuários interajam com um chatbot que responde a perguntas armazenadas em um índice Elasticsearch.

Tecnologias Utilizadas:

Docker: Utilizado para criar e gerenciar os containers da aplicação.
Flask: Framework Python para desenvolver o frontend da aplicação web.
Elasticsearch: Usado para armazenar e buscar perguntas e respostas com base em similaridade.
Nginx: Utilizado como servidor web e proxy reverso para direcionar o tráfego para o frontend.
Certbot: Ferramenta para configuração de certificados SSL/TLS e garantir a segurança da aplicação.
Estrutura do Projeto:

Challenge2023FIAP/
BackEnd/
app.py
...
FrontEnd/
app.py
...
nginx.conf
docker-compose.yml
README.md
Como Executar:

#Pré-requisitos:

Docker instalado na máquina local.
Certbot instalado para configurar certificados SSL/TLS.
Passos para Executar:

Clone o repositório para a sua máquina local:
bash
Copy code
git clone https://github.com/SeuNome/SeuRepositorio.git
cd Challenge2023FIAP
Execute o Docker Compose para criar e iniciar os containers:
Copy code
docker-compose up -d
Isso iniciará os containers do frontend, backend, Elasticsearch e Nginx.

Configure o Certbot para gerar certificados SSL/TLS para o seu domínio (substitua seu_dominio pelo seu domínio real):
css
Copy code
certbot certonly --webroot -w /var/www/html -d seu_dominio
Atualize o arquivo nginx.conf com as configurações SSL/TLS corretas:
bash
Copy code
# Configurações SSL
ssl_certificate /etc/letsencrypt/live/seu_dominio/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/seu_dominio/privkey.pem;

Reinicie o container do Nginx para aplicar as configurações atualizadas:
Copy code
docker restart Challenge2023FIAP_nginx_1
Agora sua aplicação deve estar em execução e acessível em https://seu_dominio.

# Uso da Aplicação:

Acesse a aplicação em https://seu_dominio.
Interaja com o chatbot para fazer perguntas e obter respostas com base na busca por similaridade em perguntas armazenadas no Elasticsearch.

Contribuição:

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novos recursos. Basta abrir um Pull Request!




