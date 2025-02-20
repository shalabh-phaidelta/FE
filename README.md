# FE

- Local Dev
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install
```

- What is .pre-commit-config.yaml?
This file configures automatic linting & formatting before every commit.
It ensures code follows consistent styling and best practices using:
black (Auto-formats Python code)
isort (Sorts imports)
flake8 (Checks code for PEP8 violations)
mypy (Static type checking)
✅ Whenever you commit code, these checks run automatically! If issues are found, fix them before committing.
---

- Build and Run with docker
```bash
docker-compose up --build
```
---

- Check logs
```bash
docker ps  # View running containers
docker logs fastapi-container  # View logs
```

