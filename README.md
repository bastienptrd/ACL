# ACL

Ensemble des backlogs et autres détails dans le projet (dossier `Sprint/`).

# EXECUTION

Le projet utilise [uv](https://docs.astral.sh/uv/) pour gérer Python et les dépendances (`pygame`).

## 1. Installer uv (une seule fois)

Linux / macOS :

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell) :

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Fermer puis rouvrir le terminal, et vérifier l'installation avec `uv --version`.

## 2. Lancer le jeu

Depuis la racine du projet :

```bash
uv run src/main.py
```

Au premier lancement, uv crée automatiquement l'environnement virtuel `.venv` et installe les dépendances. Il n'y a rien d'autre à faire (pas besoin de `pip install` ni d'activer le venv).

Il est aussi possible d'utiliser le Makefile :

```bash
make play
```

## Ajouter une dépendance

```bash
uv add <nom_du_paquet>
```

La dépendance est ajoutée au `pyproject.toml` et sera installée pour tout le monde au prochain `uv run`.

## Problèmes fréquents

- **Environnement cassé** : supprimer le dossier `.venv` (`rm -rf .venv`) puis relancer `uv run src/main.py`, il sera recréé.
- **PyCharm** : sélectionner `.venv` comme interpréteur dans _Settings → Project → Python Interpreter_.
