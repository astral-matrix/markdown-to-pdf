# Agent Instructions

All code changes must pass the linters and type checkers installed before committing.

## Python backend (`markup2pdf-backend`)

Activate the virtual environment and run both `mypy` and `pylint`:

```bash
source markup2pdf-backend/.venv/bin/activate
mypy app
pylint app
```

## JavaScript/TypeScript frontend (`markup2pdf-webapp`)

Run ESLint over the entire project:

```bash
cd markup2pdf-webapp
npx eslint .
cd ..
```

Only commit changes when all of the above commands succeed without errors.
