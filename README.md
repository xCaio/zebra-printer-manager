# Printer Manager — Backend

API FastAPI para gerenciamento de impressoras Zebra em rede, layouts ZPL e histórico de impressão.

## Tecnologias

- Python 3.10+
- FastAPI e Uvicorn
- SQLAlchemy + Alembic
- PostgreSQL

## Configuração

No diretório do backend, crie e ative um ambiente virtual e instale as dependências:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crie `.env` a partir de `.env.example` e informe a conexão PostgreSQL:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/printer_manager
```

Execute as migrations antes de iniciar a API:

```bash
alembic upgrade head
```

## Execução

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em `http://localhost:8000` e a documentação interativa em `http://localhost:8000/docs`.

## CORS

O backend permite origens locais do Vite (`http://localhost:5173` e `http://localhost:5174`). Inclua outra origem em `app/main.py` quando necessário.

## Endpoints

### Impressoras

- `POST /printers/` — cria uma impressora (`name`, `ip`, `port`).
- `GET /printers/` — lista impressoras.
- `GET /printers/status` — verifica conexão TCP e retorna o estado `online`.
- `GET /printers/{id}` — consulta uma impressora.
- `GET /printers/{id}/status` — consulta status de conexão individual.
- `POST /printers/{id}/test` — envia teste de impressão.
- `PATCH /printers/{id}` — edita dados da impressora.
- `PATCH /printers/{id}/status` — altera o estado `active`.
- `DELETE /printers/{id}` — remove a impressora.

`active` representa se a impressora está habilitada no sistema; `online` representa a conectividade TCP no momento da verificação.

### Layouts

- `POST /layouts/` — cria layout com `name`, `description` e `zpl_template`.
- `GET /layouts/` — lista layouts.
- `GET /layouts/{id}` — retorna detalhes e os campos `{{campo}}` identificados no ZPL.
- `POST /layouts/{id}/preview` — renderiza o ZPL com `{ "data": { "campo": "valor" } }`.

### Impressão e histórico

- `POST /print/` — envia uma etiqueta. Payload: `printer_id`, `layout_id`, `quantity` (mínimo 1) e `data`.
- `GET /print/` — lista jobs com paginação e filtros `page`, `limit`, `printer_id`, `layout_id` e `status`.
- `GET /print/{id}` — consulta um job específico.

## Observações

- O ZPL é enviado diretamente pela API à impressora configurada, normalmente na porta 9100.
- Erros de renderização, impressora inativa ou conexão TCP são retornados pela API e gravados no histórico quando aplicável.
