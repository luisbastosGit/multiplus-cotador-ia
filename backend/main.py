import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 20:37
from inteligencia.extrator_ia import processar_pdf_gemini
from drivers_seguradoras import porto_seguro

# Inicialização da API
app = FastAPI(title="Motor Multiplus - Multicálculo API")

# Liberação do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de Dados Padronizado
class DadosCotacao(BaseModel):
    origem: str
    nome: str
    cpf: str
    placa: str
    email: str
    pacote: str

@app.get("/")
def health_check():
    return {"status": "Motor Multiplus Online e Operante"}

@app.post("/extrair-apolice")
async def extrair_apolice(arquivo_pdf: UploadFile = File(...)):
    """
    Rota que recebe o PDF do Wix e repassa para o módulo Gemini.
    """
    try:
        conteudo = await arquivo_pdf.read()
        
        dados_extraidos = processar_pdf_gemini(conteudo)
        
        return {
            "status": "sucesso",
            "mensagem": f"Arquivo {arquivo_pdf.filename} processado pela IA.",
            "dados": dados_extraidos
        }
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/iniciar-cotacao")
async def iniciar_cotacao(dados: DadosCotacao):
    """
    Rota que recebe os dados limpos e aciona os robôs (Playwright).
    """
    try:
        print(f"Iniciando cotação recebida da origem: {dados.origem}")
        
        # NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 20:37
        # Aciona o robô da Porto Seguro passando o objeto de dados padronizado
        resultado_porto = porto_seguro.cotar(dados)
        
        return {
            "status": "sucesso",
            "mensagem": "Automação finalizada nas seguradoras.",
            "detalhes": [resultado_porto]
        }
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=porta)
