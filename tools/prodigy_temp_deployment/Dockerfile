FROM python:stretch

ENV PYTHONUNBUFFERED 1
ENV PRODIGY_PORT=8000
ENV PRODIGY_LOGGING=verbose

COPY *linux_x86_64.whl /root
RUN pip install /root/prodigy*.whl
RUN python -m spacy download en_core_web_md
RUN mkdir -p /root/.prodigy/
COPY ProdigyLicenseKey.txt /root/.prodigy/
COPY prodigy.json /root/.prodigy/prodigy.json
COPY ./200_sentences_cause_effect_rel_150421.jsonl /root/
RUN pip install psycopg2

ENTRYPOINT prodigy textcat.manual cm-label-eval ./root/200_sentences_cause_effect_rel_150421.jsonl  --label cause_effect_relation