# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 22:42
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
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            try:
                # 1. LOGIN
                print("[Porto Seguro] Acessando portal...")
                page.goto(self.url_base, wait_until="networkidle")
                page.click("text=ACESSAR O CORRETOR ONLINE")
                
                page.wait_for_selector("input[type='text']", timeout=15000)
                page.fill("input[placeholder*='CPF']", self.cpf_login)
                page.fill("input[type='password']", self.senha_login)
                page.click("button:has-text('ENTRAR')")
                
                # 2. SUSEP
                print("[Porto Seguro] Validando SUSEP...")
                page.wait_for_selector("input[placeholder*='SUSEP']", timeout=15000)
                page.fill("input[placeholder*='SUSEP']", self.susep)
                page.click("button:has-text('ENTRAR')")
                
                # 3. NAVEGAÇÃO E INJEÇÃO
                print("[Porto Seguro] Preenchendo dados de cálculo...")
                page.goto(self.url_cotacao, wait_until="networkidle")
                
                page.wait_for_selector("input#cpf_segurado", timeout=20000)
                page.fill("input#cpf_segurado", dados.cpf)
                page.press("input#cpf_segurado", "Tab")
                time.sleep(4) 
                
                page.fill("input#placa_veiculo", dados.placa)
                page.press("input#placa_veiculo", "Tab")
                time.sleep(4)
                
                page.screenshot(path="evidencia_porto.png")
                return {"status": "Sucesso", "detalhes": "Dados injetados"}

            except Exception as e:
                print(f"[Porto Seguro] Erro: {str(e)}")
                return {"status": "Erro", "detalhes": str(e)[:50]}
            finally:
                browser.close()

def cotar(dados):
    return RoboPortoSeguro().executar_cotacao(dados)
