install:
    rsync -av --delete \
      --exclude='.git' \
      --exclude='Justfile' \
      --exclude='README.md' \
      . ~/.agents/skills/marketing-may/
