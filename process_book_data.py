import supabase
from flask import Flask, request, Response, Blueprint, jsonify

app = Flask(__name__)
client = supabase.create_client(
    'https://<your-project-id>.supabase.co',
    '<your-anon-key>'
)


user_routes = Blueprint('user_routes', __name__)

# Define your new endpoint in this Blueprint
@user_routes.route('/download/<bucket>/<file>')
def download(bucket, file):
    response = client.storage.from_(bucket).download(file)
    print(response)
    if response.error:
        return Response('Error downloading file', status=500)
    else:
        return Response(response.content, mimetype=response.content_type)