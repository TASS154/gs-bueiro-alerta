# Bueiro Alerta

Parte de Python do trabalho. O problema é enchente em São Paulo: o bueiro entope e a limpeza chega tarde. O programa olha a leitura e, se estiver perto de entupir, grava um chamado pra prefeitura.

## Ficha

Nome: Bueiro Alerta

Cidade: São Paulo. Exemplos em Aricanduva, Ipiranga, Mooca, Sapopemba e Tatuapé.

Cidadão: quem mora onde alaga, e a equipe de limpeza da prefeitura.

Problema: o bueiro junta resíduo e água, e a rua alaga antes de alguém limpar.

Como funciona: entra o nível da água, o resíduo e a chuva. Entupimento iminente ou crítico vira notificação.

O que esta parte faz: valida o que foi digitado, decide a situação e acompanha o chamado até a limpeza.

Link do repositório: a gente coloca na entrega.

Indicador: limpezas concluídas que foram chamadas ainda no entupimento, antes do nível crítico.

ODS: 11, 13 e 3.

O sensor é a outra parte do trabalho. Aqui a notificação fica salva no JSON. Não manda mensagem de verdade pra prefeitura.

## Rodar

Python 3.10 ou mais novo, por causa do match/case. Não instala nada.

```text
cd python
python main.py
```

Se a pasta dados não existir, o programa cria os exemplos.

## Menu

1. Cadastra bueiro (código, rua, bairro, referência).
2. Registra leitura. Se precisar de limpeza, cria a notificação.
3. Consulta um bueiro.
4. Lista, dá pra filtrar por bairro.
5. Vê as notificações.
6. Marca equipe a caminho e conclui a limpeza.
7. Relatório.
8. Remove bueiro que ainda não teve notificação.
9. Sobre.
0. Sair.

## Quando chama a limpeza

Abaixo de 35%, resíduo baixo e sem chuva forte: livre, não chama.

A partir de 35%, ou resíduo médio, ou chuva forte: atenção.

Resíduo alto, ou água a partir de 60%, ou resíduo médio com chuva forte: entupimento. Prioridade alta.

A partir de 85%, ou 70% com resíduo alto e chuva forte: crítico. Urgente.

Exemplo: 52% de água, resíduo alto, chuva fraca. Ainda não transbordou, mas já chama a limpeza.

Pra concluir, a equipe precisa estar a caminho e o nível depois da limpeza tem que ficar abaixo de 60%. Se já tem chamado aberto naquele bueiro, não cria outro.

Essa escala é do protótipo. Não é regra da prefeitura nem da Defesa Civil.

## Dados

dados/bueiros.json, dados/leituras.json e dados/notificacoes.json. Exemplo e o que for cadastrado no programa. Sem nome, telefone ou documento.

main.py é o menu. regras.py decide. armazenamento.py grava o JSON.
