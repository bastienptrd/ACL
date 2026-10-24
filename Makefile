.PHONY: prettier prettier-check play

prettier:
	npx prettier --write .

prettier-check:
	npx prettier --check .

play:
	@echo "The game is starting..."
	uv run src/main.py