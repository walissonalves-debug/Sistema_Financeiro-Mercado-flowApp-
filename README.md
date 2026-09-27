# 🛒 MercadoFlow — Gestão Financeira

Sistema local de gestão financeira para mercado autônomo.
Dados salvos em banco SQLite permanente no seu computador.

---

## 📁 Estrutura dos arquivos

```
mercadoflow/
├── app.py              ← Servidor backend (Python + Flask)
├── index.html          ← Interface do sistema
├── mercadoflow.db      ← Banco de dados (criado automaticamente)
├── INICIAR.bat         ← Iniciar no Windows (duplo clique)
├── iniciar.sh          ← Iniciar no Mac/Linux
└── README.md           ← Este arquivo
```

---

## 🚀 Como usar

### Windows
1. Certifique-se de ter o **Python** instalado (https://python.org)
2. Dê **duplo clique** no arquivo `INICIAR.bat`
3. O navegador abrirá automaticamente em `http://localhost:5000`

### Mac / Linux
1. Abra o Terminal na pasta do projeto
2. Execute: `chmod +x iniciar.sh && ./iniciar.sh`
3. Acesse `http://localhost:5000` no navegador

### Manual (qualquer sistema)
```bash
# Instalar Flask (uma única vez)
pip install flask

# Iniciar o servidor
python app.py
```
Depois acesse: **http://localhost:5000**

---

## 💾 Onde ficam os dados?

Os dados ficam salvos no arquivo `mercadoflow.db` na pasta do projeto.
Este arquivo é um banco SQLite — **não apague ele**.

Para fazer backup: clique em **"Exportar Backup"** no sistema.
Para restaurar: clique em **"Importar Backup"** e selecione o arquivo `.json`.

---

## 📊 Funcionalidades

- **Dashboard** — KPIs, gráficos, evolução mensal
- **Vendas Semanais** — Dinheiro, Débito, Crédito, Pix
- **Compras Semanais** — Por fornecedor e categoria
- **Custos Fixos** — Aluguel, condomínio, energia, franquia
- **Relatório Mensal** — DRE simplificado com margem líquida
- **Backup/Restore** — Exporta e importa em JSON

---

## ⚠️ Requisitos

- Python 3.8 ou superior
- Flask (instalado automaticamente pelo script)
- Navegador moderno (Chrome, Edge, Firefox)
