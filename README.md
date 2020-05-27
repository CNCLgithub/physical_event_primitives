# physical_event_primitives
Computational, behavioral, and imaging studies of physical event perception

Master branch for physical event primitives containing details for generating stimuli (located in /causal_graphs)

**Setup**

Change directory to causal graphs -- everything is run here.

***If you are working on a Linux computer, download singularity and you should be good to go! :***

Run ./setup.sh build true true to build the Singularity image, setup the conda environment and setup julia.
Run ./setup.sh pull true true to pull the Singularity image from box, set up the conda environment, and set up julia.

***If you are working on a Mac, the situation is more complicated. ***

1. Follow instructions here: https://sylabs.io/guides/3.5/admin-guide/installation.html#mac to download vagrant, vagrant-manager, and virtual box. You need to have Homebrew to install this. 
2. Make sure to create the virtual machine inside of the physical_event_primitives directory, or in a directory that encloses it. 
3. When you want to build or pull the singularity image, go into the directory with the Vagrantfile and run 'vagrant ssh'. Then cd into the physical_event_primitives/causal_graphs directory which is located within /vagrant/. You can now run the above commands as if you were working on a Linux!

**Interacting with the image**
Run ./run.sh <command> to execute commands with the image, e.g. to launch Julia REPL ./run.sh julia.
