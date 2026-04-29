# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 21:12
import os
import json
import tempfile
import google.generativeai as genai

def processar_pdf_gemini(conteudo_pdf: bytes) -> dict:
    """
    Módulo que utiliza o Gemini 1.5 Pro para ler apólices em PDF
    e devolver os dados estruturados para o robô da Porto Seguro.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("ERRO: Variável GEMINI_API_KEY não encontrada no Render.")

    genai.configure(api_key=api_key)

    # 1. Cria um arquivo temporário no servidor para o Gemini poder ler
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(conteudo_pdf)
        caminho_tmp = tmp.name

    try:
        # 2. Faz o upload do documento para a infraestrutura do Google
        arquivo_gemini = genai.upload_file(path=caminho_tmp, mime_type="application/pdf")

        # 3. Configura o modelo para extração estrita de JSON
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={"response_mime_type": "application/json"}
        )

        prompt = """
        Analise esta apólice ou proposta de seguro automóvel e extraia os dados abaixo.
        Retorne estritamente um JSON com esta estrutura:
        {
            "origem": "ia",
            "nome": "NOME COMPLETO DO SEGURADO",
            "cpf": "APENAS NUMEROS DO CPF",
            "placa": "PLACA DO VEICULO",
            "email": "EMAIL DO SEGURADO SE DISPONIVEL",
            "pacote": "Deduza: 'basico' (guincho até 200km), 'intermediario' (guincho 500km), 'completo' (ilimitado) ou 'apenas_veiculo' (sem guincho)."
        }
        """

        # 4. Gera a extração
        resposta = model.generate_content([prompt, arquivo_gemini])
        
        # Converte a string de texto da IA para um dicionário Python
        dados_finais = json.loads(resposta.text)
        return dados_finais

    except Exception as e:
        print(f"Erro crítico no Extrator IA: {str(e)}")
        return {
            "origem": "erro_ia",
            "nome": "Erro na leitura do PDF",
            "cpf": "00000000000",
            "placa": "ERRO000",
            "email": "",
            "pacote": "intermediario"
        }
    
    finally:
        # Limpeza obrigatória do arquivo temporário para não encher o disco do Render
        if os.path.exists(caminho_tmp):
            os.remove(caminho_tmp)
