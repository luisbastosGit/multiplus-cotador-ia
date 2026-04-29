# NOVO CÓDIGO INSERIDO AQUI - 29/04/2026 19:20
import os
import time
from playwright.sync_api import sync_playwright

class RoboPortoSeguro:
    def __init__(self):
        self.url_base = "https://corretor.portoseguro.com.br/corretoronline/"
        self.url_cotacao = "https://wwws.portoseguro.com.br/porto.auto.cotacao/#/cotacao?idp=1&susep=5C266J"
        self.cpf_login = os.environ.get("PORTO_CPF")
        self.senha_login = os.environ.get("PORTO_SENHA")
        self.susep_padrao = "5C266J"

    def executar_cotacao(self, dados):
        print(f"[Porto Seguro] Iniciando robô para: {dados.nome}")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = context.new_page()
                
                # 1. ACESSO INICIAL
                print("[Porto Seguro] Acessando portal...")
                page.goto(self.url_base, wait_until="domcontentloaded", timeout=60000)
                time.sleep(5)
                
                # 2. CLIQUE NO ACESSO
                botoes_acesso = page.locator("text=ACESSAR O CORRETOR ONLINE")
                if botoes_acesso.count() > 0:
                    botoes_acesso.first.click(force=True)
                else:
                    raise Exception("Botão de acesso inicial não encontrado.")
                
                # 3. LOGIN E SENHA
                print("[Porto Seguro] Preenchendo login e senha...")
                cpf_input = page.locator("input[name='logon'], input[placeholder*='CPF']").locator("visible=true").first
                cpf_input.wait_for(timeout=30000)
                cpf_input.fill(self.cpf_login or "")
                
                senha_input = page.locator("input[type='password']").locator("visible=true").first
                senha_input.fill(self.senha_login or "")
                senha_input.press("Enter")
                
                # Clique de segurança caso o Enter não dispare
                time.sleep(2)
                btn_entrar = page.locator("text='ENTRAR'").locator("visible=true")
                if btn_entrar.count() > 0:
                    btn_entrar.first.click(force=True)
                
                # 4. TELA DA SUSEP (Conforme evidência visual)
                print(f"[Porto Seguro] Identificando tela SUSEP para inserir {self.susep_padrao}...")
                susep_input = page.locator("input[placeholder*='SUSEP'], input[name*='susep']").locator("visible=true").first
                susep_input.wait_for(timeout=30000)
                susep_input.fill(self.susep_padrao)
                susep_input.press("Enter")
                
                time.sleep(2)
                btn_confirmar_susep = page.locator("text='ENTRAR'").locator("visible=true")
                if btn_confirmar_susep.count() > 0:
                    btn_confirmar_susep.first.click(force=True)
                
                # 5. TRANSIÇÃO PARA O SISTEMA DE COTAÇÃO
                print("[Porto Seguro] Navegando para a área de cálculo...")
                page.goto(self.url_cotacao, wait_until="domcontentloaded", timeout=60000)
                
                # 6. INJEÇÃO DOS DADOS EXTRAÍDOS
                print(f"[Porto Seguro] Injetando CPF: {dados.cpf} e Placa: {dados.placa}")
                cpf_segurado = page.locator("input#cpf_segurado").locator("visible=true").first
                cpf_segurado.wait_for(timeout=30000)
                cpf_segurado.fill(dados.cpf)
                cpf_segurado.press("Tab")
                
                time.sleep(4) # Aguarda retorno do webservice da Porto
                
                placa_veiculo = page.locator("input#placa_veiculo").locator("visible=true").first
                placa_veiculo.fill(dados.placa)
                placa_veiculo.press("Tab")
                
                # Sucesso
                try:
                    page.screenshot(path="evidencia_final_porto.png")
                except:
                    pass
                    
                browser.close()
                return {"status": "Injeção finalizada com sucesso."}
                
        except Exception as e:
            msg_erro = str(e)
            print(f"[Porto Seguro] Falha no fluxo: {msg_erro}")
            return {"status": f"Erro na automação: {msg_erro[:50]}"}

def cotar(dados):
    return RoboPortoSeguro().executar_cotacao(dados)
