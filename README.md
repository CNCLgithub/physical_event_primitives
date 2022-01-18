# physical_event_primitives
Computational, behavioral, and imaging studies of physical event perception

Stimuli creation branch for experiment on spatiotemporal physical event probes, pioneered by high school research assistant Winnie Chen in summer 2021.

Builds upon the master branch, which was used to create stimuli for prior experiments on physical event probes by Shannon Yasuda (with help and support from Tristan Yates and Eivinas Butkus)  

General instructions for creation of stimuli, including how to make new scenarios, are located here: https://docs.google.com/document/d/1xJ4V6EtBgNww5IrMvxtNqDHQQuABxtDpIWd2z3jbRyg/edit?usp=sharing

First, create a conda environment with all of the requirements: `conda create -f conda_environment.yml`
Then, move into the demos directory and run `./generate.sh`
Supply the name of the scenario file you would like to use (e.g., collision_collision_occlusion) and whether you want to view the output in Blender (1) or immediately start the rendering (0)


