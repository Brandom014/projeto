from pydantic import BaseModel
from typing import List

class LoginSchema(BaseModel):
    email: str
    senha: str

class ItemVenda(BaseModel):
    variante_id: int
    qtd: int
    preco: float

class VendaSchema(BaseModel):
    total: float
    pagamento: str
    itens: List[ItemVenda]

class EntradaEstoque(BaseModel):
    variante_id: int
    quantidade: int
    tipo: str