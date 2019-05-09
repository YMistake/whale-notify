FROM python:3.7-alpine

LABEL maintainer="Anukul Thienkasemsuk"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apk update \
    && apk --no-cache add \
      bash \
      build-base \
      curl \
      gcc \
      gettext \
      git \
      libffi-dev \
      linux-headers \
      musl-dev \
      postgresql-dev \
      tini \
      jpeg-dev \
      zlib-dev

RUN pip install gunicorn

COPY . /code
WORKDIR /code

RUN pip install -r requirement.txt

ENTRYPOINT ["python"]
CMD ["flask/wsgi.py"]
