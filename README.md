# Meu Projeto Python

![CI](https://github.com/poc_pipeline/actions/workflows/ci.yml/badge.svg

Template Python com:

- FastAPI
- Testes unitários
- Testes de integração
- Coverage
- Ruff para lint e formatação
- MyPy para type checking
- Bandit para security scan
- GitHub Actions com workflow reutilizável

## Como rodar localmente

- Crie o ambiente virtual:

```bash
python -m venv .venv
```

- Instale as dependências:

```bash
pip install -r requirements.txt
```

- Inicialize o serviço (porta 8000):

```bash
uvicorn meu_projeto.main:app --reload
```