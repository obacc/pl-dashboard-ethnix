from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from functools import wraps
import os
from excel_parser import PLExcelParser

app = Flask(__name__)

# CORS - permitir Vercel
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://pl-dashboard-ethnix.vercel.app", "https://*.vercel.app", "http://localhost:*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Basic Auth
def check_auth(username, password):
    correct_username = os.getenv('AUTH_USERNAME', 'ethnix')
    correct_password = os.getenv('AUTH_PASSWORD', 'changeme')
    return username == correct_username and password == correct_password

def authenticate():
    return Response(
        'Acceso denegado. Credenciales requeridas.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Endpoints
@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/pl')
@requires_auth
def get_pl():
    tipo = request.args.get('tipo', 'general')
    
    # Datos de ejemplo (hardcoded por ahora)
    data = [
        {
            "category": "SALES",
            "isTotal": False,
            "data": {
                "col1": 1701340, "col2": 1596643, "col3": 1729466,
                "budget": 1824160, "coberPct": 95,
                "vsBDollar": -94694, "vsBPct": -5,
                "ytd": 5027449, "ytdBudget": 5543565,
                "var": -516115, "varPct": -9
            },
            "subcategories": [
                {
                    "name": "Distribuidora Limeña",
                    "data": {
                        "col1": 1310451, "col2": 1289299, "col3": 1352435,
                        "budget": 1488160, "coberPct": 91,
                        "vsBDollar": -135725, "vsBPct": -9,
                        "ytd": 3952185, "ytdBudget": 4535565,
                        "var": -583380, "varPct": -13
                    }
                }
            ]
        },
        {
            "category": "COGS",
            "isTotal": False,
            "data": {
                "col1": 1279745, "col2": 1193257, "col3": 1292570,
                "budget": 1341177, "coberPct": 96,
                "vsBDollar": -48607, "vsBPct": -4,
                "ytd": 3765572, "ytdBudget": 4073645,
                "var": -308074, "varPct": -8
            }
        },
        {
            "category": "Gross Margin",
            "isTotal": True,
            "data": {
                "col1": 421596, "col2": 403386, "col3": 436896,
                "budget": 482983, "coberPct": 90,
                "vsBDollar": -46087, "vsBPct": -10,
                "ytd": 1261878, "ytdBudget": 1469920,
                "var": -208042, "varPct": -14
            }
        },
        {
            "category": "% Gross Margin",
            "isPercent": True,
            "data": {
                "col1": 24.8, "col2": 25.3, "col3": 25.3,
                "budget": 26.5, "coberPct": 95,
                "vsBDollar": -1.22, "vsBPct": None,
                "ytd": 25.1, "ytdBudget": 26.5,
                "var": -1.4, "varPct": None
            }
        },
        {
            "category": "EBITDA",
            "isTotal": True,
            "data": {
                "col1": 24832, "col2": 6893, "col3": 27613,
                "budget": 69975, "coberPct": 39,
                "vsBDollar": -42362, "vsBPct": -61,
                "ytd": 59339, "ytdBudget": 226420,
                "var": -167081, "varPct": -74
            }
        },
        {
            "category": "NET INCOME",
            "isTotal": True,
            "data": {
                "col1": -25342, "col2": -40691, "col3": -21629,
                "budget": 20075, "coberPct": -108,
                "vsBDollar": -41704, "vsBPct": -208,
                "ytd": -87663, "ytdBudget": 76720,
                "var": -164383, "varPct": -214
            }
        }
    ]
    
    return jsonify({"success": True, "data": data})

@app.route('/api/files')
@requires_auth
def get_files():
    return jsonify({"files": []})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

