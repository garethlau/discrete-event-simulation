from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_cors import CORS
import time
from simulation import simulation

app = Flask(__name__, static_folder="react_app/build/static", template_folder="react_app/build")
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


### Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/simulate', methods=['POST'])
def simulate():
    print(request.json)
    print("Running sim")
    result = simulation.run_sim(socketio)
    socketio.emit('sim-result', result)
    return "nice"
'''
@app.route('/ping', methods=['GET'])
def ping():
    return "pong"
'''

@socketio.on('run-sim')
def sim(config):
    print("Running simulation")
    PATIENCE = config['patience']
    VISIT_DURATION = config['duration']
    REVENUE = config['revenue']
    # CAPACITY = config['capacity']

    result = simulation.run_sim(socketio)
    socketio.emit('sim-result', result)


if __name__ == "__main__":
    print("Starting Flask server")
    app.config.from_object('configurations.DevelopmentConfig')
    socketio.run(app)