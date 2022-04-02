[![Join the chat at https://gitter.im/satzbeleg/community](https://badges.gitter.im/satzbeleg/community.svg)](https://gitter.im/satzbeleg/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/satzbeleg/simiscore-semantic.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/simiscore-semantic/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/satzbeleg/simiscore-semantic.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/simiscore-semantic/context:python)


# simiscore-semantic
An ML API to compute semantic similarity scores between sentence examples. 
The API is programmed with the [`fastapi` Python package](https://fastapi.tiangolo.com/), 
and the semantic similarities are computed based on [SBert (`sentence-transformers` package)](https://github.com/UKPLab/sentence-transformers). 
The deployment is configured for Docker Compose.



## Docker Deployment
Call Docker Compose

```sh
export API_PORT=12345
docker-compose -f docker-compose.yml up --build

# or as oneliner:
API_PORT=12345 docker-compose -f docker-compose.yml up --build
```

(Start docker daemon before, e.g. `open /Applications/Docker.app` on MacOS).

Check

```sh
curl http://localhost:12345
curl "http://127.0.0.1:12345/items/5?q=somequery"
```

Notes: Only `main.py` is used in `Dockerfile`.



## Local Development

### Install a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Specify where to store the SBert model
SBert allows to set the `cache_folder` via the environment variable `SENTENCE_TRANSFORMERS_HOME` (See [here](https://github.com/UKPLab/sentence-transformers/blob/bd19871d99068f4824ff6ef213d91596885889f7/sentence_transformers/SentenceTransformer.py#L48)).

```sh
mkdir ./sbert-models
export SENTENCE_TRANSFORMERS_HOME="$(pwd)/sbert-models"
```


### Start Server

```sh
source .venv/bin/activate

gunicorn app.main:app --reload \
    --bind=localhost:12345 \
    --worker-class=uvicorn.workers.UvicornH11Worker \
    --workers=2
```


### Usage Examples

a) Send a list of strings.

```sh
curl -X 'POST' \
  'http://localhost:12345/similarities/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
    "Der Film ist super.",
    "Der Spielfilm ist gut.",
    "Der Film ist Müll.",
    "Der Spielfilm ist schlecht."
  ]'
```

b) Send an JSON object with UUID4 as keys and text as values.

```sh
curl -X 'POST' \
  'http://localhost:12345/similarities/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "80ba0456-1d26-4d22-8e80-113b919502ee": "Der Film ist super.",
    "a47fe293-26e7-40f0-b0b5-202e0955458f": "Der Spielfilm ist gut.",
    "86e356a3-5b42-4e03-91fc-cf69098b6dd2": "Der Film ist Müll.",
    "779d0245-8f54-49ec-9f0f-8e29dc987b41": "Der Spielfilm ist schlecht."
   }'
```

### Other commands and help
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`
- Show the docs: [http://localhost:12345/docs](http://localhost:12345/docs)
- Show Redoc: [http://localhost:12345/redoc](http://localhost:12345/redoc)


### Clean up 
```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


## Appendix

### Support
Please [open an issue](https://github.com/satzbeleg/simiscore-semantic/issues) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/satzbeleg/simiscore-semantic/compare/).
