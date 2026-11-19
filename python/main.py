from datetime import date

import armazenamento
import regras


opcoes = (
    ("1", "Cadastrar bueiro"),
    ("2", "Registrar leitura"),
    ("3", "Consultar um bueiro"),
    ("4", "Listar bueiros"),
    ("5", "Ver notificações"),
    ("6", "Atualizar notificação"),
    ("7", "Relatório"),
    ("8", "Remover bueiro"),
    ("9", "Sobre"),
    ("0", "Sair"),
)


def le(msg):
    try:
        return input(msg).strip()
    except EOFError:
        print()
        return None


def le_txt(msg, minimo):
    while True:
        txt = le(msg)
        if txt is None:
            return None
        if len(txt) < minimo:
            print("Digite pelo menos " + str(minimo) + " caracteres.")
            continue
        return txt


def le_num(msg, minimo, maximo):
    while True:
        txt = le(msg)
        if txt is None:
            return None
        try:
            n = float(txt.replace(",", "."))
        except ValueError:
            print("Digite um número. Exemplo: 52 ou 52,5")
            continue
        if n < minimo or n > maximo:
            print("Tem que ficar entre " + str(minimo) + " e " + str(maximo) + ".")
            continue
        return n


def le_int(msg):
    while True:
        txt = le(msg)
        if txt is None:
            return None
        try:
            return int(txt)
        except ValueError:
            print("Digite um número inteiro. Exemplo: 2")


def le_sn(msg):
    while True:
        txt = le(msg)
        if txt is None:
            return None
        r = txt.casefold()
        if r in ("s", "sim"):
            return "s"
        if r in ("n", "nao", "não"):
            return "n"
        print("Responde S ou N.")


def le_cod(msg):
    while True:
        txt = le(msg)
        if txt is None:
            return None
        cod = txt.upper().replace(" ", "")
        if regras.cod_ok(cod):
            return cod
        print("De 3 a 12 caracteres, letra, número e hífen. Exemplo: ARI-014")


def le_opc(msg, lista, apelidos):
    print("Opções: " + ", ".join(lista))
    while True:
        txt = le(msg)
        if txt is None:
            return None
        chave = txt.casefold()
        if chave in apelidos:
            return apelidos[chave]
        print("Não entendi. Usa: " + ", ".join(lista))


def espera():
    le("Enter pra voltar.")


def separa(txt):
    print()
    print("-" * 40)
    print(txt)
    print("-" * 40)


def pct(v):
    n = float(v)
    if n == int(n):
        return str(int(n)) + "%"
    s = "%.1f" % n
    return s.replace(".", ",") + "%"


def qtd_txt(qtd, um, varios):
    if qtd == 1:
        return "1 " + um
    return str(qtd) + " " + varios


def menu():
    separa("Bueiro Alerta")
    print("Vê se o bueiro vai entupir e chama a limpeza.")
    print()
    for cod, nome in opcoes:
        print(cod + " - " + nome)
    print()


def escala():
    print("Resíduo alto, água de " + str(regras.cortes[1]) + "% pra cima, ou chuva forte com resíduo médio: limpeza")
    print("Água de " + str(regras.cortes[2]) + "% pra cima, ou " + str(regras.combo[0]) + "% com resíduo alto e chuva forte: crítico")
    print("No resto, com algum sinal, só observa")


def linha_bueiro(b, leituras):
    leitura = regras.ultima(leituras, b["id"])
    if leitura is None:
        sit = "Sem leitura"
    else:
        sit = regras.nome_sit[leitura["situacao"]] + " (" + pct(leitura["nivel_agua"]) + ")"
    return "#" + str(b["id"]) + " " + b["codigo"] + " - " + b["logradouro"] + " - " + b["bairro"] + " - " + sit


def mostra_bueiros(bueiros, leituras):
    if len(bueiros) == 0:
        print("Nenhum bueiro.")
        return
    for b in bueiros:
        print(linha_bueiro(b, leituras))


def linha_notif(item, bueiros):
    b = regras.pega_id(bueiros, item["bueiro_id"])
    if b is None:
        onde = "bueiro sumiu"
    else:
        onde = b["codigo"] + " - " + b["bairro"]
    return (
        "#"
        + str(item["id"])
        + " "
        + onde
        + " - "
        + regras.nome_sit[item["situacao"]]
        + " - "
        + regras.nome_prio[item["prioridade"]]
        + " - "
        + regras.nome_status[item["status"]]
    )


def cadastra(bueiros):
    separa("Cadastrar bueiro")
    cod = le_cod("Código (exemplo ARI-014): ")
    if cod is None:
        return
    if regras.pega_cod(bueiros, cod) is not None:
        print("Já tem bueiro com esse código.")
        espera()
        return
    rua = le_txt("Logradouro: ", 5)
    if rua is None:
        return
    bairro = le_txt("Bairro: ", 3)
    if bairro is None:
        return
    ref = le_txt("Referência: ", 5)
    if ref is None:
        return
    item = {
        "id": regras.prox_id(bueiros),
        "codigo": cod,
        "logradouro": rua,
        "bairro": bairro,
        "referencia": ref,
    }
    if armazenamento.bota(bueiros, item, "bueiros.json"):
        print("Bueiro salvo com o número #" + str(item["id"]) + ".")
        print(item["codigo"] + " - " + item["logradouro"] + " - " + item["bairro"])
    espera()


def nova_leitura(bueiros, leituras, notifs):
    separa("Registrar leitura")
    escala()
    cod = le_cod("Código do bueiro: ")
    if cod is None:
        return
    b = regras.pega_cod(bueiros, cod)
    if b is None:
        print("Não achei esse bueiro. Cadastra ele antes.")
        espera()
        return
    nivel = le_num("Nível da água, de 0 a 100: ", 0, 100)
    if nivel is None:
        return
    lixo = le_opc("Resíduos: ", regras.lixos, regras.apelido_lixo)
    if lixo is None:
        return
    chuva = le_opc("Chuva: ", regras.chuvas, regras.apelido_chuva)
    if chuva is None:
        return

    resultado = regras.classifica(nivel, lixo, chuva)
    leitura = {
        "id": regras.prox_id(leituras),
        "bueiro_id": b["id"],
        "nivel_agua": nivel,
        "residuos": lixo,
        "chuva": chuva,
        "data": date.today().isoformat(),
        "situacao": resultado["situacao"],
    }
    if not armazenamento.bota(leituras, leitura, "leituras.json"):
        espera()
        return

    print()
    print(b["codigo"] + " ficou em " + resultado["nome"] + " (" + pct(nivel) + ").")
    print(resultado["mensagem"])
    if resultado["acionar"]:
        ja = regras.aberta(notifs, b["id"])
        if ja is not None:
            print("Já existe a notificação #" + str(ja["id"]) + " em aberto. Nenhuma nova chamada foi criada.")
        else:
            nota = {
                "id": regras.prox_id(notifs),
                "bueiro_id": b["id"],
                "leitura_id": leitura["id"],
                "situacao": resultado["situacao"],
                "prioridade": resultado["prioridade"],
                "status": "aberta",
                "data": date.today().isoformat(),
                "nivel_depois": None,
                "resumo": regras.resumo(b, resultado),
            }
            if armazenamento.bota(notifs, nota, "notificacoes.json"):
                print("Notificação #" + str(nota["id"]) + " registrada para a prefeitura.")
                print(nota["resumo"])
    espera()


def consulta(bueiros, leituras, notifs):
    separa("Consultar bueiro")
    cod = le_cod("Código do bueiro: ")
    if cod is None:
        return
    b = regras.pega_cod(bueiros, cod)
    if b is None:
        print("Não achei esse bueiro.")
        espera()
        return
    print(linha_bueiro(b, leituras))
    print("Referência: " + b["referencia"])
    leitura = regras.ultima(leituras, b["id"])
    if leitura is None:
        print("Sem leitura ainda.")
    else:
        print(
            "Última, "
            + leitura["data"]
            + ": água "
            + pct(leitura["nivel_agua"])
            + ", resíduos "
            + regras.nome_lixo[leitura["residuos"]]
            + ", "
            + regras.nome_chuva[leitura["chuva"]]
            + "."
        )
        print(regras.fala(leitura["situacao"]))
    ja = regras.aberta(notifs, b["id"])
    if ja is None:
        print("Sem notificação aberta.")
    else:
        print(linha_notif(ja, bueiros))
        print(ja["resumo"])
    espera()


def lista(bueiros, leituras):
    separa("Listar bueiros")
    bairro = le("Bairro (Enter lista todos): ")
    if bairro is None:
        return
    achados = regras.filtra(bueiros, bairro)
    print(qtd_txt(len(achados), "bueiro encontrado.", "bueiros encontrados."))
    mostra_bueiros(achados, leituras)
    espera()


def ver_notif(notifs, bueiros):
    separa("Notificações")
    if len(notifs) == 0:
        print("Nenhuma notificação.")
        espera()
        return
    for item in notifs:
        print(linha_notif(item, bueiros))
        print("  " + item["resumo"])
    espera()


def atualiza(notifs, bueiros):
    separa("Atualizar notificação")
    print("Ainda sem concluir:")
    qtd = 0
    for item in notifs:
        if item["status"] != "concluida":
            print(linha_notif(item, bueiros))
            qtd = qtd + 1
    if qtd == 0:
        print("Nada em aberto.")
        espera()
        return
    print()
    print("1 - equipe a caminho")
    print("2 - concluir limpeza")
    num = le_int("Número da notificação: ")
    if num is None:
        return
    item = regras.pega_id(notifs, num)
    if item is None:
        print("Não achei essa notificação.")
        espera()
        return
    if item["status"] == "concluida":
        print("Essa já foi concluída.")
        espera()
        return
    acao = le("Ação: ")
    if acao is None:
        return

    match acao:
        case "1":
            if item["status"] != "aberta":
                print("A equipe já saiu. Quando terminar, conclui a limpeza.")
                espera()
                return
            antes = item["status"]
            item["status"] = "a_caminho"
            if armazenamento.grava("notificacoes.json", notifs):
                print("Equipe marcada como a caminho da notificação #" + str(item["id"]) + ".")
            else:
                item["status"] = antes
        case "2":
            if item["status"] != "a_caminho":
                print("Só conclui depois que a equipe estiver a caminho.")
                espera()
                return
            nivel = le_num("Nível da água depois da limpeza (0 a 100): ", 0, 100)
            if nivel is None:
                return
            if nivel >= regras.cortes[1]:
                print("Ainda tá em " + pct(nivel) + ". A limpeza não foi concluída.")
                print("Se mudou, registra outra leitura.")
                espera()
                return
            ok = le_sn("Confirma que limpou? (S/N): ")
            if ok != "s":
                print("Cancelado.")
                espera()
                return
            antes = item["status"]
            nivel_antes = item["nivel_depois"]
            item["status"] = "concluida"
            item["nivel_depois"] = nivel
            if armazenamento.grava("notificacoes.json", notifs):
                print("Limpeza da notificação #" + str(item["id"]) + " concluída.")
                if item["situacao"] == "entupimento":
                    print("Saiu antes do crítico, conta como enchente evitada.")
            else:
                item["status"] = antes
                item["nivel_depois"] = nivel_antes
        case _:
            print("Ação inválida. Usa 1 ou 2.")
    espera()


def mostra_relatorio(bueiros, leituras, notifs):
    separa("Relatório")
    r = regras.relatorio(bueiros, leituras, notifs)
    print(qtd_txt(r["total_bueiros"], "bueiro.", "bueiros."))
    print(qtd_txt(r["total_leituras"], "leitura.", "leituras."))
    print("Situação agora:")
    por_sit = r["por_situacao"]
    for sit in regras.sits:
        print("  " + regras.nome_sit[sit] + ": " + str(por_sit[sit]))
    print("  Sem leitura: " + str(por_sit["sem_leitura"]))
    print("Notificação:")
    for st in regras.status_lista:
        n = 0
        if st in r["por_status"]:
            n = r["por_status"][st]
        print("  " + regras.nome_status[st] + ": " + str(n))
    print(
        "Indicador: "
        + str(r["evitadas"])
        + " limpeza(s) concluída(s) no entupimento, antes do crítico."
    )
    print(str(r["abertas"]) + " ainda sem conclusão.")
    espera()


def remove(bueiros, leituras, notifs):
    separa("Remover bueiro")
    mostra_bueiros(bueiros, leituras)
    if len(bueiros) == 0:
        espera()
        return
    num = le_int("Número pra remover: ")
    if num is None:
        return
    alvo = regras.pega_id(bueiros, num)
    if alvo is None:
        print("Não achei esse número.")
        espera()
        return
    if regras.tem_notif(notifs, alvo["id"]):
        print("Esse já tem notificação. O histórico fica.")
        espera()
        return
    print(linha_bueiro(alvo, leituras))
    ok = le_sn("Remove mesmo? (S/N): ")
    if ok != "s":
        print("Cancelado.")
        espera()
        return
    fora, i = regras.tira(bueiros, num)
    if fora is None:
        print("Não achei esse número.")
        espera()
        return
    if armazenamento.grava("bueiros.json", bueiros):
        print("Bueiro removido: " + fora["codigo"] + ".")
    else:
        bueiros.insert(i, fora)
        print("Não gravou. O bueiro continua.")
    espera()


def sobre():
    separa("Sobre")
    print("Serve pra morador de área que alaga em São Paulo")
    print("e pra equipe de limpeza da prefeitura.")
    print("O bueiro entope e a enchente chega antes da limpeza.")
    print("Aqui a leitura vira decisão e vira notificação.")
    print("Sensor fica na outra parte. Os dados daqui são exemplo.")
    print("ODS 11 cidades, ODS 13 clima, ODS 3 saúde.")
    espera()


def faz(escolha, bueiros, leituras, notifs):
    match escolha:
        case "0":
            return False
        case "1":
            cadastra(bueiros)
        case "2":
            nova_leitura(bueiros, leituras, notifs)
        case "3":
            consulta(bueiros, leituras, notifs)
        case "4":
            lista(bueiros, leituras)
        case "5":
            ver_notif(notifs, bueiros)
        case "6":
            atualiza(notifs, bueiros)
        case "7":
            mostra_relatorio(bueiros, leituras, notifs)
        case "8":
            remove(bueiros, leituras, notifs)
        case "9":
            sobre()
        case _:
            print("Opção inválida. Escolhe um número do menu.")
    return True


def roda():
    bueiros, leituras, notifs = armazenamento.abre()
    segue = True
    while segue:
        menu()
        escolha = le("Opção: ")
        if escolha is None:
            segue = False
        else:
            segue = faz(escolha, bueiros, leituras, notifs)
    print()
    print("Até logo.")


if __name__ == "__main__":
    try:
        roda()
    except KeyboardInterrupt:
        print()
        print("Fechou.")
