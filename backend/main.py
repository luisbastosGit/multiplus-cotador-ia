# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 22:42
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
    Recebe o PDF, extrai via IA e executa o robô de forma síncrona.
    """
    try:
        # Leitura do conteúdo do arquivo de forma síncrona
        conteudo = arquivo_pdf.file.read()
        
        # 1. Extração pela IA
        dados_extraidos = processar_pdf_gemini(conteudo)
        
        resultado_robo = {"status": "Não iniciado"}
        
        # 2. Execução do Robô
        if dados_extraidos.get("origem") == "ia":
            objeto_dados = DadosCotacao(**dados_extraidos)
            resultado_robo = porto_seguro.cotar(objeto_dados)
        
        return {
            "status": "sucesso",
            "dados": dados_extraidos,
            "automacao": resultado_robo
        }
    except Exception as e:
        print(f"Erro na rota: {str(e)}")
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
