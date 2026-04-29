# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 23:00
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
                
                # LOGIN
                page.goto(self.url_base, wait_until="networkidle")
                page.click("text=ACESSAR O CORRETOR ONLINE")
                
                page.wait_for_selector("input[type='text']", timeout=10000)
                page.fill("input[placeholder*='CPF']", self.cpf_login)
                page.fill("input[type='password']", self.senha_login)
                page.click("button:has-text('ENTRAR')")
                
                # SUSEP
                page.wait_for_selector("input[placeholder*='SUSEP']", timeout=10000)
                page.fill("input[placeholder*='SUSEP']", self.susep)
                page.click("button:has-text('ENTRAR')")
                
                # NAVEGAÇÃO E INJEÇÃO
                page.goto(self.url_cotacao, wait_until="networkidle")
                page.wait_for_selector("input#cpf_segurado", timeout=15000)
                page.fill("input#cpf_segurado", dados.cpf)
                page.press("input#cpf_segurado", "Tab")
                time.sleep(3)
                
                page.fill("input#placa_veiculo", dados.placa)
                page.press("input#placa_veiculo", "Tab")
                
                page.screenshot(path="evidencia_porto.png")
                browser.close()
                return {"status": "Injeção Concluída"}
                
        except Exception as e:
            msg_erro = str(e)
            if "Executable doesn't exist" in msg_erro:
                return {"status": "Erro: Navegador não instalado no Render. Verifique o Build Command."}
            return {"status": f"Erro no Robô: {msg_erro[:50]}"}

def cotar(dados):
    return RoboPortoSeguro().executar_cotacao(dados)
