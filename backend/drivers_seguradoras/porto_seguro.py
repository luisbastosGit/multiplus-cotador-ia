# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 22:15
from playwright.sync_api import sync_playwright
import time
import os

class RoboPortoSeguro:
    def __init__(self):
        self.url_base = "https://corretor.portoseguro.com.br/corretoronline/"
        self.url_cotacao = "https://wwws.portoseguro.com.br/porto.auto.cotacao/#/cotacao?idp=1&susep=5C266J"
        # Dados sensíveis devem vir do ambiente (Render)
        self.cpf_login = os.environ.get("PORTO_CPF")
        self.senha_login = os.environ.get("PORTO_SENHA")
        self.susep = "5C266J"

    def executar_cotacao(self, dados):
        print(f"[Porto Seguro] Iniciando automação para {dados.nome}")
        
        with sync_playwright() as p:
            # Lançamento com User-Agent para evitar bloqueio por bot
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            try:
                # 1. ACESSO INICIAL
                page.goto(self.url_base, wait_until="networkidle")
                
                # 2. CLIQUE NO ACESSAR (Figura 1)
                page.click("text=ACESSAR O CORRETOR ONLINE")
                
                # 3. LOGIN (Figura 2)
                # Seletores baseados na estrutura comum de modais da Porto
                page.wait_for_selector("input[type='text']") # Espera o campo CPF
                page.fill("input[placeholder*='CPF']", self.cpf_login or "67144845004")
                page.fill("input[type='password']", self.senha_login or "PFloripa@26")
                page.click("button:has-text('ENTRAR')")
                
                # 4. CONFIRMAÇÃO SUSEP (Figura 3)
                page.wait_for_selector("input[placeholder*='SUSEP']", timeout=15000)
                page.fill("input[placeholder*='SUSEP']", self.susep)
                page.click("button:has-text('ENTRAR')")
                
                # 5. NAVEGAÇÃO DIRETA PARA COTAÇÃO
                print("[Porto Seguro] Indo para URL de cotação final...")
                page.goto(self.url_cotacao, wait_until="networkidle")
                
                # 6. INJEÇÃO DOS DADOS (Onde a mágica acontece)
                # Inserir CPF
                page.wait_for_selector("input#cpf_segurado") # Exemplo de ID
                page.fill("input#cpf_segurado", dados.cpf)
                page.press("input#cpf_segurado", "Tab")
                
                # Pequena espera para o site buscar na Receita Federal (como você notou)
                time.sleep(3) 
                
                # Inserir Placa
                page.fill("input#placa_veiculo", dados.placa)
                page.press("input#placa_veiculo", "Tab")
                
                # Espera o auto-preenchimento do veículo
                time.sleep(3)

                return {
                    "seguradora": "Porto Seguro",
                    "status": "Dados injetados com sucesso. Aguardando cálculo.",
                    "veiculo_detectado": True
                }

            except Exception as e:
                print(f"[Porto Seguro] Erro no fluxo: {str(e)}")
                return {"seguradora": "Porto Seguro", "status": f"Erro: {str(e)[:100]}"}
            finally:
                browser.close()

def cotar(dados):
    robo = RoboPortoSeguro()
    return robo.executar_cotacao(dados)
