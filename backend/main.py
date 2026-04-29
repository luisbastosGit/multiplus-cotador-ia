# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 22:23
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from inteligencia.extrator_ia import processar_pdf_gemini
from drivers_seguradoras import porto_seguro

app = FastAPI(title="Motor Multiplus - Multicálculo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DadosCotacao(BaseModel):
    origem: str
    nome: str
    cpf: str
    placa: str
    email: str
    pacote: str

@app.get("/")
def health_check():
    return {"status": "Motor Multiplus Online"}

@app.post("/extrair-apolice")
async def extrair_apolice(arquivo_pdf: UploadFile = File(...)):
    """
    Recebe o PDF, extrai via IA e aciona IMEDIATAMENTE o robô da Porto.
    """
    try:
        conteudo = await arquivo_pdf.read()
        
        # 1. Extração pela IA
        dados_extraidos = processar_pdf_gemini(conteudo)
        
        # 2. Se a extração funcionou, dispara o robô da Porto Seguro
        resultado_robo = {"status": "IA falhou, robô não acionado."}
        
        if dados_extraidos.get("origem") == "ia":
            # Converte dicionário para o objeto esperado pelo robô
            objeto_dados = DadosCotacao(**dados_extraidos)
            resultado_robo = porto_seguro.cotar(objeto_dados)
        
        return {
            "status": "sucesso",
            "dados": dados_extraidos,
            "automacao": resultado_robo
        }
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/iniciar-cotacao")
async def iniciar_cotacao(dados: DadosCotacao):
    """Rota para o formulário manual"""
    try:
        resultado = porto_seguro.cotar(dados)
        return {"status": "sucesso", "detalhes": resultado}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=porta)
