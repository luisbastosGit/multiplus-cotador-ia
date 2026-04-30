# NOVO CÓDIGO INSERIDO AQUI - 30/04/2026 14:30
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from inteligencia.extrator_ia import processar_pdf_gemini

app = FastAPI(title="Motor Multiplus IA Híbrido")

# CORS ATUALIZADO E TOTALMENTE LIBERADO PARA TESTE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que qualquer frontend (onrender.com, localhost) fale com este backend
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
    return {"status": "Motor Multiplus IA Híbrido Online"}

# ROTA ATUALIZADA PARA COINCIDIR COM O FRONTEND (/cotar-ia)
@app.post("/cotar-ia")
def cotar_ia(arquivo_pdf: UploadFile = File(...)):
    try:
        conteudo = arquivo_pdf.file.read()
        
        # O backend apenas extrai os dados via IA e devolve.
        dados_extraidos = processar_pdf_gemini(conteudo)
        
        return {
            "status": "sucesso",
            "dados": dados_extraidos,
            "automacao": {"status": "Sinal delegado à Extensão Local"}
        }
        
    except Exception as e:
        print(f"Erro Crítico Backend: {str(e)}")
        raise HTTPException(status_code=500, detail="Falha severa na leitura do documento.")

# ROTA ATUALIZADA PARA COINCIDIR COM O FRONTEND (/enviar-cotacao)
@app.post("/enviar-cotacao")
def enviar_cotacao(dados: DadosCotacao):
    # No modelo híbrido, essa rota manual também delega para a extensão.
    return {"status": "sucesso", "detalhes": {"status": "Sinal manual delegado à Extensão Local"}}

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=porta)
