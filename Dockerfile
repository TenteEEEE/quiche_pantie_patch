FROM python:3.12-slim

ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add project files
ADD https://api.github.com/repos/TenteEEEE/quiche_pantie_patch/git/refs/heads/master version.json
RUN git clone https://github.com/TenteEEEE/quiche_pantie_patch.git --depth 1
WORKDIR /quiche_pantie_patch

# Install project dependencies
RUN poetry install --no-dev

# Set the entrypoint
CMD ["sh", "-c", "git pull && poetry run gunicorn --bind 0.0.0.0:5000 restapi:app -k uvicorn.workers.UvicornWorker"]