# Importing required library and dependencies

from flask import Flask, request, render_template, json
from embedding import text_embedding
import pymongo

app = Flask(__name__)

# MongoDB connection parameters
# In production system, do not hardcode your connection parameter (including the password)

srv = [CONN_URI]
client = pymongo.MongoClient(srv, tlsAllowInvalidCertificates=True)
db = [DB_NAME]
collection = [COLL_NAME]

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/search", methods=['POST'])
def search():
    #get the data from index.html form
    forms = request.form
    search_term = forms.get('search_term')
    
    #convert search term to vector data then compare it to what has been stored in database    
    search_result = collection.aggregate([
        {
            '$search': {
                "index": "semantic",
                "knnBeta": {
                    "vector": text_embedding(search_term),
                    "k": 5,
                    "path": "text_embedding"
                }

            }
        }
    ])
    
    #list to accommodate extracted data from search result
    title = []
    description = []
    img = []
    
    for document in search_result:
        title.append(document["title"])
        description.append(document["description"])
        img.append(document["thumbnail"])
        
    #make a link list from 3 of lists to make it easier displaying to html
    link_list = zip(title,description,img) 
    return render_template("search.html", link_list=link_list)  

if __name__ =="__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT",8080)))