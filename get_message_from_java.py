from flask import Flask

app = Flask(__name__)

@app.route('/api/run_code', methods=['POST'])
def run_code():
    print("WORKS!!!!!!!")
    return "OK"
    

if __name__ == '__main__':
    app.run(host='localhost', port=5050)
