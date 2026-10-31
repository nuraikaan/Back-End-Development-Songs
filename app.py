from flask import Flask,jsonify,request
from pathlib import Path
import json
app=Flask(__name__); DATA_FILE=Path(__file__).with_name('songs.json')
def load(): return json.loads(DATA_FILE.read_text())
def save(x): DATA_FILE.write_text(json.dumps(x,indent=2))
@app.get('/health')
def health(): return jsonify({'status':'OK'})
@app.get('/count')
def count(): return jsonify({'count':len(load())})
@app.get('/song')
def songs(): return jsonify(load())
@app.get('/song/<int:sid>')
def song(sid):
 x=next((s for s in load() if s['id']==sid),None); return (jsonify(x),200) if x else (jsonify({'error':'Song not found'}),404)
@app.post('/song')
def post():
 x=request.get_json(silent=True) or {}; data=load()
 if 'id' not in x: return jsonify({'error':'Missing id'}),400
 if any(s['id']==x['id'] for s in data): return jsonify(x),409
 data.append(x); save(data); return jsonify(x),201
@app.put('/song/<int:sid>')
def put(sid):
 x=request.get_json(silent=True) or {}; data=load()
 for i,s in enumerate(data):
  if s['id']==sid: data[i]={**s,**x,'id':sid}; save(data); return jsonify(data[i])
 return jsonify({'error':'Song not found'}),404
@app.delete('/song/<int:sid>')
def delete(sid):
 data=load(); new=[s for s in data if s['id']!=sid]
 if len(new)==len(data): return jsonify({'error':'Song not found'}),404
 save(new); return jsonify({'status':'Deleted'})
if __name__=='__main__': app.run(host='0.0.0.0',port=5002)
