# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 21:58
import os
import json
import tempfile
import time
import google.generativeai as genai

def buscar_melhor_modelo_disponivel():
    """
    Consulta a API do Google para encontrar o melhor modelo disponível
    que suporte a geração de conteúdo.
    """
    try:
        modelos_disponiveis = genai.list_models()
        modelos_suportados = [
            m.name for m in modelos_disponiveis 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # Prioridade 1: Qualquer variação do Gemini 1.5 Pro
        for m in modelos_suportados:
            if 'gemini-1.5-pro' in m:
                return m
        
        # Prioridade 2: Qualquer variação do Gemini 1.5 Flash
        for m in modelos_suportados:
            if 'gemini-1.5-flash' in m:
                return m
                
        # Fallback: O primeiro modelo que suportar a função
        return modelos_suportados[0] if modelos_suportados else "gemini-1.5-flash"
    except Exception as e:
        print(f"Erro ao listar modelos: {e}")
        return "gemini-1.5-flash"

def processar_pdf_gemini(conteudo_pdf: bytes) -> dict:
    """
    Módulo dinâmico que detecta o modelo disponível e extrai dados do PDF.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return {
            "origem": "erro_ia",
            "nome": "Erro: Variável GEMINI_API_KEY ausente",
            "cpf": "00000000000",
            "placa": "ERRO000",
            "email": "",
            "pacote": "intermediario"
        }

    genai.configure(api_key=api_key)
    caminho_tmp = None
    arquivo_gemini = None

    try:
        # 1. Descoberta dinâmica do modelo
        modelo_escolhido = buscar_melhor_modelo_disponivel()
        print(f"Modelo detectado e selecionado: {modelo_escolhido}")

        # 2. Criação do arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(conteudo_pdf)
            caminho_tmp = tmp.name

        # 3. Upload para o Google
        arquivo_gemini = genai.upload_file(path=caminho_tmp, mime_type="application/pdf")

        # 4. Aguarda processamento (Polling)
        while arquivo_gemini.state.name == "PROCESSING":
            time.sleep(2)
            arquivo_gemini = genai.get_file(arquivo_gemini.name)
            
        if arquivo_gemini.state.name == "FAILED":
            raise Exception("Falha no processamento do arquivo pelo Google.")

        # 5. Configuração do modelo detectado
        model = genai.GenerativeModel(
            model_name=modelo_escolhido,
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

        # 6. Geração do conteúdo
        resposta = model.generate_content([prompt, arquivo_gemini])
        
        # 7. Limpeza e parsing do JSON
        texto_limpo = resposta.text.strip()
        if texto_limpo.startswith("```"):
            import re
            texto_limpo = re.sub(r'^```[a-zA-Z]*\n|```$', '', texto_limpo, flags=re.MULTILINE).strip()

        return json.loads(texto_limpo)

    except Exception as e:
        print(f"Erro crítico no Extrator IA: {str(e)}")
        return {
            "origem": "erro_ia",
            "nome": f"Erro Técnico: {str(e)[:150]}",
            "cpf": "00000000000",
            "placa": "ERRO000",
            "email": "",
            "pacote": "intermediario"
        }
    
    finally:
        if caminho_tmp and os.path.exists(caminho_tmp):
            os.remove(caminho_tmp)
        if arquivo_gemini:
            try:
                genai.delete_file(arquivo_gemini.name)
            except:
                pass
