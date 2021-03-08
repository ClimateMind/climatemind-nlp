FROM python:stretch
LABEL version="1.0"

ENV PYTHONUNBUFFERED 1

COPY *linux_x86_64.whl /root
RUN pip install /root/prodigy*.whl
RUN python -m spacy download en_core_web_md
RUN mkdir -p /root/.prodigy/
COPY ProdigyLicenseKey.txt /root/.prodigy/
COPY prodigy.json /root/.prodigy/prodigy.json
COPY data_split_on_sentences.jsonl /root/
RUN pip install psycopg2

ENTRYPOINT prodigy textcat.manual cm_cause_effect_rel ./root/data_split_on_sentences.jsonl  --label cause_effect_relation,none