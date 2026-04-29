# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 22:45
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from inteligencia.extrator_ia import processar_pdf_gemini
from drivers_seguradoras import porto_seguro

app = FastAPI(title="Motor Multiplus - Multicálculo API")

# Configuração de CORS - Mantendo acessibilidade total para o seu frontend
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
    """Rota de verificação de integridade do servidor"""
    return {"status": "Motor Multiplus Online", "ambiente": "Render"}

@app.post("/extrair-apolice")
async def extrair_apolice(arquivo_pdf: UploadFile = File(...)):
    """
    Recebe o PDF, extrai via IA e aguarda a execução do robô da Porto Seguro.
    """
    try:
        conteudo = await arquivo_pdf.read()
        
        # 1. Extração pela IA (Gemini Dinâmico)
        dados_extraidos = processar_pdf_gemini(conteudo)
        
        # Inicializa o status da automação
        resultado_robo = {"status": "Não iniciado", "detalhes": "Dados insuficientes da IA"}
        
        # 2. Execução Síncrona do Robô
        # A conexão HTTP ficará aberta até o robô terminar ou dar timeout
        if dados_extraidos.get("origem") == "ia":
            objeto_dados = DadosCotacao(**dados_extraidos)
            resultado_robo = porto_seguro.cotar(objeto_dados)
        
        return {
            "status": "sucesso",
            "dados": dados_extraidos,
            "automacao": resultado_robo
        }
    except Exception as e:
        print(f"Erro na rota extrair-apolice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/iniciar-cotacao")
async def iniciar_cotacao(dados: DadosCotacao):
    """Rota para disparar o robô a partir de dados digitados manualmente"""
    try:
        resultado = porto_seguro.cotar(dados)
        return {"status": "sucesso", "detalhes": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=porta)
