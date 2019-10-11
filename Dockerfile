FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends git python3.7-dev python3-dev python3-pip build-essential
RUN pip3 install setuptools wheel gunicorn uvicorn
ADD https://api.github.com/repos/TenteEEEE/quiche_pantie_patch/git/refs/heads/master version.json
RUN git clone https://github.com/TenteEEEE/quiche_pantie_patch.git --depth 1
WORKDIR /quiche_pantie_patch
RUN pip3 install -r requirements.txt
CMD git pull ; gunicorn --bind 0.0.0.0:5000 restapi:app -k uvicorn.workers.UvicornWorker
