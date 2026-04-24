from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import LoginSchema, VendaSchema, EntradaEstoque
from services import (
    fazer_login,
    listar_produtos,
    listar_vendas,
    criar_venda,
    registrar_entrada,
    resumo_dashboard,
    listar_entradas
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LOGIN
@app.post("/login")
def login(dados: LoginSchema):
    return fazer_login(dados.email, dados.senha)


# PRODUTOS
@app.get("/produtos")
def produtos():
    return listar_produtos()


# VENDA
@app.post("/venda")
def venda(dados: VendaSchema):
    venda_id = criar_venda(dados)
    return {"status": "ok", "venda_id": venda_id}


# ENTRADA
@app.post("/entrada")
def entrada(dados: EntradaEstoque):
    registrar_entrada(dados)
    return {"status": "estoque atualizado"}


# VENDAS
@app.get("/vendas")
def vendas():
    return listar_vendas()


# ENTRADAS
@app.get("/entradas")
def entradas():
    return listar_entradas()


# DASHBOARD
@app.get("/dashboard")
def dashboard():
    return resumo_dashboard()