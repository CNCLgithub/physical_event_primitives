#!/bin/bash

. load_config.sh

# Define the path to the container and conda env
CONT="${ENV['cont']}"

# Parse the incoming command
# (xvfb-run starts a virtual display)
COMMAND="xvfb-run -a $@"

# Enter the container and run the command
SING="${ENV['path']} exec --nv"
mounts=(${ENV[mounts]})
BS=""
for i in "${mounts[@]}";do
    if [[ $i ]]; then
        BS="${BS} -B $i:$i"
    fi
done
for i in "${!PATHS[@]}"
do
  BS="${BS} -B ${PATHS[$i]}:/$i"
done
# add the repo path to "/project"
BS="${BS} -B ${PWD}:/project"


${SING} ${BS} ${CONT} bash -c "source activate $PWD/${ENV[env]} \
        && export JULIA_DEPOT_PATH=${ENV[julia_depot]} \
        && export JULIA_PROJECT=${PWD} \
        && export PYCALL_JL_RUNTIME_PYTHON=$PWD/${ENV[env]}/bin/python3 \
        && export XDG_CONFIG_HOME=$PWD/${ENV[blender_config]} \
        && cd ${PWD} \
        && exec $COMMAND \
        && source deactivate"
