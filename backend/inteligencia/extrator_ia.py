# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 21:34
import os
import json
import tempfile
import time
import google.generativeai as genai

def processar_pdf_gemini(conteudo_pdf: bytes) -> dict:
    """
    Módulo que utiliza o Gemini 1.5 Pro para ler apólices em PDF
    e devolver os dados estruturados para o robô da Porto Seguro.
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
        # 1. Cria um arquivo temporário no servidor para o Gemini poder ler
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(conteudo_pdf)
            caminho_tmp = tmp.name

        # 2. Faz o upload do documento para a infraestrutura do Google
        arquivo_gemini = genai.upload_file(path=caminho_tmp, mime_type="application/pdf")

        # 3. Espera Inteligente (Polling): Aguarda o Google processar o PDF antes de ler
        while arquivo_gemini.state.name == "PROCESSING":
            print("Aguardando processamento do PDF pelo Google...")
            time.sleep(2)
            arquivo_gemini = genai.get_file(arquivo_gemini.name)
            
        if arquivo_gemini.state.name == "FAILED":
            raise Exception("Os servidores do Google falharam ao processar este PDF.")

        # 4. Configura o modelo para extração estrita de JSON
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={"response_mime_type": "application/json"}
        )

        prompt = """
        Analise esta apólice ou proposta de seguro automóvel e extraia os dados abaixo.
        Retorne estritamente um JSON com esta estrutura, sem formatação markdown:
        {
            "origem": "ia",
            "nome": "NOME COMPLETO DO SEGURADO",
            "cpf": "APENAS NUMEROS DO CPF",
            "placa": "PLACA DO VEICULO",
            "email": "EMAIL DO SEGURADO SE DISPONIVEL",
            "pacote": "Deduza: 'basico' (guincho até 200km), 'intermediario' (guincho 500km), 'completo' (ilimitado) ou 'apenas_veiculo' (sem guincho)."
        }
        """

        # 5. Gera a extração
        resposta = model.generate_content([prompt, arquivo_gemini])
        
        # 6. Limpeza brutal de qualquer formatação Markdown invisível
        texto_limpo = resposta.text.strip()
        if texto_limpo.startswith("```json"):
            texto_limpo = texto_limpo[7:]
        if texto_limpo.startswith("```"):
            texto_limpo = texto_limpo[3:]
        if texto_limpo.endswith("```"):
            texto_limpo = texto_limpo[:-3]
        texto_limpo = texto_limpo.strip()

        # Converte a string de texto da IA para um dicionário Python
        dados_finais = json.loads(texto_limpo)
        return dados_finais

    except Exception as e:
        print(f"Erro crítico no Extrator IA: {str(e)}")
        # Injeta o erro real da Google no campo 'nome' para debug visual
        return {
            "origem": "erro_ia",
            "nome": f"Erro Técnico: {str(e)[:150]}",
            "cpf": "00000000000",
            "placa": "ERRO000",
            "email": "",
            "pacote": "intermediario"
        }
    
    finally:
        # Limpeza obrigatória do arquivo temporário no disco do Render
        if caminho_tmp and os.path.exists(caminho_tmp):
            os.remove(caminho_tmp)
        # Limpeza do arquivo na nuvem da Google por segurança de dados
        if arquivo_gemini:
            try:
                genai.delete_file(arquivo_gemini.name)
            except:
                pass
