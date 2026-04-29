# NOVO CÓDIGO INSERIDO AQUI - 29/04/2026
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
                
                # Pausa estratégica baseada no tempo real de carregamento do site
                time.sleep(5)
                
                print("[Porto Seguro] Tentando clicar no botão de acesso...")
                # Localiza os botões e força o clique no primeiro elemento disponível
                botoes_acesso = page.locator("text=ACESSAR O CORRETOR ONLINE")
                if botoes_acesso.count() > 0:
                    botoes_acesso.first.click(force=True)
                else:
                    raise Exception("Botão de acesso não encontrado na página.")
                
                print("[Porto Seguro] Preenchendo credenciais...")
                page.wait_for_selector("input[type='text']", timeout=30000)
                page.fill("input[placeholder*='CPF']", self.cpf_login or "")
                page.fill("input[type='password']", self.senha_login or "")
                page.click("button:has-text('ENTRAR')")
                
                # SUSEP
                print("[Porto Seguro] Inserindo SUSEP...")
                page.wait_for_selector("input[placeholder*='SUSEP']", timeout=30000)
                page.fill("input[placeholder*='SUSEP']", self.susep)
                page.click("button:has-text('ENTRAR')")
                
                # NAVEGAÇÃO E INJEÇÃO
                print("[Porto Seguro] Redirecionando para Cotação Auto...")
                page.goto(self.url_cotacao, wait_until="domcontentloaded", timeout=60000)
                
                print("[Porto Seguro] Injetando CPF e Placa...")
                page.wait_for_selector("input#cpf_segurado", timeout=30000)
                page.fill("input#cpf_segurado", dados.cpf)
                page.press("input#cpf_segurado", "Tab")
                time.sleep(4)
                
                page.fill("input#placa_veiculo", dados.placa)
                page.press("input#placa_veiculo", "Tab")
                
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
                return {"status": "Erro: Tempo limite excedido no portal da seguradora."}
                
            return {"status": f"Falha de Automação: {msg_erro[:40]}"}

def cotar(dados):
    return RoboPortoSeguro().executar_cotacao(dados)
