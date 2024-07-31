import time
from selenium.webdriver.common.by import By
import pyanty as dolphin
from pyanty import DolphinAPI

# Configuração da API Dolphin
API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiODUwMjIyOGU0ZmMzYzMxNTA1ODUwNzdjNTZkM2Y5MGM2NWEzYWNiNGEwNDJlYTdlMTcwZDAyYTBlMGI1Yjc4MTAzNzg1MTYwNTYxMmJhYjkiLCJpYXQiOjE3MjE4OTY3NzguMTAwNjcsIm5iZiI6MTcyMTg5Njc3OC4xMDA2NzMsImV4cCI6MTc1MzQzMjc3OC4wODkzMjUsInN1YiI6IjI2OTAzMDQiLCJzY29wZXMiOltdfQ.pwbdn5lEHU5B9th8Q6et9dgocmM8P6ZwP72MkoQtkUr3HXE_qjcN2a4LMwk6Qgyr8RKaJt1raSnhTR9V97aczQhloetwDKG4iaLPWqaX-dVXkjW9P3Ph-oklQDIc6XMpqQB7XvEOrYh0qEp33u75ADHPHsL8sOfytcs1XCfE3KWcbHkISTF1CMHeROTT8BkZRh_Ic4TnvDZuwsZNkkkaOi521kTl_7dSo9582qwnspMWtK8tNvNhWVYp4PvTV1LaWsQsTJUGB454b97TGhkH0lpQF2JyKKPkw29dC08xTcudMAHPgEZR7zRQX5tMq74A3MnIL-tJ0Zy2kDtufaTN6Uv9ty27aaxKkvgyAYvBdDYFwPxg_fAotTurLtXlXV7Rkqx6sULmfzvZLsIbHbKSEpcIZIlNNzAl--4UgxcZTWIRzBXHPw6DejWaqgADYKQiKTv2A_95zl3L0GCuxvMVPYoba3b8-Ml2pEDOft9wwk5kERWPCTMN6Y_pG_b765IGnk0p-4Ib_TrlFAVByYO0wQBLjnyKiOMDonCnRgowwjQN13VMQu4ivnfjLst4e8NabQ27u-9Kly6Dpx51rg7ou-FyZKp5Set4-JEzM4SfbNotAv8zbSxnWoyZKc8L2wVakuv0DKLsXKFrYscA-UiwBmuq-iOUS3ZYA11uh56rAtE'  # Substitua pela sua chave da API

class DolphinAutomator:
    def __init__(self):
        self.api = DolphinAPI(api_key=API_KEY)

    def locate_element(self, driver, selector, by=By.XPATH):
        try:
            return driver.find_element(by, selector)
        except Exception as e:
            print(f"Erro ao localizar o elemento com o seletor {selector}: {e}")
            return None

    def automate_profile(self, profile_id, profile_name, password='kawan123'):
        try:
            response = dolphin.run_profile(profile_id)
            port = response['automation']['port']
            
            driver = dolphin.get_driver(port=port)
            driver.get('https://cometpg.com/?id=726375406&currency=BRL&type=2')
            
            time.sleep(5)  # Esperar a página carregar

            # Tentar localizar os campos e botão com diferentes seletores
            username_field = self.locate_element(driver, "//input[@placeholder='Nome de usuário']")
            if not username_field:
                username_field = self.locate_element(driver, "input[name='username']", By.CSS_SELECTOR)
            
            password_field = self.locate_element(driver, "//input[@placeholder='Senha']")
            if not password_field:
                password_field = self.locate_element(driver, "input[name='password']", By.CSS_SELECTOR)
            
            confirm_password_field = self.locate_element(driver, "//input[@placeholder='Confirme a senha']")
            if not confirm_password_field:
                confirm_password_field = self.locate_element(driver, "input[name='confirm_password']", By.CSS_SELECTOR)
            
            register_button = self.locate_element(driver, "//button[text()='Registro']")
            if not register_button:
                register_button = self.locate_element(driver, "button#register", By.CSS_SELECTOR)
            
            # Preencher e enviar o formulário de cadastro
            if username_field and password_field and confirm_password_field and register_button:
                username_field.send_keys(profile_name)
                password_field.send_keys(password)
                confirm_password_field.send_keys(password)
                register_button.click()
            else:
                print("Não foi possível localizar todos os elementos necessários.")
            
            time.sleep(5)  # Esperar a ação de registro concluir

            driver.quit()
            dolphin.close_profile(profile_id)
            print(f"Automatizou o perfil {profile_name} com sucesso!")
        except Exception as e:
            print(f"Falha ao automatizar o perfil {profile_name}: {str(e)}")

    def get_profiles(self):
        try:
            response = self.api.get_profiles()
            return response['data']
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar perfis: {e}")
