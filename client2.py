import requests
import json
import random
url = "http://localhost:5000/receber_dados"
def criar_json_aleatorio():
    jsonEntrada = []
    
    for _ in range(1000):
        order_id = random.uniform(10,100)
        price = round(random.uniform(10.0, 100.0), 2)
        tax = round(random.uniform(1.0, 10.0), 2)
        jsonEntrada.append({"ID": order_id, "Price": price, "Tax": tax})
      
    return jsonEntrada

def enviar_dados():
    json_data = criar_json_aleatorio()
    response = requests.post(url, json=json_data)
    if response.status_code == 200:
        print(f"Requisição bem-sucedida: {response.json()}")
    else:
        print(f"Erro na requisição: {response.status_code}, {response.text}")


        
def main():
    while True:
        enviar_dados()
    

if __name__ == '__main__':
    main()