# ecommerse
Django tutorial for beetroot veteran 3

# Setup
`curl -Ls https://astral.sh/uv/install.sh | sh`

`export PATH="$HOME/.cargo/bin:$PATH"`

`source ~/.bashrc    # or ~/.zshrc depending on your shell`

`uv --version`

``` bash
uv venv      # optional: creates `.venv` if needed
uv pip install -r uv.lock
```

```bash
docker-compose up -d  # run in the background
```

`python manage.py migrate`  # apply migrations

`python manage.py runserver`  # run the server
