.PHONY: prettier prettier-check play

prettier:
	npx prettier --write .

prettier-check:
	npx prettier --check .

play:
	@echo "The game is starting..."
	.venv/bin/python src/main.py
