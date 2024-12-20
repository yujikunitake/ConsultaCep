from pydantic import BaseModel
from typing import Optional


class CEP(BaseModel):
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    complemento: Optional[str] = None  # Notei que há CEPs sem complemento
    unidade: Optional[str] = None  # Notei que há CEPs sem complemento
    bairro: Optional[str] = None
    localidade: Optional[str] = None
    uf: Optional[str] = None
    estado: Optional[str] = None
    regiao: Optional[str] = None
    ibge: Optional[int] = None  # Notei que não existe cod IBGE iniciado com 0
    gia: Optional[str] = None  # Notei que há CEPs sem GIA
    ddd: Optional[int] = None  # Todos DDDs são números naturais
    siafi: Optional[str] = None  # Segundo a planilha obtida em https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/informacoes-uteis/Codigomunicipiossiafi.xlsx há siafi que começam com 0
