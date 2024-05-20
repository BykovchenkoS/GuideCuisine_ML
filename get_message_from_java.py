from flask import Flask
import os.path
import subprocess

app = Flask(__name__)


@app.route('/api/run_code', methods=['POST'])
def run_code():
    if not os.path.exists("data.csv"):
        subprocess.run(["python", "createCSV.py"])
    subprocess.run(["python", "k-nn.py"])
    return "Ok!!!"


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="localhost", port=5050)
