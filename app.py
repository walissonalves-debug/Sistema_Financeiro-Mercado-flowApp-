"""
MercadoFlow — Backend Flask + SQLite
Rode com: python app.py
Acesse em: http://localhost:5000
"""

from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')

DB_PATH = os.path.join(os.path.dirname(__file__), 'mercadoflow.db')

# ─────────────────────────────────────────────
#  BANCO DE DADOS
# ─────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            mes       TEXT NOT NULL,
            semana    INTEGER NOT NULL,
            dinheiro  REAL DEFAULT 0,
            debito    REAL DEFAULT 0,
            credito   REAL DEFAULT 0,
            pix       REAL DEFAULT 0,
            total     REAL DEFAULT 0,
            obs       TEXT,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            mes         TEXT NOT NULL,
            semana      INTEGER NOT NULL,
            fornecedor  TEXT,
            categoria   TEXT,
            valor       REAL DEFAULT 0,
            obs         TEXT,
            criado_em   TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS custos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            mes         TEXT NOT NULL,
            categoria   TEXT NOT NULL,
            descricao   TEXT,
            valor       REAL DEFAULT 0,
            criado_em   TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
#  CORS manual (sem dependência extra)
# ─────────────────────────────────────────────

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,OPTIONS'
    return response

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

# ─────────────────────────────────────────────
#  SERVIR FRONTEND
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ─────────────────────────────────────────────
#  API — VENDAS
# ─────────────────────────────────────────────

@app.route('/api/vendas', methods=['GET'])
def get_vendas():
    mes = request.args.get('mes')
    conn = get_db()
    if mes:
        rows = conn.execute('SELECT * FROM vendas WHERE mes=? ORDER BY semana', (mes,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM vendas ORDER BY mes DESC, semana').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/vendas', methods=['POST'])
def post_venda():
    d = request.get_json()
    total = (d.get('dinheiro',0) + d.get('debito',0) +
             d.get('credito',0) + d.get('pix',0))
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO vendas (mes,semana,dinheiro,debito,credito,pix,total,obs) VALUES (?,?,?,?,?,?,?,?)',
        (d['mes'], d['semana'], d.get('dinheiro',0), d.get('debito',0),
         d.get('credito',0), d.get('pix',0), total, d.get('obs',''))
    )
    conn.commit()
    row = conn.execute('SELECT * FROM vendas WHERE id=?', (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201

@app.route('/api/vendas/<int:vid>', methods=['DELETE'])
def delete_venda(vid):
    conn = get_db()
    conn.execute('DELETE FROM vendas WHERE id=?', (vid,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

# ─────────────────────────────────────────────
#  API — COMPRAS
# ─────────────────────────────────────────────

@app.route('/api/compras', methods=['GET'])
def get_compras():
    mes = request.args.get('mes')
    conn = get_db()
    if mes:
        rows = conn.execute('SELECT * FROM compras WHERE mes=? ORDER BY semana', (mes,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM compras ORDER BY mes DESC, semana').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/compras', methods=['POST'])
def post_compra():
    d = request.get_json()
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO compras (mes,semana,fornecedor,categoria,valor,obs) VALUES (?,?,?,?,?,?)',
        (d['mes'], d['semana'], d.get('fornecedor',''), d.get('categoria',''),
         d.get('valor',0), d.get('obs',''))
    )
    conn.commit()
    row = conn.execute('SELECT * FROM compras WHERE id=?', (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201

@app.route('/api/compras/<int:cid>', methods=['DELETE'])
def delete_compra(cid):
    conn = get_db()
    conn.execute('DELETE FROM compras WHERE id=?', (cid,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

# ─────────────────────────────────────────────
#  API — CUSTOS FIXOS
# ─────────────────────────────────────────────

@app.route('/api/custos', methods=['GET'])
def get_custos():
    mes = request.args.get('mes')
    conn = get_db()
    if mes:
        rows = conn.execute('SELECT * FROM custos WHERE mes=? ORDER BY categoria', (mes,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM custos ORDER BY mes DESC, categoria').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/custos', methods=['POST'])
def post_custo():
    d = request.get_json()
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO custos (mes,categoria,descricao,valor) VALUES (?,?,?,?)',
        (d['mes'], d['categoria'], d.get('descricao',''), d.get('valor',0))
    )
    conn.commit()
    row = conn.execute('SELECT * FROM custos WHERE id=?', (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201

@app.route('/api/custos/<int:cid>', methods=['DELETE'])
def delete_custo(cid):
    conn = get_db()
    conn.execute('DELETE FROM custos WHERE id=?', (cid,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

# ─────────────────────────────────────────────
#  API — RESUMO (dashboard)
# ─────────────────────────────────────────────

@app.route('/api/resumo', methods=['GET'])
def get_resumo():
    mes = request.args.get('mes')
    conn = get_db()

    if mes:
        vendas = conn.execute('SELECT * FROM vendas WHERE mes=?', (mes,)).fetchall()
        compras = conn.execute('SELECT * FROM compras WHERE mes=?', (mes,)).fetchall()
        custos = conn.execute('SELECT * FROM custos WHERE mes=?', (mes,)).fetchall()
    else:
        vendas = conn.execute('SELECT * FROM vendas').fetchall()
        compras = conn.execute('SELECT * FROM compras').fetchall()
        custos = conn.execute('SELECT * FROM custos').fetchall()

    conn.close()

    receita = sum(r['total'] for r in vendas)
    custo_compras = sum(r['valor'] for r in compras)
    custos_fixos = sum(r['valor'] for r in custos)
    lucro_bruto = receita - custo_compras
    lucro_liq = lucro_bruto - custos_fixos
    margem = (lucro_liq / receita * 100) if receita > 0 else 0

    return jsonify({
        'receita': receita,
        'custo_compras': custo_compras,
        'custos_fixos': custos_fixos,
        'lucro_bruto': lucro_bruto,
        'lucro_liq': lucro_liq,
        'margem': round(margem, 2),
        'num_vendas': len(vendas),
        'num_compras': len(compras),
    })

# ─────────────────────────────────────────────
#  API — BACKUP / RESTORE
# ─────────────────────────────────────────────

@app.route('/api/backup', methods=['GET'])
def backup():
    conn = get_db()
    data = {
        'vendas':  [dict(r) for r in conn.execute('SELECT * FROM vendas').fetchall()],
        'compras': [dict(r) for r in conn.execute('SELECT * FROM compras').fetchall()],
        'custos':  [dict(r) for r in conn.execute('SELECT * FROM custos').fetchall()],
        'gerado_em': datetime.now().isoformat()
    }
    conn.close()
    from flask import Response
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename=backup_mercadoflow_{datetime.now().strftime("%Y%m%d")}.json'}
    )

@app.route('/api/restore', methods=['POST'])
def restore():
    data = request.get_json()
    conn = get_db()
    try:
        if 'vendas' in data:
            conn.execute('DELETE FROM vendas')
            for r in data['vendas']:
                conn.execute(
                    'INSERT INTO vendas (id,mes,semana,dinheiro,debito,credito,pix,total,obs,criado_em) VALUES (?,?,?,?,?,?,?,?,?,?)',
                    (r['id'],r['mes'],r['semana'],r['dinheiro'],r['debito'],r['credito'],r['pix'],r['total'],r.get('obs',''),r.get('criado_em',''))
                )
        if 'compras' in data:
            conn.execute('DELETE FROM compras')
            for r in data['compras']:
                conn.execute(
                    'INSERT INTO compras (id,mes,semana,fornecedor,categoria,valor,obs,criado_em) VALUES (?,?,?,?,?,?,?,?)',
                    (r['id'],r['mes'],r['semana'],r.get('fornecedor',''),r.get('categoria',''),r['valor'],r.get('obs',''),r.get('criado_em',''))
                )
        if 'custos' in data:
            conn.execute('DELETE FROM custos')
            for r in data['custos']:
                conn.execute(
                    'INSERT INTO custos (id,mes,categoria,descricao,valor,criado_em) VALUES (?,?,?,?,?,?)',
                    (r['id'],r['mes'],r['categoria'],r.get('descricao',''),r['valor'],r.get('criado_em',''))
                )
        conn.commit()
        conn.close()
        return jsonify({'ok': True, 'msg': 'Backup restaurado com sucesso!'})
    except Exception as e:
        conn.close()
        return jsonify({'ok': False, 'msg': str(e)}), 400

# ─────────────────────────────────────────────
#  START
# ─────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    print("\n" + "="*50)
    print("  🛒  MercadoFlow — Servidor iniciado!")
    print("  Acesse: http://localhost:5000")
    print("  Banco:  mercadoflow.db")
    print("  Para encerrar: Ctrl+C")
    print("="*50 + "\n")
    app.run(debug=False, port=5000, host='0.0.0.0')
