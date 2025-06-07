# Agent Instructions

All code changes must pass the linters and type checkers installed before committing.

## Python backend (`markdown2pdf-backend`)

Activate the virtual environment and run both `mypy` and `pylint`:

```bash
source markdown2pdf-backend/.venv/bin/activate
mypy app
pylint app
```

## JavaScript/TypeScript frontend (`markdown2pdf-webapp`)

Run ESLint over the entire project:

```bash
cd markdown2pdf-webapp
npx eslint .
cd ..
```

Only commit changes when all of the above commands succeed without errors.
