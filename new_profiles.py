import tkinter as tk
from tkinter import ttk
import random
import json
import requests
import openpyxl

# Definição das variáveis e arrays de configuração
platforms_array = ["macos", "windows", "linux"]
vendors_array = ["Google Inc. (Intel)", "Google Inc. (NVIDIA)", "Google Inc. (AMD)", "Google Inc.",
                 "Google Inc. (Microsoft)", "Google Inc. (Unknown)", "Intel Inc.",
                 "Google Inc. (NVIDIA Corporation)"]
renderers_array = {
    "Google Inc. (Intel)": [
        "ANGLE (Intel, Intel(R) HD Graphics Family Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)"
    ],
    "Google Inc. (NVIDIA)": [
        "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7247)",
        "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.6172)"
    ],
    "Google Inc. (AMD)": [
        "ANGLE (AMD, AMD Radeon(TM) Vega 10 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.13044.0)"
    ],
    "Google Inc.": [
        "ANGLE (Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)"
    ],
    "Google Inc. (Microsoft)": [
        "ANGLE (Microsoft, Microsoft Basic Render Driver Direct3D11 vs_5_0 ps_5_0, D3D11-10.0.19041.546)",
        "ANGLE (Microsoft, Microsoft Basic Render Driver Direct3D11 vs_5_0 ps_5_0, D3D11-6.3.9600.16505)"
    ],
    "Google Inc. (Unknown)": [
        "ANGLE (Unknown, Qualcomm(R) Adreno(TM) 630 GPU Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (Unknown, Qualcomm(R) Adreno(TM) 630 GPU Direct3D11 vs_5_0 ps_5_0, D3D11-25.18.10500.0)"
    ],
    "Intel Inc.": [
        "Intel Iris OpenGL Engine"
    ],
    "Google Inc. (NVIDIA Corporation)": [
        "ANGLE (NVIDIA Corporation, GeForce RTX 3070/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 461.40)"
    ]
}
cpu = [2, 4, 6, 8, 12, 16]
memory = [2, 4, 8]

def authentication(token: str):
    return token

def get_new_user_agent(platform: str, session: requests.Session):
    version_number = random.randint(101, 107)
    options = {
        "url": f"https://anty-api.com/fingerprints/useragent?browser_type=anty&browser_version=107&platform={platform}"
    }
    response = session.get(options["url"]).json()
    if "data" in response:
        return response["data"]
    else:
        raise Exception("Can't get new user agent, something went wrong")

def create_multiple_profiles(session: requests.Session, num_profiles: int):
    workbook = openpyxl.load_workbook("./nomes.xlsx")
    sheet = workbook.active
    completed_sheet = workbook.create_sheet("Completed")
    profiles_created = []

    for i in range(num_profiles):
        current_vendor = random.choice(vendors_array)
        current_renderer = random.choice(renderers_array[current_vendor])
        current_platform = random.choice(platforms_array)
        current_user_agent = get_new_user_agent(platform=current_platform, session=session)
        proxy_info = sheet.cell(row=2, column=2).value
        proxy_parts = proxy_info.split(':')
        proxy_name = sheet.cell(row=2, column=1).value
        proxy_login = proxy_parts[2]
        proxy_password = proxy_parts[3]
        facebook_login = sheet.cell(row=2, column=3).value
        facebook_password = sheet.cell(row=2, column=4).value

        proxy_host = proxy_parts[0]
        proxy_port = proxy_parts[1]

        options = {
            "url": "https://anty-api.com/browser_profiles",
            "data": {
                "platform": current_platform,
                "browserType": "anty",
                "useragent": {
                    "mode": "manual",
                    "value": current_user_agent
                },
                "webrtc": {
                    "mode": "altered",
                    "ipAddress": None
                },
                "canvas": {
                    "mode": "real"
                },
                "webgl": {
                    "mode": "real"
                },
                "webglInfo": {
                    "mode": "manual",
                    "vendor": current_vendor,
                    "renderer": current_renderer
                },
                "geolocation": {
                    "mode": "real",
                    "latitude": None,
                    "longitude": None
                },
                "cpu": {
                    "mode": "manual",
                    "value": random.choice(cpu)
                },
                "memory": {
                    "mode": "manual",
                    "value": random.choice(memory)
                },
                "timezone": {
                    "mode": "auto",
                    "value": None
                },
                "locale": {
                    "mode": "auto",
                    "value": None
                },
                "name": proxy_name,
                "tags": [
                    ""
                ],
                "mainWebsite": "facebook",
                "notes": {
                    "username": facebook_login,
                    "password": facebook_password,
                    "content": None,
                    "color": "blue",
                    "style": "text",
                    "icon": None
                },
                "proxy": {
                    "name": f"http://{proxy_name}",
                    "host": proxy_host,
                    "port": proxy_port,
                    "type": "http",
                    "login": proxy_login,
                    "password": proxy_password
                },
                "statusId": 0,
                "doNotTrack": False
            }
        }

        try:
            response = session.post(options["url"], headers=session.headers, data=json.dumps(options["data"]))
            profile_id = get_last_browser_profile(session=session)
            profiles_created.append(profile_id['id'])
            print(f"Perfil criado com sucesso para {proxy_name}, ID: {profile_id['id']}")

            completed_sheet.append([
                sheet.cell(row=2, column=1).value,
                sheet.cell(row=2, column=2).value,
                sheet.cell(row=2, column=3).value,
                sheet.cell(row=2, column=4).value
            ])
            sheet.delete_rows(2)

        except Exception as e:
            print(f"Erro ao criar perfil para {proxy_name}: {str(e)}")

    workbook.save("./nomes.xlsx")
    workbook.close()
    session.close()
    return profiles_created

def get_last_browser_profile(session: requests.Session):
    options = {
        "url": "https://anty-api.com/browser_profiles"
    }
    response = session.get(options["url"]).json()
    if "data" in response:
        return response["data"][0]
    else:
        raise Exception("Can't get list of browser profiles")

def main(num_profiles):
    session = requests.session()
    auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZjAwY2M1N2E1Y2E3YzM5NTI4OWZjMTcxNzFmOTMzMDFiZjg3NzBjYWM3Yzk5YjU4NWRhZWVmYmIzMTA5ZmFiYzFkODEyZTU1ZDQ5ZjI1MGEiLCJpYXQiOjE3MTk2MDE3ODguMTQwMTQ1LCJuYmYiOjE3MTk2MDE3ODguMTQwMTQ4LCJleHAiOjE3MjIxOTM3ODguMTIxMTAxLCJzdWIiOiIyNjkwMzA0Iiwic2NvcGVzIjpbXX0.Q4890D2UQDqFwOQ9PtM0gwnBWTulRJU4HCyX8bj18NN3Wnm5_JYqRH6G3cs9atN391i14Hhxhhg6EkihYvCWd_UriH_z9yRaLrwQWXpPRxAwvqU0kqGvIubE85MyJ-MLwSd4GM4V1WhM7CtCde35v9wvF9Hj6kKMYq0QHW_hA93fkz8YXeyO0gFpQoudQpvLTcyYiQKoFxQNcdz8brgPJXOSmrV6LsYKkcinZLMwSxFQ68iILy8pCi6ytzCqzkpBMrXCfIYk9msToK2f_p1LPG4SLiQ1lArK-PFivIHh7vvfhhcr0yVb0PiSqM3U5zC4B8jmGZifCj4ZBrCX-6Vet2cFRQ1KUpsaX765XRLyWPNbd11C6UpcnZfTv-nmNt3ODv19X0Y0AZIPtZY9muF-Q7Yk-w85R0LeXZfZoLQ08dtv8oyoP_wqweARQrK75RROneEjgKjdTnZBI9L0WrEDZgxh-fTFSnEe8zsEUamyTrWYKexe-87FWHKTe94kuzvnN3QwsGNKhsvUYihe66tueMOWeOultujEgQGT5JtoqnQdqhoizfeu3_KtZLpyjkC4k2o6udWYw1EzqTwhys1GFMS-jR55e6Ae9hJuHrTfpW4qsOAQbcT4yzMNeZTBZa_V9EopBlFq8AZK1DgGgLfCnSUqQZx5K5UamYOGtCA862E"
    session.headers.update({
        "Authorization": f"Bearer {authentication(token=auth_token)}",
        "Content-Type": "application/json"
    })

    profiles_created = create_multiple_profiles(session=session, num_profiles=num_profiles)
    return profiles_created

def start_creation():
    num_profiles = int(num_profiles_entry.get())
    created_profiles = main(num_profiles)
    display_profiles(created_profiles)

def display_profiles(profiles):
    for profile in profiles:
        profiles_listbox.insert(tk.END, profile)

# Interface Gráfica com tkinter
root = tk.Tk()
root.title("Gerador de Perfis de Navegador")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

num_profiles_label = ttk.Label(frame, text="Número de Perfis:")
num_profiles_label.grid(row=0, column=0, sticky=tk.W)

num_profiles_entry = ttk.Entry(frame)
num_profiles_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

start_button = ttk.Button(frame, text="Iniciar Criação", command=start_creation)
start_button.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

profiles_listbox = tk.Listbox(frame, height=10, width=50)
profiles_listbox.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

root.mainloop()