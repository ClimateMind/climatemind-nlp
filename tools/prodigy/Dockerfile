FROM python:stretch
LABEL version="1.0"

ENV PYTHONUNBUFFERED 1
ENV PRODIGY_ALLOWED_SESSIONS anthony,sampath,shweta,mukut,nikita,vivek

COPY *linux_x86_64.whl /root
RUN pip install /root/prodigy*.whl
RUN python -m spacy download en_core_web_md
RUN mkdir -p /root/.prodigy/
COPY ProdigyLicenseKey.txt /root/.prodigy/
COPY prodigy.json /root/.prodigy/prodigy.json
COPY data.jsonl /root/
RUN pip install psycopg2

ENTRYPOINT prodigy ner.manual climatemind_onto en_core_web_md ./root/data.jsonl --label STRENGTH,MODIFIER,HEAD,PREDICATE,GROUP