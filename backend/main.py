# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 23:00
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
def extrair_apolice(arquivo_pdf: UploadFile = File(...)):
    """
    Lê o PDF, extrai via IA e aciona o robô.
    Usamos 'def' puro para evitar conflitos de loop com o Playwright Sync.
    """
    try:
        # Leitura síncrona para evitar problemas de concorrência
        conteudo = arquivo_pdf.file.read()
        
        # 1. Extração pela IA (Gemini)
        dados_extraidos = processar_pdf_gemini(conteudo)
        
        # 2. Inicialização do status do robô
        resultado_automacao = {"status": "IA falhou ou dados insuficientes"}
        
        # 3. Disparo do Robô se a IA teve sucesso
        if dados_extraidos.get("origem") == "ia":
            objeto_dados = DadosCotacao(**dados_extraidos)
            resultado_automacao = porto_seguro.cotar(objeto_dados)
        
        return {
            "status": "sucesso",
            "dados": dados_extraidos,
            "automacao": resultado_automacao
        }
    except Exception as e:
        print(f"Erro Crítico: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/iniciar-cotacao")
def iniciar_cotacao(dados: DadosCotacao):
    try:
        resultado = porto_seguro.cotar(dados)
        return {"status": "sucesso", "detalhes": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=porta)
