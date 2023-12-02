import supabase
from flask import Flask, request, Response, Blueprint, jsonify
import requests

bucket_url='https://qzmfnmaqhitbkitxdwwq.supabase.co/storage/v1/object/public/books-data/'

process_data = Blueprint('process_data', __name__)

# Define your new endpoint in this Blueprint
@process_data.route('/download/<file>', methods=['GET'])
def download(file):
    response = response = requests.get(bucket_url+file)
    file_contents = response.content
    print(file_contents)
    return Response(response.content, mimetype=response.content_type)