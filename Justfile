install:
    rsync -av --delete \
      --exclude='.git' \
      --exclude='/Justfile' \
      --exclude='/README.md' \
      --exclude='/docs' \
      --exclude='/tests' \
      --exclude='/pyrightconfig.json' \
      --exclude='/requirements-dev.txt' \
      --exclude='__pycache__' \
      --exclude='.pytest_cache' \
      --exclude='.mypy_cache' \
      --exclude='.ruff_cache' \
      --exclude='.venv' \
      --exclude='typst/preview' \
      --exclude='*.pdf' \
      . ~/.agents/skills/marketing-may/

test:
    python3 -m pytest tests/ -v

test-quiet:
    python3 -m pytest tests/ -q

setup-dev:
    pip install -r requirements-dev.txt
