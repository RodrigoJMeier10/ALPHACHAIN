import requests
import json

NODE_URL = "http://localhost:5000" # Cambiar por tu IP publica

# 1. Agregar transaccion y minar
tx = {
    "sender": "Rodrigo",
    "receiver": "Ciencia", 
    "amount": 0,
    "data": "Prediccion GLIMPSE-17775 dim 3x-5x antes 15/08/2027"
}
r = requests.post(f"{NODE_URL}/mine", json=tx)
print("Bloque minado:", r.json())

# 2. Ver cadena
r = requests.get(f"{NODE_URL}/chain")
print("Largo de cadena:", len(r.json()))
