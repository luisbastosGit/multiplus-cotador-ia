# NOVO CÓDIGO INSERIDO AQUI - 30/04/2026
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from inteligencia.extrator_ia import processar_pdf_gemini

app = FastAPI(title="Motor Multiplus - API de IA")

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
    return {"status": "Motor Multiplus IA Online"}

@app.post("/extrair-apolice")
def extrair_apolice(arquivo_pdf: UploadFile = File(...)):
    try:
        conteudo = arquivo_pdf.file.read()
        
        # O backend agora é ultra-rápido: apenas extrai os dados via IA e devolve.
        dados_extraidos = processar_pdf_gemini(conteudo)
        
        return {
            "status": "sucesso",
            "dados": dados_extraidos,
            "automacao": {"status": "Sinal enviado para a Extensão Local"}
        }
        
    except Exception as e:
        print(f"Erro Crítico Backend: {str(e)}")
        raise HTTPException(status_code=500, detail="Falha severa na leitura do documento.")

@app.post("/iniciar-cotacao")
def iniciar_cotacao(dados: DadosCotacao):
    return {"status": "sucesso", "detalhes": {"status": "Sinal manual enviado para a Extensão Local"}}

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=porta)
