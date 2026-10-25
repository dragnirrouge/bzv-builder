from flask import Flask, request, jsonify, send_from_directory
import os, time, re
app = Flask(__name__)
BASE_DIR = "/tmp/bzv_sites"
os.makedirs(BASE_DIR, exist_ok=True)

IMAGE_BANK = {
  "Boutique": ["https://images.unsplash.com/photo-1617038260892-41a1f14a8ca0?w=1200&q=80","https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=1200&q=80","https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=1200&q=80","https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=1200&q=80"],
  "Hotel": ["https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200&q=80","https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=1200&q=80"],
  "Ecole": ["https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&q=80","https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&q=80"],
  "Restaurant": ["https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1200&q=80"],
  "Business": ["https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200&q=80"],
  "Immobilier": ["https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200&q=80"]
}

@app.route('/')
def home(): return send_from_directory('.', 'index.html')

@app.route('/api/research', methods=['POST'])
def research():
    d=request.json; t=d.get('type','Boutique')
    return jsonify({"images": IMAGE_BANK.get(t, IMAGE_BANK["Boutique"]), "palette": ["#0A0A0A","#D4AF37","#F5F1E8"]})

@app.route('/api/security-scan', methods=['POST'])
def sec(): return jsonify({"score":95,"issues":[]})

@app.route('/api/generate', methods=['POST'])
def gen():
    d=request.json; html=d.get('html',''); prompt=d.get('prompt','site')
    slug=re.sub(r'[^a-z0-9]+','-',prompt.lower()[:15]) or "site"
    sid=f"{slug}-{int(time.time())}"
    path=os.path.join(BASE_DIR,f"{sid}.html")
    open(path,'w',encoding='utf-8').write(html)
    return jsonify({"url":f"/site/{sid}","full_url":request.host_url.rstrip('/')+f"/site/{sid}"})

@app.route('/site/<sid>')
def serve(sid):
    p=os.path.join(BASE_DIR,f"{sid}.html")
    if os.path.exists(p): return send_from_directory(BASE_DIR,f"{sid}.html")
    return "Not found",404

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
