# NOVO CÓDIGO INSERIDO AQUI - 29/04/2026 11:26
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
    try:
        conteudo = arquivo_pdf.file.read()
        
        # 1. A Extração pela IA sempre ocorre primeiro
        dados_extraidos = processar_pdf_gemini(conteudo)
        
        resultado_automacao = {"status": "Aguardando Inicialização do Robô"}
        
        # 2. Proteção Absoluta: Tenta rodar o robô. Se falhar, não derruba a IA.
        if dados_extraidos.get("origem") == "ia":
            objeto_dados = DadosCotacao(**dados_extraidos)
            try:
                resultado_automacao = porto_seguro.cotar(objeto_dados)
            except Exception as erro_robo:
                print(f"Falha isolada no robô: {str(erro_robo)}")
                resultado_automacao = {"status": "Erro no servidor do robô, mas IA concluída."}
        
        # 3. Retorna os dados da IA com segurança para o Frontend
        return {
            "status": "sucesso",
            "dados": dados_extraidos,
            "automacao": resultado_automacao
        }
        
    except Exception as e:
        print(f"Erro Crítico Backend: {str(e)}")
        raise HTTPException(status_code=500, detail="Falha severa na leitura do documento.")

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
