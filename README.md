# physical_event_primitives
Repository for computational, behavioral, and imaging studies of physical event perception.

**Setup**

Requirements: `singularity`

***If you are working on a Linux computer, download singularity and you should be good to go! :***

1. `git clone` the repository
2. `cd physical_even_primitives`
3. `git submodule update --init` (initialized the Blender egg importer add-on)
4. `./setup.sh pull true true` (pulls the container from Box.com, sets up Conda and Julia environments). Run `./setup.sh build true true` if you want to build the container for some reason.

***If you are working on a Mac, the situation is more complicated.***

1. Follow instructions here: https://sylabs.io/guides/3.5/admin-guide/installation.html#mac to download `vagrant`, `vagrant-manager`, and `virtual box`. You need to have `Homebrew` to install this. 
2. Make sure to create the virtual machine inside of the `physical_event_primitives` directory, or in a directory that encloses it. 
3. When you want to build or pull the singularity image, go into the directory with the Vagrantfile and run `vagrant ssh`. Then `cd` into the `physical_event_primitives` directory which is located within `/vagrant/`. You can now run the above commands as if you were working on a Linux!

**Interacting with the image**

Run `./run.sh <command>` to execute commands with the image, e.g. to launch Julia REPL `./run.sh julia`.

If using Milgram and need a virtual display (e.g. rendering with Blender), run `./run.sh xvfb-run -a <command>`.


***Disclaimer: Much of this code is taken directly from http://geometry.cs.ucl.ac.uk/projects/2019/causal-graphs/ with tweaks to fit our specific situation***

Contents
--------
blender/                   Scripts used to export animations to Blender
core/                      Core package; contains all the algorithms
demos/                     Demos to play with & contains the main generate.sh script for generating videos
gui/                       Graphical modules -- mostly irrelevant here
scenarios/                 Config files of different possible scenarios


Usage
-----
You can run the script using `./run.sh demos/generate.py`
