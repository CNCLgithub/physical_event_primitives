# physical_event_primitives
Computational, behavioral, and imaging studies of physical event perception

----------------------------------------------------------------------------
----------------------------------------------------------------------------

Branch for using Gen/Julia in order to choose the random elements to be implemented with the scene

----------------------------------------------------------------------------
----------------------------------------------------------------------------

Use Docker to set up the environment for using Julia in Jupyter notebooks:
(Instructions taken/adapted from https://github.com/probcomp/gen-quickstart.git)
1. Check that you are in the project home directory: (/physical_event_primitives)
2. On the command line, run: docker build -t events:v0 .
3. Wait for build to finish (be patient!) then run: docker run -p 2020:2020 -v ~/Desktop/github_code/physical_event_primitives:/physical_event_primitives --name events events:v0
4. Open the notebooks using localhost:2020 on your browser
5. Save your work! If you need to exit, simply use ctrl+c
6. Revisit the notebooks by running: docker start -ia events

Download Docker here: https://www.docker.com/products/docker-desktop


```python

```
