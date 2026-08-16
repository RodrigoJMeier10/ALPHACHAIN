from flask import Flask, request, jsonify
import requests
import threading
from alphachain import Alphachain # Importamos el de Nivel 5

app = Flask(__name__)
bc = Alphachain(node_name="Rodrigo")
PEERS = set() # Lista de otros nodos

@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    bc.add_transaction(data['sender'], data['receiver'], data['amount'], data['data'])
    block = bc.mine_block()
    broadcast_block(block) # Avisar a todos los peers
    return jsonify(block), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify([b.to_dict() for b in bc.chain]), 200

@app.route('/add_peer', methods=['POST'])
def add_peer():
    peer = request.get_json()['peer']
    PEERS.add(peer)
    return jsonify({"msg": f"Peer {peer} agregado"}), 201

def broadcast_block(block):
    for peer in PEERS:
        try: requests.post(f"{peer}/receive_block", json=block, timeout=2)
        except: pass

@app.route('/receive_block', methods=['POST'])
def receive_block():
    block = request.get_json()
    # Acá validarías y agregarías si es más larga
    print(f"Bloque recibido de la red: {block['index']}")
    return jsonify({"msg": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
