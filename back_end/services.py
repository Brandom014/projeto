import requests
from database import SUPABASE_URL, SUPABASE_KEY, HEADERS


# LOGIN (CORRIGIDO)
def fazer_login(email, senha):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"

    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(url, json={
        "email": email,
        "password": senha
    }, headers=headers)

    data = res.json()

    return data


# CADASTRO (CORRIGIDO)
def criar_usuario(nome, email, senha):
    url = f"{SUPABASE_URL}/auth/v1/signup"

    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(url, json={
        "email": email,
        "password": senha,
        "data": {"nome": nome}
    }, headers=headers)

    return res.json()


# PRODUTOS (MANTIDO)
def listar_produtos():
    url_prod = f"{SUPABASE_URL}/rest/v1/produtos"
    url_var = f"{SUPABASE_URL}/rest/v1/variantes"

    produtos = requests.get(url_prod, headers=HEADERS).json()
    variantes = requests.get(url_var, headers=HEADERS).json()

    for p in produtos:
        p["variantes"] = [v for v in variantes if v["produto_id"] == p["id"]]
        p["tipo"] = "simples" if len(p["variantes"]) == 1 else "variavel"

    return produtos


# VENDAS
def listar_vendas():
    url = f"{SUPABASE_URL}/rest/v1/vendas"
    return requests.get(url, headers=HEADERS).json()


# ENTRADAS
def listar_entradas():
    url = f"{SUPABASE_URL}/rest/v1/entradas_estoque"
    return requests.get(url, headers=HEADERS).json()


# ESTOQUE SAÍDA
def atualizar_estoque_saida(variante_id, qtd):
    url = f"{SUPABASE_URL}/rest/v1/variantes?id=eq.{variante_id}"

    atual = requests.get(url, headers=HEADERS).json()[0]
    novo = atual["estoque"] - qtd

    requests.patch(url, json={"estoque": novo}, headers=HEADERS)


# ESTOQUE ENTRADA
def atualizar_estoque_entrada(variante_id, qtd):
    url = f"{SUPABASE_URL}/rest/v1/variantes?id=eq.{variante_id}"

    atual = requests.get(url, headers=HEADERS).json()[0]
    novo = atual["estoque"] + qtd

    requests.patch(url, json={"estoque": novo}, headers=HEADERS)


# VENDA (OK)
def criar_venda(dados):
    url_venda = f"{SUPABASE_URL}/rest/v1/vendas"

    res = requests.post(url_venda, json={
        "total": dados.total,
        "forma_pagamento": dados.pagamento
    }, headers=HEADERS)

    venda = res.json()[0]
    venda_id = venda["id"]

    url_itens = f"{SUPABASE_URL}/rest/v1/itens_venda"

    for item in dados.itens:
        requests.post(url_itens, json={
            "venda_id": venda_id,
            "variante_id": item.variante_id,
            "quantidade": item.qtd,
            "preco_unitario": item.preco
        }, headers=HEADERS)

        atualizar_estoque_saida(item.variante_id, item.qtd)

    return venda_id


# ENTRADA
def registrar_entrada(dados):
    url = f"{SUPABASE_URL}/rest/v1/entradas_estoque"

    requests.post(url, json={
        "variante_id": dados.variante_id,
        "quantidade": dados.quantidade,
        "tipo": dados.tipo
    }, headers=HEADERS)

    atualizar_estoque_entrada(dados.variante_id, dados.quantidade)


# DASHBOARD
def resumo_dashboard():
    vendas = listar_vendas()
    entradas = listar_entradas()

    faturamento = sum(v["total"] for v in vendas)
    total_vendas = len(vendas)
    total_entradas = sum(e["quantidade"] for e in entradas)

    return {
        "faturamento": faturamento,
        "total_vendas": total_vendas,
        "total_itens_entrada": total_entradas
    }