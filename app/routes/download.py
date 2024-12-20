from bson import json_util
import csv
from fastapi.responses import JSONResponse, StreamingResponse
from io import StringIO
from fastapi import HTTPException, APIRouter
from app.database import db
from app.models import CEP

router = APIRouter()

def gerar_json(dados):
    try:
        return JSONResponse(
            content=json_util.dumps(dados),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=ceps.json"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar arquivo JSON: {str(e)}")

def gerar_csv(dados):
    try:
        fieldnames = list(CEP.model_fields.keys()) + ["_id"]

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for dado in dados:
            dado["_id"] = str(dado["_id"])
            writer.writerow(dado)

        output.seek(0)

        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=ceps.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar arquivo CSV: {str(e)}")

@router.get("/{formato}")
def download_dados(formato: str):
    try:
        dados = list(db.ceps.find())

        if not dados:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para exportação.")

        if formato == "json":
            return gerar_json(dados)

        elif formato == "csv":
            return gerar_csv(dados)

        else:
            raise HTTPException(status_code=400, detail="Formato inválido. Escolha 'json' ou 'csv'.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar arquivo: {str(e)}")
