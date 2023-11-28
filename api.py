from flask import Flask, request, jsonify
import random
import multiprocessing
import time
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
dados_agregados = []
lock = multiprocessing.Lock()
num_processos = 2

def processar_dados(dado):
    # current_process = multiprocessing.current_process()
    # print(f"Processo atual: {current_process.name}, PID: {current_process.pid}")
    print(dado)
    order_id = dado["ID"]
    finalPrice = dado['Price'] * 0.10
    tax = dado['Tax']
    cod_uuid = random.randint(1, 5000)

    with lock:
        return {"ID": order_id, "Final Price": finalPrice, "Tax": tax, "UUID": cod_uuid}

@app.route('/receber_dados', methods=['POST'])
def receber_dados():
    try:
        inicio = time.time()
        dados_json = request.json

        # Criar um pool de processos com o número de processos desejado
        print("\nIniciando pool de processos...")
        pool = multiprocessing.Pool(processes=num_processos)
        # Dividir o JSON em partes
        partes_json = [dados_json[i::num_processos] for i in range(num_processos)]
        print("Dividindo JSON em partes...")
        # Aplicar a função processar_dados para cada parte usando o pool
        resultados = pool.map(processar_dados, [parte for partes_json in partes_json for parte in partes_json])
        
        dados_agregados.append(resultados)
        # Fechar o pool
        pool.close()
        pool.join()
        fim = time.time()
        tempo = (fim - inicio) * 1000
        print(tempo)
        print("Processo Conluido...\n")
        return jsonify({"mensagem": "Dados recebidos com sucesso", "Resultados": resultados})

    except Exception as e:
        return jsonify({"erro": str(e)})

@app.route('/pesquisar_dados', methods=['GET'])
def pesquisar_dados():
    return jsonify({"Dados": dados_agregados})

@app.route('/pesquisar_compra', methods=['GET'])
def pesquisar_compra():
    dados_json = request.json
    print(dados_json["UUID"])
    for resultado in dados_agregados:
        for compra in resultado:
            print(compra)
            if compra["UUID"] == dados_json['UUID']:
                return jsonify({"Compra": compra})

    return jsonify({"mensagem": "Compra não encontrada"})    

if __name__ == '__main__':
    app.run(debug=True)
