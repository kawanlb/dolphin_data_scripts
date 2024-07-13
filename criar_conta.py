import requests
import time

# Defina seu token de autenticação
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZjAwY2M1N2E1Y2E3YzM5NTI4OWZjMTcxNzFmOTMzMDFiZjg3NzBjYWM3Yzk5YjU4NWRhZWVmYmIzMTA5ZmFiYzFkODEyZTU1ZDQ5ZjI1MGEiLCJpYXQiOjE3MTk2MDE3ODguMTQwMTQ1LCJuYmYiOjE3MTk2MDE3ODguMTQwMTQ4LCJleHAiOjE3MjIxOTM3ODguMTIxMTAxLCJzdWIiOiIyNjkwMzA0Iiwic2NvcGVzIjpbXX0.Q4890D2UQDqFwOQ9PtM0gwnBWTulRJU4HCyX8bj18NN3Wnm5_JYqRH6G3cs9atN391i14Hhxhhg6EkihYvCWd_UriH_z9yRaLrwQWXpPRxAwvqU0kqGvIubE85MyJ-MLwSd4GM4V1WhM7CtCde35v9wvF9Hj6kKMYq0QHW_hA93fkz8YXeyO0gFpQoudQpvLTcyYiQKoFxQNcdz8brgPJXOSmrV6LsYKkcinZLMwSxFQ68iILy8pCi6ytzCqzkpBMrXCfIYk9msToK2f_p1LPG4SLiQ1lArK-PFivIHh7vvfhhcr0yVb0PiSqM3U5zC4B8jmGZifCj4ZBrCX-6Vet2cFRQ1KUpsaX765XRLyWPNbd11C6UpcnZfTv-nmNt3ODv19X0Y0AZIPtZY9muF-Q7Yk-w85R0LeXZfZoLQ08dtv8oyoP_wqweARQrK75RROneEjgKjdTnZBI9L0WrEDZgxh-fTFSnEe8zsEUamyTrWYKexe-87FWHKTe94kuzvnN3QwsGNKhsvUYihe66tueMOWeOultujEgQGT5JtoqnQdqhoizfeu3_KtZLpyjkC4k2o6udWYw1EzqTwhys1GFMS-jR55e6Ae9hJuHrTfpW4qsOAQbcT4yzMNeZTBZa_V9EopBlFq8AZK1DgGgLfCnSUqQZx5K5UamYOGtCA862E"

# URL base da API Dolphin Anty
base_url = 'https://api.dolphin-anty.com'

# Nomes dos perfis na ordem desejada
nomes_dos_perfis = [
    {"nome": "Denira", "id": 415539380},
    {"nome": "Eleivia", "id": 415539388},
    {"nome": "Flanesia", "id": 415539401},
    {"nome": "Gelicia", "id": 415539410},
    {"nome": "Harila", "id": 415539424},
    {"nome": "Ilania", "id": 415539431},
    {"nome": "Jonia", "id": 415539437},
    {"nome": "Kalicia", "id": 415539442},
    {"nome": "Lareana", "id": 415539450},
    {"nome": "Malucio", "id": 415539455},
    {"nome": "Nonelio", "id": 415539458},
    {"nome": "Olisia", "id": 415539463},
    {"nome": "Paniba", "id": 415539466},
    {"nome": "Quileia", "id": 415539473},
    {"nome": "Ranoria", "id": 415539481},
    {"nome": "Salina", "id": 415539488},
    {"nome": "Talba", "id": 415539496},
    {"nome": "Urielio", "id": 415539508},
    {"nome": "Vanderico", "id": 415539518},
    {"nome": "Wanisio", "id": 415539527}
]

# Função para executar o script "criar conta" em um perfil
def executar_script_criar_conta(perfil_id):
    url = f"{base_url}/browser_profiles/{perfil_id}/execute_script"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'script_name': 'criar_conta'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['task_id']
    return None

# Função para verificar o status do script em um perfil
def verificar_status(task_id):
    url = f"{base_url}/tasks/{task_id}"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            status = response.json()['status']
            if status == 'completed':
                return True
            elif status == 'failed':
                return False
        time.sleep(5)  # Espera 5 segundos antes de verificar novamente

# Ordenar perfis e executar script "criar conta"
for perfil in nomes_dos_perfis:
    perfil_id = perfil['id']
    task_id = executar_script_criar_conta(perfil_id)
    if task_id:
        print(f"Executando script 'criar conta' no perfil {perfil['nome']}...")
        if verificar_status(task_id):
            print(f"Script 'criar conta' completado no perfil {perfil['nome']}.")
        else:
            print(f"Falha ao executar o script 'criar conta' no perfil {perfil['nome']}.")
    else:
        print(f"Falha ao iniciar o script 'criar conta' no perfil {perfil['nome']}.")
