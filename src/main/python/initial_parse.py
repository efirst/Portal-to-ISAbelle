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
    # parser.add_argument('--jar-path', '-jp', help='Path to the jar file', default=None)
    # parser.add_argument('--isabelle-path', '-ip', help='Path to the Isabelle installation', default=None)
    # parser.add_argument('--extraction-file-directory', '-efd', help='Where the parsed json files are')
    # parser.add_argument('--saving-directory', '-sd', help='Where to save the translation pairs')
    parser.add_argument('--all_files', default=None)
    parser.add_argument('--current', default=None)
    parser.add_argument('--resume', action='store_true', default=False)
    args = parser.parse_args()

    all_files_path = args.all_files
    current_path = args.current
    resume = args.resume

    all_file_dict = json.load(open(all_files_path,'r'))
    current_tup = json.load(open(current_path, 'r')) # tuple, where first element is the proj_idx, second is the file_idx
    # ast.literal_eval(line)
    print(current_tup)


    jar_path = "/pisa/target/scala-2.13/pisa_2.13-0.1.jar"
    isabelle_dir = "/isabelle"
    output_dir = "/pisa/extracted-examples-test"

    # working_dir = "/isabelle/src/HOL/IMP/"
    # all_thy_files = glob.glob("/isabelle/src/HOL/IMP/*.thy")
    # print(len(all_thy_files))

    # all_files_path = "/pisa/all_files.json"
    # all_files_dict = {}
    # working_dirs = [working_dir] 
    # proj_idx = 0
    # for wd in working_dirs:
    #     glob_path = wd + "**/*.thy"
    #     print(glob_path)
    #     thy_files = glob.glob(glob_path, recursive=True)
    #     all_files_dict[proj_idx] = {"wd": wd, "tf": thy_files}
    # json.dump(all_files_dict, open(all_files_path, 'w'))

    # exit()

    num_projs = len(list(all_file_dict.keys()))


    env_init_count = 0
    threshold = 10
    # for theory_file_path in all_thy_files:

    for i in range(current_tup[0], num_projs):

        start = 0
        if i == current_tup[0]:
            start = current_tup[1]

        for j in range(start, len(all_file_dict[str(i)]["tf"])):

            working_dir = all_file_dict[str(i)]["wd"]
            theory_file_path = all_file_dict[str(i)]["tf"][j]
                        
            extract_file_data_from_params(
                jar_path, 
                isabelle_dir, 
                output_dir,
                working_dir, 
                theory_file_path,
                resume=resume
            )

            env_init_count += 1

            if env_init_count == threshold:
                if j+1 == len(all_file_dict[str(i)]["tf"]):
                    json.dump((i+1,0), open(current_path, 'w'))
                else:
                    json.dump((i,j+1), open(current_path, 'w'))
                exit(0)
    
    exit(1)

    
