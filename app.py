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
    # No registramos en historial, solo actualizamos estado
    estado['tipo'] = 'leve'
    return ('', 204)

@app.route('/alerta', methods=['POST'])
def caida_alerta():
    registrar_evento('alerta')
    return ('', 204)

@app.route('/ruido', methods=['POST'])
def ruido_descartado():
    # Parar alerta (modo sin caídas)
    estado['tipo'] = 'sin_datos'
    return ('', 204)

@app.route('/clear', methods=['POST'])
def clear_history():
    # Borra todo el historial y para la alerta
    historial.clear()
    estado['tipo'] = 'sin_datos'
    return ('', 204)

@app.route('/state', methods=['GET'])
def get_state():
    # Solo dos estados: alerta o sin_datos
    return jsonify({'tipo': 'alerta' if estado['tipo']=='alerta' else 'sin_datos'})

@app.route('/history', methods=['GET'])
def get_history():
    # Solo caídas
    caidas = [e for e in historial if e['tipo']=='alerta']
    return jsonify(caidas[-20:][::-1])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
