from pydantic import BaseModel, field_validator
from typing import Optional
import re

class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    peso: float
    altura: float
    nivel_atividade: str

    @field_validator('id')
    def validar_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError('O id do usuário não pode ser negativo ou zero.')
        return v

    @field_validator('nome')
    def validar_nome(cls, v):
        nome_limpo = v.strip()
        if not nome_limpo:
            raise ValueError('O nome do usuário não pode ser vazio.')
        if len(nome_limpo) > 100:
            raise ValueError('O nome do usuário não pode exceder 100 caracteres.')
        return nome_limpo

    @field_validator('email')
    def validar_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Email inválido.')
        return v

    @field_validator('peso')
    def validar_peso(cls, v):
        if v <= 0 or v > 300:
            raise ValueError('O peso deve ser maior que zero e menor que 300 kg.')
        return v

    @field_validator('altura')
    def validar_altura(cls, v):
        if v <= 0 or v > 2.5:
            raise ValueError('A altura deve ser maior que zero e menor que 2.5 metros.')
        return v

    @field_validator('nivel_atividade')
    def validar_nivel_atividade(cls, v):
        niveis_validos = ['sedentário', 'leve', 'moderado', 'ativo', 'muito ativo']
        if v.lower() not in niveis_validos:
            raise ValueError(f'Nível de atividade deve ser um dos seguintes: {", ".join(niveis_validos)}.')
        return v.lower()