# syntax=docker/dockerfile1
ARG VERSION=18.04
FROM ubuntu:$VERSION
ENV USERNAME dev
# Insert your generated `pymatgen` API key below in place of
# `insert-api-key-here` before building
ENV MP_API_KEY insert-api-key-here
WORKDIR /home/$USERNAME

COPY . ./piro/

RUN apt-get update \
 && apt-get -y update \
 && apt-get install -y \
    software-properties-common \
    build-essential \
    git \
 && apt-get clean -qq

RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update \
 && apt-get -y update \
 && apt-get install -y \
    python3.7 \
    python3.7-dev \
    python3-pip \
 && apt-get clean -qq

RUN python3.7 -m pip install --upgrade \
    pip \
    setuptools \
    wheel

RUN python3.7 -m pip install --upgrade \
    numpy \
    Cython \
    jupyter \
    pymatgen \
    joblib \
    scipy \
    threadpoolctl \
    pytz

RUN git clone https://github.com/hackingmaterials/matminer.git

WORKDIR /home/$USERNAME/matminer/

# A pinned version of `matminer` with most recent `pymatgen` import patches
RUN git checkout dd6a7326dca0f28527c76a0a5a6b9198999fb558

RUN python3.7 setup.py install

WORKDIR /home/$USERNAME/piro/

RUN python3.7 setup.py develop
