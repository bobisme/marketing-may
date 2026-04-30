install:
    rsync -av --delete --exclude='.git' --exclude='Justfile' . ~/.agents/skills/marketing-may/
