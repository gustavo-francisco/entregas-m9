# Ponderada 5
Neste projeto, estou aprendendo a integrar um simulador MQTT que publica e lê dados json em um broker na nuvem ao metabase para persistência e visualização dos dados.

## Passo a Passo para execução do projeto
1. Primeiro, garanta que você já possui o **Docker Instalado**.
2. Após isso, dê um pull na imagem do metabase.<br>
`docker pull metabase/metabase:latest`
3. Depois, rode o comando para configurar o volume corretamente:<br>
`docker run -d -p 3000:3000 -v "seu-caminho/Ponderada 5/metabase-data:/metabase-data" -v "seu-caminho/Ponderada 5/metabase-data:/dados.db" --name metabase metabase/metabase`<br>
Pronto! seu metabase deve estar configurado e rodando localmente. Agora, vamos partir para o MQTT.<br>
4. Entre no diretório MQTT dentro de pyTdd:<br>
`cd pyTdd/MQTT`
5. Abra um terminal e rode o comando:<br>
`python sub.py`<br>
Verifique se a conexão foi criada corretamente.
7. Abra outro terminal e rode o comando:<br>
`python pub.py`<br>
Verifique se o publisher está publicando os dados corretamente.<br>
**IMPORTANTE!**<br>
Lembrando que as credenciais do Cluster que eu criei estão dentro de uma env. Por motivos de segurança não irei compartilhar aqui dentro do repositório. Se quiser rodar pelo meu cluster, entre em contato comigo.<br>
Prontinho! o projeto deve estar rodando, com um publicador enviando as mensagens do sensores para um subscriber alocado na nuvem, que insere no banco de dados no metabase.

## Vídeo de execução do projeto


https://github.com/gustavo-francisco/entregas-m9/assets/99208114/76f8eb18-1789-400d-9003-fc7ef31cd0bc

