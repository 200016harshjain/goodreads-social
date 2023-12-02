import supabase
from flask import Flask, request, Response, Blueprint, jsonify
import requests
import json
from supabase import create_client, Client
import pandas as pd

bucket_url='https://qzmfnmaqhitbkitxdwwq.supabase.co/storage/v1/object/public/books-data/'

process_data = Blueprint('process_data', __name__)


#establish conection once only but lite
url: str = ""
key: str = ".."
supabase: Client = create_client(url, key)


# Define your new endpoint in this Blueprint
@process_data.route('/download/<file>', methods=['GET'])
def download(file):
    response = response = requests.get(bucket_url+file)
    file_contents = response.content
    return Response(response, mimetype=response)

file_path = 'book_146736008-harsh-jain.jl'

records = []
with open(file_path, 'r') as file:
    for i, line in enumerate(file, 1):  # Enumerate lines, starting at line 1
        try:
            # Strip leading/trailing whitespace and check if line is not empty
            line = line.strip()
            if line:  # This skips empty lines
                record = json.loads(line)
                records.append(record)
                
            else:
                print(f"Line {i}: Empty or whitespace only line.")
        except json.JSONDecodeError as e:
            print(f"Line {i}: JSONDecodeError: {e}")
            print(f"Line {i} content: {line}")


def insert_into_books_authors_table(data):
    
    #initially insert the book and description into books table and have a 'book-id', loop over author - insert each author (get author id) --> then insert into book author mapping
    for i in range(0,len(data)):
        book_data = {
            "book_name": df.loc[i, "title"],
            "description": df.loc[i, "description"]
        }
        book_data_response,book_count = supabase.table("books").insert(book_data).execute()
        #inserted book's 'id'
        book_id = book_data_response[1][0].get('book_id')
        #used [1][0].get() as data format  : [x,[{"book_id":value}]] 
        #do the author bit
        author_list= df.loc[i,"author"]
        for author in author_list:
            author_data,author_count=supabase.table("authors").insert({"author_name":author}).execute()
            author_id = author_data[1][0].get('author_id')
            author_book_mapping,author_book_mapping_count = supabase.table("book_author_mapping").insert({"book_id":book_id,"author_id":author_id}).execute()
        


     

df = pd.DataFrame(records)
insert_into_books_authors_table(df[['title','author','description']])

