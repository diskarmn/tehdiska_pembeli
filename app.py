import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask,render_template,redirect,url_for,jsonify,request
from pymongo import MongoClient

app=Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI)
db=client[DB_NAME]
# mongo_string='mongodb://diskarmn:Diska123@ac-sjiapka-shard-00-00.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-01.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-02.3lnlkgx.mongodb.net:27017/?ssl=true&replicaSet=atlas-vnije0-shard-0&authSource=admin&retryWrites=true&w=majority'
# client=MongoClient(mongo_string)
# db=client.tehdiska

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/pesan',methods=['POST','GET'])
def pesan():
    original=request.form['k_original']
    strawberry=request.form['k_strawberry']
    nama=request.form['k_nama']
    nohp=request.form['k_nohp']
    request_p=request.form['k_request']
    harga_original= 3000 * int(original)
    harga_strawberry= 4000 * int(strawberry)
    total=harga_original+harga_strawberry 
    nomor=db.pelanggan.count_documents({})
    urutan=nomor + 1
    data={
            'num':urutan,
            'nama':nama,
            'nohp':nohp,
            'request':request_p,
            'original':int(original),
            'strawberry':int(strawberry),
            'total_bayar':total,
            'status':'belum'
        }
    db.pelanggan.insert_one(data)
    return jsonify({'pesan':'berhasil syanag',
                    'nama':nama,'nohp':nohp,
                    'request_p':request_p,
                    'teh_original':int(original),
                    'teh_strawberry':int(strawberry),
                    'total_bayar':total})

@app.route("/tampilp",methods=['GET'])
def tampilp():
    semuap=list(db.status.find({},{'_id': False}))
    return jsonify({'semuap':semuap})
  
@app.route('/pemberitahuan',methods=['GET'])
def pemberitahuan():
    return render_template('pemberitahuan.html')


if __name__=='__main__':
    app.run('0.0.0.0',port=5000,debug=True)