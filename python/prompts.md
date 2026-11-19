# Uso de Inteligência Artificial no Projeto

## Finalidade

A inteligência artificial foi utilizada como ferramenta de apoio durante o desenvolvimento do projeto, principalmente para pesquisa, esclarecimento de dúvidas, avaliação de decisões técnicas e análise crítica das regras de negócio e do funcionamento previsto para o sistema.

Seu uso teve caráter consultivo: as respostas serviram como referências para orientar a investigação e levantar possibilidades, não como substitutas da pesquisa, das decisões da equipe ou da validação do projeto.

## Ferramentas utilizadas

### ChatGPT (GPT)

O GPT foi utilizado para consultas e discussões sobre o problema abordado e sobre as decisões do protótipo.

### Cursor

O Cursor foi utilizado como apoio à análise do código-fonte. A ferramenta foi escolhida especialmente por facilitar a leitura conjunta de múltiplos arquivos do projeto, permitindo compreender relações entre componentes, identificar possíveis inconsistências e investigar o funcionamento geral do sistema com mais contexto.

O código Python deste repositório também foi escrito e revisado com o Cursor. A equipe confere o resultado e responde pela entrega.

## Prompts utilizados

- Levantamento de áreas afetadas por alagamentos: “Quais bairros de São Paulo alagam mais por causa de bueiro entupido? Preciso de 5 exemplos com uma referência de rua ou córrego.”
- Definição de níveis de alerta: “Um sensor que mede nível de água, quantidade de resíduo e chuva num bueiro. Como eu classifico em livre, atenção, entupimento e crítico? Pensei na divisão de 30, 60 e 90. Analise se são limites razoáveis pra protótipo.”
- Justificativa dos limites: “Por que 35, 60 e 70–85%?”
- Relação com os Objetivos de Desenvolvimento Sustentável (ODS): “O trabalho pede um indicador mensurável e os ODS relacionados. Já identifiquei 11, 9 e 13. Qual mais faz sentido pra um sistema de alerta de bueiro entupido?”
- Reavaliação da relação com o ODS 9: “Por que 9 não entra?”
- Análise de falhas e exceções: “Procure e me diga furos de regra de negócio ou de funcionamento, por exemplo se o usuário digitar errado ou o arquivo corromper?”
- Dificuldade em bugs: “Quando entro no menu, ele fica em loop infinito e trava depois de um tempo, mas não acho o por que. analise o código e me aponto o trecho e o por que de estar ocorrendo”

Essas consultas foram usadas para apoiar:

- a pesquisa inicial sobre locais e situações relacionados a alagamentos;
- a discussão e a justificativa dos limites de classificação dos estados do bueiro;
- a análise da pertinência dos ODS relacionados ao projeto;
- a identificação de possíveis falhas, entradas inválidas, arquivos corrompidos e outros cenários excepcionais que deveriam ser considerados nas regras de negócio.

As sugestões da ferramenta foram tratadas como pontos de partida para análise. Valores, classificações, referências e decisões finais devem ser conferidos e definidos de acordo com os requisitos e as condições do protótipo.

## Limites do uso de IA

As ferramentas não foram consideradas fontes definitivas nem responsáveis pelas decisões do projeto. Suas respostas foram utilizadas para levantar hipóteses, esclarecer dúvidas e apontar aspectos que mereciam investigação. A seleção das soluções e a definição das regras permaneceram sob responsabilidade da equipe.

O login na plataforma da FIAP está bloqueado. Por isso não foi possível conferir, na hora da consulta, o que estava dentro do escopo ensinado na disciplina e o que não estava.

Em resumo, a IA entrou na pesquisa, na análise das regras e na escrita do código Python. A equipe continua responsável por conferir e explicar o que foi entregue.
