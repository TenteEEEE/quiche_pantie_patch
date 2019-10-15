FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends git python3.7-dev python3-pip build-essential
RUN python3.7 -m pip install setuptools wheel
RUN python3.7 -m pip install gunicorn uvicorn
ADD https://api.github.com/repos/TenteEEEE/quiche_pantie_patch/git/refs/heads/master version.json
RUN git clone https://github.com/TenteEEEE/quiche_pantie_patch.git --depth 1
WORKDIR /quiche_pantie_patch
RUN python3.7 -m pip install -r requirements.txt
CMD git pull ; gunicorn --bind 0.0.0.0:5000 restapi:app -k uvicorn.workers.UvicornWorker
