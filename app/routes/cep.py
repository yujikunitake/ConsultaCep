from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import CEP
from app.util import viacep
from bson import ObjectId


router = APIRouter()

def salvar_consulta(cep: CEP):
    try:
        db.ceps.insert_one(cep.model_dump())

        return {"message": "Consulta salva com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {str(e)}")

@router.post("/{estado}/{cidade}/{logradouro}")
def consultar_cep(estado: str, cidade: str, logradouro: str):
    try:
        resultado = viacep.consultar_cep_por_estado_cidade_logradouro(estado, cidade, logradouro)

        for cep in resultado:
            salvar_consulta(cep)
        return {"message": "Consulta realizada e salva com sucesso!", "dados": resultado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/")
def listar_consultas():
    try:
        consultas = db.ceps.find()
        return [CEP(**consulta) for consulta in consultas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar consultas: {str(e)}")

@router.put("/{id}")
def atualizar_consulta(id: str, cep: CEP):
    try:
        result = db.ceps.update_one(
            {"_id": ObjectId(id)},
            {"$set": cep.model_dump()}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Consulta não encontrada para atualização")
        
        return {"message": "Consulta atualizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar consulta: {str(e)}")


@router.delete("/{id}")
def deletar_consulta(id: str):
    try:
        result = db.ceps.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Consulta não encontrada para deleção")
        
        return {"message": "Consulta deletada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar consulta: {str(e)}")

