from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
app = Flask(__name__)
CORS(app)

# Estado y historial
estado = {'tipo': 'sin_datos'}
historial = []  # Lista de dicts: {'tipo': ..., 'ts': ...}

def registrar_evento(tipo):
    ts = datetime.now().isoformat(sep=' ', timespec='seconds')
    evento = {'tipo': tipo, 'ts': ts}
    historial.append(evento)
    estado['tipo'] = tipo

@app.route('/leve', methods=['POST'])
def vibracion_leve():
    # No registrar en historial
    estado['tipo'] = 'leve'
    return ('', 204)

@app.route('/alerta', methods=['POST'])
def caida_alerta():
    print("🔥 LLEGÓ POST /alerta")
    registrar_evento('alerta')
    return ('', 204)

@app.route('/ruido', methods=['POST'])
def ruido_descartado():
    # No registrar en historial
    estado['tipo'] = 'sin_datos'
    return ('', 204)

@app.route('/state', methods=['GET'])
def get_state():
    # Solo mostrar "alerta" o "sin caídas"
    if estado['tipo'] == 'alerta':
        return jsonify({'tipo': 'alerta'})
    else:
        return jsonify({'tipo': 'sin_datos'})

@app.route('/history', methods=['GET'])
def get_history():
    # Solo mostrar eventos tipo 'alerta' (caídas) en el historial
    caidas = [evento for evento in historial if evento['tipo'] == 'alerta']
    return jsonify(caidas[-20:][::-1])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)