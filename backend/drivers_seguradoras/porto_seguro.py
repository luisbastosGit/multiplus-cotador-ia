# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 22:45
import os
import time
from playwright.sync_api import sync_playwright

class RoboPortoSeguro:
    def __init__(self):
        self.url_base = "https://corretor.portoseguro.com.br/corretoronline/"
        self.url_cotacao = "https://wwws.portoseguro.com.br/porto.auto.cotacao/#/cotacao?idp=1&susep=5C266J"
        # Busca credenciais das variáveis de ambiente do Render
        self.cpf_login = os.environ.get("PORTO_CPF")
        self.senha_login = os.environ.get("PORTO_SENHA")
        self.susep = "5C266J"

    def executar_cotacao(self, dados):
        """
        Realiza o fluxo completo: Login -> SUSEP -> Navegação -> Preenchimento
        """
        print(f"[Porto Seguro] Iniciando robô para: {dados.nome}")
        
        with sync_playwright() as p:
            # Lançamento do navegador em modo headless no servidor
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            try:
                # 1. LOGIN
                print("[Porto Seguro] Acessando portal...")
                page.goto(self.url_base, wait_until="networkidle")
                
                # Clica no botão de acesso da página inicial
                page.click("text=ACESSAR O CORRETOR ONLINE")
                
                # Espera e preenche o formulário de login (Figura 2)
                page.wait_for_selector("input[type='text']", timeout=15000)
                page.fill("input[placeholder*='CPF']", self.cpf_login)
                page.fill("input[type='password']", self.senha_login)
                page.click("button:has-text('ENTRAR')")
                
                # 2. SELEÇÃO DE SUSEP (Figura 3)
                print("[Porto Seguro] Validando SUSEP...")
                page.wait_for_selector("input[placeholder*='SUSEP']", timeout=15000)
                page.fill("input[placeholder*='SUSEP']", self.susep)
                page.click("button:has-text('ENTRAR')")
                
                # 3. NAVEGAÇÃO PARA COTAÇÃO
                print("[Porto Seguro] Indo para tela de cálculo...")
                # Navega diretamente para a URL da cotação com a SUSEP injetada
                page.goto(self.url_cotacao, wait_until="networkidle")
                
                # 4. INJEÇÃO DE DADOS (Simulando interação humana)
                # CPF do Segurado
                page.wait_for_selector("input#cpf_segurado", timeout=20000)
                page.fill("input#cpf_segurado", dados.cpf)
                page.press("input#cpf_segurado", "Tab")
                
                # Tempo de espera para a busca automática de dados cadastrais
                time.sleep(4) 
                
                # Placa do Veículo
                page.fill("input#placa_veiculo", dados.placa)
                page.press("input#placa_veiculo", "Tab")
                
                # Tempo de espera para a busca do veículo no banco de dados
                time.sleep(4)
                
                # 5. CAPTURA DE SUCESSO
                page.screenshot(path="evidencia_sucesso_porto.png")
                print("[Porto Seguro] Injeção finalizada com sucesso.")
                
                return {
                    "status": "Sucesso na Injeção",
                    "mensagem": f"Dados de {dados.nome} inseridos no portal."
                }

            except Exception as e:
                # Em caso de erro, captura a tela para diagnóstico
                try:
                    page.screenshot(path="erro_automacao.png")
                except:
                    pass
                print(f"[Porto Seguro] Falha no processo: {str(e)}")
                return {
                    "status": "Erro na Automação",
                    "detalhes": str(e)[:100]
                }
            finally:
                browser.close()

def cotar(dados):
    """Função de entrada para o driver"""
    robo = RoboPortoSeguro()
    return robo.executar_cotacao(dados)
