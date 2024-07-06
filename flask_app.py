from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, send_from_directory, redirect
from pipeline import handle_request, load_datasets
app = Flask(__name__, static_folder='./app/build', static_url_path='/')
load_datasets()

# cors support
from flask_cors import CORS
CORS(app)

# Serve the static index.html file
@app.route('/')
def index():
    if app.debug:
        # redirect to react dev server
        #return redirect('http://localhost:3000/', code=302)
        pass
    return send_from_directory(app.static_folder, 'index.html')


# API route to handle POST requests with JSON content
@app.route('/api/ask', methods=['POST'])
def ask():
    if request.is_json:
        data = request.get_json()
        model = "local"
        if 'model' in data.keys():
            model = data['model']
        temperature = 0.5
        if 'temperature' in data.keys():
            temperature = data['temperature']
        # Process the JSON data as needed
        response, p = handle_request(data['question'], model=model, temperature=temperature)
        
        return jsonify({"response":response, "products":p}), 200
    else:
        return jsonify({'error': 'Invalid content type, expected application/json'}), 400

if __name__ == '__main__':
    app.run(debug=True)
