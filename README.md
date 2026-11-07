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

## Installer make (optionnel)

`make` est un programme système : il ne s'installe pas avec `uv` ni `pip`.

Linux (Debian / Ubuntu) :

```bash
sudo apt install make
```

macOS :

```bash
xcode-select --install
```

Windows (PowerShell) :

```powershell
winget install ezwinports.make
```

Fermer puis rouvrir le terminal, et vérifier l'installation avec `make --version`.

## Formater avec Prettier

[Prettier](https://prettier.io/) formate les fichiers Markdown, JSON, YAML, HTML, CSS, JS, etc. Il ne gère pas le Python.

### 1. Installer Node.js (une seule fois)

Prettier a besoin de Node.js, qui fournit les commandes `node`, `npm` et `npx`.

Windows (PowerShell) :

```powershell
winget install OpenJS.NodeJS.LTS
```

Linux (Debian / Ubuntu) :

```bash
sudo apt install nodejs npm
```

macOS :

```bash
brew install node
```

Sinon, télécharger la version LTS sur [nodejs.org](https://nodejs.org). Fermer puis rouvrir le terminal, et vérifier l'installation avec `node -v` et `npx -v`.

Sous Windows, si PowerShell indique que l'exécution de scripts est désactivée, lancer une fois :

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 2. Lancer Prettier

Depuis la racine du projet :

```bash
npx prettier --write .
```

`npx` télécharge Prettier automatiquement au premier lancement. Pour seulement vérifier le formatage sans modifier les fichiers :

```bash
npx prettier --check .
```

## Ajouter une dépendance

```bash
uv add <nom_du_paquet>
```

La dépendance est ajoutée au `pyproject.toml` et sera installée pour tout le monde au prochain `uv run`.

## Problèmes fréquents

- **Environnement cassé** : supprimer le dossier `.venv` (`rm -rf .venv`) puis relancer `uv run src/main.py`, il sera recréé.
- **PyCharm** : sélectionner `.venv` comme interpréteur dans _Settings → Project → Python Interpreter_.
- **`npx` : le terme n'est pas reconnu** : Node.js n'est pas installé ou le terminal n'a pas été rouvert après son installation.
- **`make` : le terme n'est pas reconnu** : `make` n'est pas installé ou le terminal n'a pas été rouvert après son installation.