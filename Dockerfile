ARG libpq_dev_version=9.6.17-0+deb9u1

FROM python:3.7-slim-stretch AS base
#####

FROM base as builder
ARG libpq_dev_version

WORKDIR /code

# hadolint ignore=DL3008,DL3015
RUN apt-get update && \ 
    # installing basic tool chain
    apt-get -y install git procps curl vim net-tools

# requirement for postgreql
RUN apt-get install -y --no-install-recommends "libpq-dev=$libpq_dev_version"

# hadolint ignore=DL3013
RUN pip install virtualenv
RUN virtualenv venv && chmod a+x venv/bin/activate

RUN /bin/bash -c 'source venv/bin/activate && python -m pip install pip==19.2.1'
RUN /bin/bash -c 'source venv/bin/activate && pip install --upgrade setuptools newrelic'

COPY requirements.txt .
RUN /bin/bash -c 'source venv/bin/activate && pip install -r requirements.txt'

###

FROM base
ARG libpq_dev_version

WORKDIR /code

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        "libpq-dev=$libpq_dev_version" procps && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /code/ .
COPY . .

WORKDIR /code/user

ENV PATH="/code/venv/bin:$PATH"
