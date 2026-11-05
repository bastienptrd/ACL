.PHONY: prettier prettier-check play


#rend le code pretty
prettier:
	npx prettier --write .
#regarde si le code est pretty
prettier-check:
	npx prettier --check .
#lance le jeu avec toute les dépendances dans un venv
play:
	@echo "The game is starting..."
	uv run src/main.py