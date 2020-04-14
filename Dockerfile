FROM            ubuntu:16.04
MAINTAINER      MIT Probabilistic Computing Project

RUN             apt-get update -qq \
                && apt-get install -qq -y \
                    hdf5-tools \
                    python3-dev \
                    python3-tk \
                    wget \
                    virtualenv \
                    zlib1g-dev

RUN             apt-get install -qq -y git
RUN             git config --global user.name "Gen User"
RUN             git config --global user.email "email@example.com"

RUN             virtualenv -p /usr/bin/python3 /venv
RUN             . /venv/bin/activate && pip install jupyter jupytext matplotlib tensorflow

RUN             wget https://julialang-s3.julialang.org/bin/linux/x64/1.0/julia-1.0.3-linux-x86_64.tar.gz
RUN             tar -xzv < julia-1.0.3-linux-x86_64.tar.gz
RUN             ln -s /julia-1.0.3/bin/julia /usr/bin/julia

ADD             . /physical_event_primitives
ENV             JULIA_PROJECT=/physical_event_primitives

RUN             . /venv/bin/activate && julia -e 'using Pkg; Pkg.build()'
RUN             . /venv/bin/activate && julia -e 'using Pkg; Pkg.API.precompile()'

WORKDIR         /physical_event_primitives

ENTRYPOINT      . /venv/bin/activate && jupyter notebook \
                    --ip='0.0.0.0' \
                    --port=2020 \
                    --no-browser \
                    --NotebookApp.token= \
                    --allow-root \
                    --NotebookApp.iopub_data_rate_limit=-1
