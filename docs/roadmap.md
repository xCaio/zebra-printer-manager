## Etapa 1 — FastAPI
- Fazer:

POST   /layouts
GET    /layouts
GET    /layouts/{id}
PUT    /layouts/{id}
DELETE /layouts/{id}


## Etapa 2 — Impressoras

POST   /printers
GET    /printers
GET    /printers/{id}
PUT    /printers/{id}
DELETE /printers/{id}

## Etapa 3 - Gerador ZPL

services/zpl.py
testar tudo sem impressora.

validar se:

{{codigo}}
{{descricao}}
{{lote}}
{{qrcode}}

estão sendo substituídos corretamente

## Etapa 4 — Impressão
POST /print

Conecta na Zebra e testa:

FastAPI
   ↓
Socket
   ↓
10.79.1.141:9100
   ↓
Zebra

## Etapa 5 — Histórico

GET /print-jobs

ata                  Layout              Impressora       Status
12/08/2026 16:30      Etiqueta Produto    ZE500            OK
12/08/2026 16:32      Etiqueta Produto    ZE500            OK
12/08/2026 16:35      Almoxarifado        ZD220            ERRO

## Etapa 6 — React

Impressoras cadastradas
[ ZE500 Produção ▼ ]

IP: 10.79.1.141
Porta: 9100

🟢 Online

E teria um botão:
[ + Cadastrar impressora ]

Assim o IP é configurado uma vez.

Isso também abre caminho para futuramente ter:

🏭 Produção
    ├── ZE500
    ├── ZD220
    └── ZT410

📦 Almoxarifado
    ├── ZD220
    └── ZT230