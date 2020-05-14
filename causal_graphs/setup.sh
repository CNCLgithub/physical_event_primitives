#!/bin/bash

#JULIAPATH="https://julialang-s3.julialang.org/bin/linux/x64/1.3/julia-1.3.1-linux-x86_64.tar.gz"

. load_config.sh

build=${1:-"false"}
conda=${2:-"false"}
julia=${3:-"false"}

#if [ ! -f "julia.tar.gz" ]; then
	#echo "Getting Julia binary..."
	#wget "$JULIAPATH" -O "julia.tar.gz"
#fi

if [ ! -d $PWD/.tmp ]; then
	mkdir $PWD/.tmp
fi

if [ "$build" = "true" ]; then
	echo "building..."
	SINGULARITY_TMPDIR=$PWD/.tmp sudo -E singularity build "${ENV[cont]}" Singularity
fi

if [ "$conda" = "true" ]; then
	echo "Setting up the Conda environment"
	singularity exec ${ENV[cont]} bash -c "yes | conda create -p $PWD/${ENV[env]} python=3.6"
	./run.sh python -m pip install -r requirements.txt
fi

if [ "$julia" = "true" ]; then
	# Instantiating Julia packages
	./run.sh julia -e '"using Pkg; Pkg.instantiate()"'
fi
