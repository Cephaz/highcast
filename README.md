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
