#!/usr/bin/env python

import os
import subprocess
import argparse
from pathlib import Path
import json

# loading function from demos/import_scenario.py
from import_scenario import import_scenario


def main():

    # parsing the arguments
    parser = argparse.ArgumentParser(
        description='Scenarios generation script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('scene', type=str,
                        help='specify name of the scene')
    parser.add_argument('--trace', type=int, default = 0,
                        help = 'random seed for Gen (also determined the name of the saved JSON)')
    parser.add_argument('--debug', action='store_true',
                        help='enables debug, i.e. blender GUI (? I suppose haha)')

    parser.add_argument('--blender', type=str, default = '/blender/blender',
                        help='specify blender path')
    parser.add_argument('--scenarios', type=str, default = 'scenarios/',
                        help='specify scenarios path')

    args = parser.parse_args()

    
    # step 1 : create the scene priors file if this
    # seed has never been used before

    # TODO I would suggest writing a python script
    # with the same random calls that just returns
    # a dictionary with all of the scene random choices
    # - there is no need for the data generating procedure
    # to be in Julia. We can then pass that dictionary to import_scenario
    # instead of even loading from disk
    
    # creating directory for gen json if it doesn't exist
    scenario_dir = os.path.join(args.scenarios, args.scene)
    if not os.path.isdir(scenario_dir):
        os.mkdir(scenario_dir)

    gen_json_path = os.path.join(scenario_dir, '{trace}.gen.json'.format(trace=args.trace))
    if not os.path.isfile(gen_json_path):
        print('Creating a random instance of: {scene}'.format(scene=args.scene))
        #cmd = ['julia', 'demos/create_scene_priors.jl', args.scene, str(args.trace), gen_json_path]
        #subprocess.run(cmd)
    else:
        print('JSON file already created for this seed number. Skipping the gen step.')

    
    # step 2 : creates simu.pkl and scene.egg files
    py_scenario_path = os.path.join(args.scenarios, args.scene+'.py')
    
    # notice that a function is loaded from demos/import_scenario.py
    # (new function based on main in that file)
    import_scenario(py_scenario_path, gen_json_path, args.debug, scenario_dir, args.trace)
    
    blendfile = os.path.join(scenario_dir, '{trace}.blend'.format(trace=args.trace))
    Path(blendfile).touch()
    

    # step 3 : clean up the scene and render in blender
    eggfile = os.path.join(scenario_dir, '{trace}.egg'.format(trace=args.trace))

    if not args.debug:
        cmd = [ args.blender, '-b',
                '--python', 'demos/import.py',
                '--python', 'blender/clean_up_scene.py',
                '--python', 'blender/import_keyframes2.py',
                '--python', 'blender/render.py',
                '--',
                scenario_dir,
                str(args.trace)]

        subprocess.run(cmd)

    else:
        cmd = [ args.blender,
                '--python', 'demos/import.py',
                '--python', 'blender/clean_up_scene.py',
                '--python', 'blender/import_keyframes2.py',
                '--',
                scenario_dir,
                str(args.trace)]

        subprocess.run(cmd)

if __name__ == '__main__':
    main()
