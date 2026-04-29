# NOVO CÓDIGO INSERIDO AQUI - 29/04/2026 19:06
import os
import time
from playwright.sync_api import sync_playwright

class RoboPortoSeguro:
    def __init__(self):
        self.url_base = "https://corretor.portoseguro.com.br/corretoronline/"
        self.url_cotacao = "https://wwws.portoseguro.com.br/porto.auto.cotacao/#/cotacao?idp=1&susep=5C266J"
        self.cpf_login = os.environ.get("PORTO_CPF")
        self.senha_login = os.environ.get("PORTO_SENHA")
        self.susep = "5C266J"

    def executar_cotacao(self, dados):
        print(f"[Porto Seguro] Iniciando robô para: {dados.nome}")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = context.new_page()
                
                print("[Porto Seguro] Acessando portal...")
                page.goto(self.url_base, wait_until="domcontentloaded", timeout=60000)
                time.sleep(5)
                
                print("[Porto Seguro] Tentando clicar no botão de acesso...")
                botoes_acesso = page.locator("text=ACESSAR O CORRETOR ONLINE")
                if botoes_acesso.count() > 0:
                    botoes_acesso.first.click(force=True)
                else:
                    raise Exception("Botão de acesso não encontrado na página.")
                
                print("[Porto Seguro] Preenchendo credenciais...")
                # CORREÇÃO: Filtramos para pegar APENAS os campos visíveis, ignorando o "Recuperar Senha" oculto
                cpf_input = page.locator("input[name='logon'], input[placeholder*='CPF']").locator("visible=true").first
                cpf_input.wait_for(timeout=30000)
                cpf_input.fill(self.cpf_login or "")
                
                senha_input = page.locator("input[type='password']").locator("visible=true").first
                senha_input.fill(self.senha_login or "")
                
                btn_entrar = page.locator("button:has-text('ENTRAR')").locator("visible=true").first
                btn_entrar.click()
                
                # SUSEP
                print("[Porto Seguro] Inserindo SUSEP...")
                susep_input = page.locator("input[placeholder*='SUSEP']").locator("visible=true").first
                susep_input.wait_for(timeout=30000)
                susep_input.fill(self.susep)
                
                btn_susep = page.locator("button:has-text('ENTRAR')").locator("visible=true").first
                btn_susep.click()
                
                # NAVEGAÇÃO E INJEÇÃO
                print("[Porto Seguro] Redirecionando para Cotação Auto...")
                page.goto(self.url_cotacao, wait_until="domcontentloaded", timeout=60000)
                
                print("[Porto Seguro] Injetando CPF e Placa...")
                cpf_segurado = page.locator("input#cpf_segurado").locator("visible=true").first
                cpf_segurado.wait_for(timeout=30000)
                cpf_segurado.fill(dados.cpf)
                cpf_segurado.press("Tab")
                time.sleep(4)
                
                placa_veiculo = page.locator("input#placa_veiculo").locator("visible=true").first
                placa_veiculo.fill(dados.placa)
                placa_veiculo.press("Tab")
                
                try:
                    page.screenshot(path="evidencia_porto.png")
                except:
                    pass
                    
                browser.close()
                return {"status": "Injeção Concluída no Portal."}
                
        except Exception as e:
            msg_erro = str(e)
            print(f"[Porto Seguro] Erro capturado no fluxo: {msg_erro}")
            
            if "Executable doesn't exist" in msg_erro:
                return {"status": "Erro: Navegador Ausente."}
            elif "Timeout" in msg_erro:
                return {"status": "Aviso: O site da Porto Seguro demorou muito e o robô foi abortado."}
                
            return {"status": f"Falha de Automação: {msg_erro[:40]}"}

def cotar(dados):
    return RoboPortoSeguro().executar_cotacao(dados)
