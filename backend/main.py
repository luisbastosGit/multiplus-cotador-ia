import os
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Inicialização da API
app = FastAPI(title="Motor Multiplus - Multicálculo API")

# Liberação do CORS (Isso impede que o navegador bloqueie a comunicação com o Wix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, colocaremos o domínio do seu frontend aqui
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de Dados Padronizado (Injeção de Dependência)
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
    Rota que receberá o PDF do Wix.
    Aqui integraremos o Gemini futuramente para extrair os dados.
    """
    try:
        conteudo = await arquivo_pdf.read()
        tamanho_mb = len(conteudo) / (1024 * 1024)
        
        # Simulação de resposta de sucesso para o Frontend
        return {
            "status": "sucesso",
            "mensagem": f"Arquivo {arquivo_pdf.filename} recebido ({tamanho_mb:.2f} MB). Fila de IA iniciada."
        }
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/iniciar-cotacao")
async def iniciar_cotacao(dados: DadosCotacao):
    """
    Rota que recebe os dados limpos (do form manual ou da IA)
    e aciona os robôs (Playwright) das seguradoras.
    """
    try:
        # Aqui chamaremos o driver da Porto Seguro, ex: 
        # resultado = porto_seguro.executar_cotacao(dados)
        
        print(f"Iniciando cotação para: {dados.nome} | Placa: {dados.placa}")
        
        return {
            "status": "sucesso",
            "mensagem": "Dados injetados na fila de processamento da seguradora."
        }
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

if __name__ == "__main__":
    # O Render exige que a porta seja definida por variável de ambiente
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=porta)
