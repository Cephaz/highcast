## RUN PROJECT STEP BY STEP

- https://api-portal.electricitymaps.com/ `GET THE API KEY`
- `cp .env.example .env` and change `<NEW_KEY>`
```bash
sed -i '' 's/ELECTRICITYMAPS_API_KEY=.*/ELECTRICITYMAPS_API_KEY=<NEW_KEY>/' .env
```
- `docker-compose up -d` for running the database
- `python3 -m venv .venv` for creating the virtual environment
- `source .venv/bin/activate` for activating the virtual environment
- `pip3 install -r requirements.txt` for installing the requirements
- `alembic upgrade head` for creating the tables
- `uvicorn app.main:app --reload` for running the server

## Init project
`python3 -m venv .venv`

`source .venv/bin/activate`

## Update requirements
`pip3 freeze > requirements.txt`

## Install requirements
`pip3 install -r requirements.txt`

## alembic commands
`alembic revision --autogenerate -m "message"`
`alembic upgrade head`

## pytest
`pytest tests/`
