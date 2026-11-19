cortes = (35, 60, 85)
combo = (70, "alto", "forte")

sits = ("livre", "atencao", "entupimento", "critico")
lixos = ("baixo", "medio", "alto")
chuvas = ("sem", "fraca", "forte")
status_lista = ("aberta", "a_caminho", "concluida")

nome_sit = {
    "livre": "Livre",
    "atencao": "Atenção",
    "entupimento": "Entupimento iminente",
    "critico": "Crítico",
}

nome_lixo = {
    "baixo": "Baixo",
    "medio": "Médio",
    "alto": "Alto",
}

nome_chuva = {
    "sem": "Sem chuva",
    "fraca": "Chuva fraca",
    "forte": "Chuva forte",
}

nome_status = {
    "aberta": "Aberta",
    "a_caminho": "Equipe a caminho",
    "concluida": "Limpeza concluída",
}

nome_prio = {
    "nenhuma": "Nenhuma",
    "alta": "Alta",
    "urgente": "Urgente",
}

apelido_lixo = {
    "baixo": "baixo",
    "medio": "medio",
    "médio": "medio",
    "alto": "alto",
}

apelido_chuva = {
    "sem": "sem",
    "fraca": "fraca",
    "forte": "forte",
}


# só Deus sabe como djabo isso funciona
def tira_acento(txt):
    txt = txt.strip().casefold()
    bagunca = "áaàaãaâaéeêeíióoôoõoúuüuçc"
    i = 0
    saida = ""
    while i < len(txt):
        c = txt[i]
        j = 0
        achou = False
        while j < len(bagunca):
            if bagunca[j] == c:
                saida = saida + bagunca[j + 1]
                achou = True
                break
            j = j + 2
        if achou == False:
            saida = saida + c
        i = i + 1
    return saida


def igual(a, b):
    return tira_acento(a) == tira_acento(b)


def cod_ok(cod):
    if len(cod) < 3 or len(cod) > 12:
        return False
    ok = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    for c in cod:
        if c not in ok:
            return False
    return True


def classifica(nivel, lixo, chuva):
    n = float(nivel)
    corte, lixo_ruim, chuva_ruim = combo
    if n >= cortes[2] or (n >= corte and lixo == lixo_ruim and chuva == chuva_ruim):
        sit = "critico"
    elif lixo == "alto" or n >= cortes[1] or (lixo == "medio" and chuva == "forte"):
        sit = "entupimento"
    elif lixo == "medio" or n >= cortes[0] or chuva == "forte":
        sit = "atencao"
    else:
        sit = "livre"
    return {
        "situacao": sit,
        "nome": nome_sit[sit],
        "mensagem": fala(sit),
        "prioridade": prio(sit),
        "acionar": chama(sit),
    }


def fala(sit):
    match sit:
        case "livre":
            return "Escoando. Não precisa chamar ninguém."
        case "atencao":
            return "Fica de olho. Ainda não chama a limpeza."
        case "entupimento":
            return "Prestes a entupir. Chama a limpeza da prefeitura antes de alagar."
        case "critico":
            return "Crítico. A limpeza tem que sair agora."
        case _:
            return "Não deu pra classificar essa leitura."


def prio(sit):
    match sit:
        case "critico":
            return "urgente"
        case "entupimento":
            return "alta"
        case _:
            return "nenhuma"


def chama(sit):
    if sit == "entupimento" or sit == "critico":
        return True
    return False


def pega_cod(bueiros, cod):
    for b in bueiros:
        if b["codigo"].upper() == cod.upper():
            return b
    return None


def pega_id(lista, num):
    for item in lista:
        if item["id"] == num:
            return item
    return None


def ultima(leituras, id_bueiro):
    achada = None
    for leitura in leituras:
        if leitura["bueiro_id"] == id_bueiro:
            achada = leitura
    return achada


def aberta(notifs, id_bueiro):
    achada = None
    for item in notifs:
        if item["bueiro_id"] == id_bueiro and item["status"] != "concluida":
            achada = item
    return achada


def tem_notif(notifs, id_bueiro):
    for item in notifs:
        if item["bueiro_id"] == id_bueiro:
            return True
    return False


def filtra(bueiros, bairro):
    lista = []
    for b in bueiros:
        if bairro != "" and not igual(b["bairro"], bairro):
            continue
        lista.append(b)
    return lista


def prox_id(lista):
    maior = 0
    for item in lista:
        if item["id"] > maior:
            maior = item["id"]
    return maior + 1


def tira(lista, num):
    i = 0
    for item in lista:
        if item["id"] == num:
            fora = lista.pop(i)
            return fora, i
        i = i + 1
    return None, -1


def conta(lista, chave):
    d = {}
    for item in lista:
        v = item[chave]
        if v in d:
            d[v] = d[v] + 1
        else:
            d[v] = 1
    return d


def conta_sit(bueiros, leituras):
    d = {"sem_leitura": 0}
    for sit in sits:
        d[sit] = 0
    for b in bueiros:
        leitura = ultima(leituras, b["id"])
        if leitura is None:
            d["sem_leitura"] = d["sem_leitura"] + 1
        else:
            sit = leitura["situacao"]
            d[sit] = d[sit] + 1
    return d


def conta_evitou(notifs):
    total = 0
    for item in notifs:
        if item["status"] == "concluida" and item["situacao"] == "entupimento":
            total = total + 1
    return total


def conta_aberta(notifs):
    total = 0
    for item in notifs:
        if item["status"] != "concluida":
            total = total + 1
    return total


def resumo(b, resultado):
    if resultado["situacao"] == "critico":
        return "Bueiro " + b["codigo"] + " crítico. Limpeza urgente em " + b["logradouro"] + "."
    return "Bueiro " + b["codigo"] + " prestes a entupir. Manda a limpeza em " + b["logradouro"] + "."


def relatorio(bueiros, leituras, notifs):
    return {
        "total_bueiros": len(bueiros),
        "total_leituras": len(leituras),
        "por_situacao": conta_sit(bueiros, leituras),
        "por_status": conta(notifs, "status"),
        "abertas": conta_aberta(notifs),
        "evitadas": conta_evitou(notifs),
        "total_notificacoes": len(notifs),
    }
