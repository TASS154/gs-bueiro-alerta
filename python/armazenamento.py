import json
import os


pasta = os.path.join(os.path.dirname(__file__), "dados")

bueiros_ex = [
    {
        "id": 1,
        "codigo": "ARI-014",
        "logradouro": "Avenida Aricanduva",
        "bairro": "Aricanduva",
        "referencia": "Margem do córrego Aricanduva",
    },
    {
        "id": 2,
        "codigo": "EST-007",
        "logradouro": "Avenida do Estado",
        "bairro": "Ipiranga",
        "referencia": "Perto do Tamanduateí",
    },
    {
        "id": 3,
        "codigo": "MOO-021",
        "logradouro": "Rua da Mooca",
        "bairro": "Mooca",
        "referencia": "Trecho da rua da Mooca",
    },
    {
        "id": 4,
        "codigo": "SAP-103",
        "logradouro": "Avenida Sapopemba",
        "bairro": "Sapopemba",
        "referencia": "Baixada da Sapopemba",
    },
    {
        "id": 5,
        "codigo": "RAD-055",
        "logradouro": "Avenida Radial Leste",
        "bairro": "Tatuapé",
        "referencia": "Embaixo da Radial Leste",
    },
]

leituras_ex = [
    {
        "id": 1,
        "bueiro_id": 2,
        "nivel_agua": 64,
        "residuos": "alto",
        "chuva": "fraca",
        "data": "2026-11-18",
        "situacao": "entupimento",
    },
    {
        "id": 2,
        "bueiro_id": 2,
        "nivel_agua": 18,
        "residuos": "baixo",
        "chuva": "sem",
        "data": "2026-11-19",
        "situacao": "livre",
    },
    {
        "id": 3,
        "bueiro_id": 1,
        "nivel_agua": 52,
        "residuos": "alto",
        "chuva": "fraca",
        "data": "2026-11-19",
        "situacao": "entupimento",
    },
    {
        "id": 4,
        "bueiro_id": 3,
        "nivel_agua": 33,
        "residuos": "medio",
        "chuva": "fraca",
        "data": "2026-11-19",
        "situacao": "atencao",
    },
    {
        "id": 5,
        "bueiro_id": 4,
        "nivel_agua": 88,
        "residuos": "alto",
        "chuva": "forte",
        "data": "2026-11-19",
        "situacao": "critico",
    },
    {
        "id": 6,
        "bueiro_id": 5,
        "nivel_agua": 30,
        "residuos": "baixo",
        "chuva": "forte",
        "data": "2026-11-19",
        "situacao": "atencao",
    },
]

notifs_ex = [
    {
        "id": 1,
        "bueiro_id": 2,
        "leitura_id": 1,
        "situacao": "entupimento",
        "prioridade": "alta",
        "status": "concluida",
        "data": "2026-11-18",
        "nivel_depois": 15,
        "resumo": "Limpeza feita na Avenida do Estado antes de alagar.",
    },
    {
        "id": 2,
        "bueiro_id": 1,
        "leitura_id": 3,
        "situacao": "entupimento",
        "prioridade": "alta",
        "status": "aberta",
        "data": "2026-11-19",
        "nivel_depois": None,
        "resumo": "ARI-014 prestes a entupir. Manda a equipe de limpeza.",
    },
    {
        "id": 3,
        "bueiro_id": 4,
        "leitura_id": 5,
        "situacao": "critico",
        "prioridade": "urgente",
        "status": "a_caminho",
        "data": "2026-11-19",
        "nivel_depois": None,
        "resumo": "SAP-103 crítico. Limpeza urgente na Sapopemba.",
    },
]


def copia(lista):
    nova = []
    for item in lista:
        nova.append(dict(item))
    return nova


def cria_pasta():
    os.makedirs(pasta, exist_ok=True)


def arq(nome):
    return os.path.join(pasta, nome)


def confere(dados, campos):
    if not isinstance(dados, list):
        return False
    for item in dados:
        if not isinstance(item, dict):
            return False
        for campo in campos:
            if campo not in item:
                return False
    return True


def grava(nome, dados):
    cria_pasta()
    caminho = arq(nome)
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
            f.write("\n")
        return True
    except OSError:
        print("Não gravou " + nome + ".")
        return False


def le_json(nome, padrao, campos):
    cria_pasta()
    caminho = arq(nome)
    if not os.path.exists(caminho):
        dados = copia(padrao)
        grava(nome, dados)
        return dados
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, json.JSONDecodeError):
        print("Não li " + nome + ". Vou recriar os exemplos.")
        dados = copia(padrao)
        grava(nome, dados)
        return dados
    if not confere(dados, campos):
        print(nome + " tá fora do formato. Vou recriar os exemplos.")
        dados = copia(padrao)
        grava(nome, dados)
        return dados
    return dados


def abre():
    bueiros = le_json(
        "bueiros.json",
        bueiros_ex,
        ("id", "codigo", "logradouro", "bairro", "referencia"),
    )
    leituras = le_json(
        "leituras.json",
        leituras_ex,
        ("id", "bueiro_id", "nivel_agua", "residuos", "chuva", "data", "situacao"),
    )
    notifs = le_json(
        "notificacoes.json",
        notifs_ex,
        (
            "id",
            "bueiro_id",
            "leitura_id",
            "situacao",
            "prioridade",
            "status",
            "data",
            "nivel_depois",
            "resumo",
        ),
    )
    return bueiros, leituras, notifs


def bota(lista, item, nome):
    lista.append(item)
    if grava(nome, lista):
        return True
    lista.pop()
    return False
