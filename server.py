from flask import Flask
from alphachain import Alphachain

app = Flask(__name__)
bc = Alphachain(node_name="Rodrigo_Replit")

@app.route('/')
def home():
    return f"ALPHACHAIN Online! Bloques: {len(bc.chain)} | Balance: {bc.get_balance('Rodrigo_Replit')} ALPHA"

@app.route('/mine_prediction')
def mine_prediction():
    bc.add_transaction("Rodrigo", "Ciencia", 0, "Prediccion: GLIMPSE-17775 dim 3x-5x antes 15/08/2027")
    bc.mine_block()
    return "Bloque minado y timestampiado!"

app.run(host='0.0.0.0', port=8080)
