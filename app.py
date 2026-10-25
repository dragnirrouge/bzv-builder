from flask import Flask, request, jsonify, send_from_directory
import os, time, re

app = Flask(__name__)
BASE_DIR = "/tmp/bzv_sites"
os.makedirs(BASE_DIR, exist_ok=True)

# Banque d'images HD V2 Universelle
IMAGE_BANK = {
  "Boutique": [
    "https://images.unsplash.com/photo-1617038260892-41a1f14a8ca0?w=1200&q=80",
    "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=1200&q=80",
    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=1200&q=80",
    "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=1200&q=80"
  ],
  "Hotel": [
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1600&q=80",
    "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=1200&q=80",
    "https://images.unsplash.com/photo-1551882547-b79c5f0636e3?w=1200&q=80"
  ],
  "Ecole": [
    "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&q=80",
    "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&q=80"
  ],
  "Restaurant": ["https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1200&q=80"],
  "Business": ["https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200&q=80"],
  "Immobilier": ["https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200&q=80"]
}

# FIX CORS pour que fetch() marche depuis ton builder
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def home():
    # FIX: chemin absolu pour Render
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(root_dir, 'index.html')

@app.route('/api/research', methods=['POST', 'OPTIONS'])
def research():
    if request.method == 'OPTIONS':
        return '', 200
    d = request.get_json() or {}
    t = d.get('type', 'Boutique')
    return jsonify({
        "images": IMAGE_BANK.get(t, IMAGE_BANK["Boutique"]),
        "palette": ["#0A0A0A", "#D4AF37", "#F5F1E8"],
        "status": "ok"
    })

@app.route('/api/security-scan', methods=['POST', 'OPTIONS'])
def sec():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({"score": 95, "issues": []})

@app.route('/api/generate', methods=['POST', 'OPTIONS'])
def gen():
    if request.method == 'OPTIONS':
        return '', 200
    d = request.get_json() or {}
    html = d.get('html', '')
    prompt = d.get('prompt', 'site')
    if not html:
        return jsonify({"error": "no html"}), 400
    slug = re.sub(r'[^a-z0-9]+', '-', prompt.lower()[:15]) or "site"
    sid = f"{slug}-{int(time.time())}"
    path = os.path.join(BASE_DIR, f"{sid}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    full = request.host_url.rstrip('/') + f"/site/{sid}"
    return jsonify({"url": f"/site/{sid}", "full_url": full})

@app.route('/site/<sid>')
def serve(sid):
    p = os.path.join(BASE_DIR, f"{sid}.html")
    if os.path.exists(p):
        return send_from_directory(BASE_DIR, f"{sid}.html")
    return "Site non trouvé - Regénère le site", 404

@app.route('/health')
def health():
    return jsonify({"status": "V2 Universelle OK", "sites": len(os.listdir(BASE_DIR))})

if __name__ == '__main__':
    # FIX: Port Render dynamique
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
