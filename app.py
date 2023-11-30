from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from supabase import create_client, Client

url: str = "test"
key: str = "test"
supabase: Client = create_client(url, key)


app = Flask(__name__)

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
