from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from process_book_data import process_data

url: str = ""
key: str = ""
supabase: Client = create_client(url, key)


app = Flask(__name__)


app.register_blueprint(process_data, url_prefix='/process_data')

# Endpoint to create a user
@app.route('/create_user', methods=['POST'])
def create_user():
    user_id = request.json.get('user_id')
    user_name = request.json.get('user_name')
    email = request.json.get('email')

    # Insert data into the database
    data, count = supabase.table('users').insert({"user_id":user_id, "user_name":user_name, "email":email}).execute()
    return jsonify({
        'user_id': user_id,
        'user_name': user_name,
        'email': email,
        'status': 'User created successfully (simulated)'
    })
if __name__ == '__main__':
    app.run(debug=True)
