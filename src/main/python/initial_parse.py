import json
import os
from pisa_client import initialise_env
from lemma_exploration_client import extract_file_data_from_params
from utils.pisa_server_control import start_server, close_server
import glob
import argparse
import json
import ast

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracting transition data from theory files.')
    parser.add_argument('--jar-path', default='/pisa/target/scala-2.13/pisa_2.13-0.1.jar')
    parser.add_argument('--isabelle-dir', default='/isabelle')
    parser.add_argument('-o', '--output-dir')    
    parser.add_argument('--job-file', default="all_files.json")
    parser.add_argument('--tracker-file', default="current.json")
    parser.add_argument('--resume', action='store_true', default=False)
    args = parser.parse_args()
    
    jar_path = args.jar_path
    isabelle_dir = args.isabelle_dir
    output_dir = args.output_dir
    job_file = args.job_file
    tracker_file_path = args.tracker_file
    resume = args.resume

    job_file_path = os.path.join(output_dir, job_file)
    tracker_file_path = os.path.join(output_dir, tracker_file_path)
    all_file_dict = json.load(open(job_file_path,'r'))
    project_idx, file_idx = json.load(open(tracker_file_path, 'r'))
    
    num_projs = len(all_file_dict)
    env_init_count = 0
    threshold = 5

    for i in range(project_idx, num_projs):
        if i == project_idx:
            start = file_idx
        else:
            start = 0
            
        project = all_file_dict[i]
        theory_files = project["theory_files"]
        for j in range(start, len(theory_files)):

            working_dir = project["working_dir"]
            theory_file_path = theory_files[j]
                        
            extract_file_data_from_params(
                jar_path, 
                isabelle_dir, 
                os.path.join(output_dir, working_dir),
                os.path.join(project["root_dir"], working_dir), 
                theory_file_path,
                resume=resume
            )

            env_init_count += 1

            if env_init_count == threshold:
                if j+1 == len(theory_files) and i < num_projs:
                    json.dump((i+1,0), open(tracker_file_path, 'w'))
                else:
                    json.dump((i,j+1), open(tracker_file_path, 'w'))
                exit(0)
    
    exit(1)

    
