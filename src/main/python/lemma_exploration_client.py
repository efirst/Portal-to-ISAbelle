import argparse
import json
import os
from pisa_client import initialise_env
from data_extraction.extract_data import extract_test_file_from_params, analyse_file_string_with_defs
from utils.pisa_server_control import start_server, close_server
from lemma_exploration_utils import get_global_facts, get_local_facts, get_constants_from_theorem_statement, get_module_name

def parse_args():
    parser = argparse.ArgumentParser(
                    prog='Lemma Exploration Extraction Client')
    parser.add_argument('--jar-path', default='/pisa/target/scala-2.13/pisa_2.13-0.1.jar')
    parser.add_argument('--isabelle-dir', default='/isabelle')
    parser.add_argument('-o', '--output-dir', default='/pisa/extracted')
    parser.add_argument('--working-dir')
    parser.add_argument('-f', '--files', nargs='*')
    parser.add_argument('--resume', action='store_true', default=False)
    return parser.parse_args()

def get_theory_files(working_dir):
    print(f"Getting theory files from {working_dir}")
    for root, dirs, files in os.walk(working_dir):
        for file in files:
            if file.endswith(".thy"):
                yield os.path.join(root, file)

def init_server(jar_path, isabelle_dir, output_dir, working_dir, theory_file_path, port=8000):
    module_name = get_module_name(theory_file_path)
    sub_output_path = f"{output_dir}/{module_name}_subout.json"
    sub_error_path = f"{output_dir}/{module_name}_suberr.json"
    server_subprocess_id = start_server(jar_path, port,
        outputfile=sub_output_path, errorfile=sub_error_path)
    close_server(server_subprocess_id)
    print("Server closed")
    env = initialise_env(
        port=port,
        isa_path=isabelle_dir,
        theory_file_path=os.path.join(working_dir, theory_file_path),
        working_directory=working_dir,
    )
    return server_subprocess_id, env

def get_constant_name(definition):
    # TODO: make sure we can get the name from all definitions
    tokens = definition.split()
    return tokens[1]

def extract_facts_and_defs(env):
    whole_file_string = env.post("PISA extract data")
    env.proceed_to_line('end', 'before')
    env.initialise()
    data = analyse_file_string_with_defs(whole_file_string)
    data["const_defs"] = {get_constant_name(defn): defn for defn in data["def_names"] }
    data["lemma_symbols"] = [(lemma, get_constants_from_theorem_statement(env, lemma)) for lemma in data["problem_names"]]
    return data
            
def extract_file_data_from_params(jar_path, isabelle_dir, output_dir, working_dir, theory_file_path, resume=False):
    module_name = get_module_name(theory_file_path)
    output_path = f"{output_dir}/{module_name}_output.json"
    error_path = f"{output_dir}/{module_name}_error.json"
    os.makedirs(output_dir, exist_ok=True) # create output directory if it doesn't exist
    
    if os.path.isfile(output_path):
        if resume:
            print(f"Found existing output file {output_path}.")
            return
        else:
            os.remove(output_path)
    
    print(f"Extracting data from {theory_file_path}")
    try:
        # Figure out the parameters to start the server
        print("before init_server")
        server_subprocess_id, env = init_server(jar_path, isabelle_dir, output_dir, working_dir, theory_file_path, port=8000)
        print("after init_server")

        # Extract data from input file
        data = extract_facts_and_defs(env)
        print("after extract_facts_and_defs")

        # additional data
        # data["global_facts"] = get_global_facts(env, "default")
        # data["local_facts"] = get_local_facts(env, "default")
        # data["whole_thing"] = whole_file_string
        data["working_dir"] = working_dir
        data["theory_file_path"] = theory_file_path
        data["module_name"] = module_name

        json.dump(data, open(output_path, "w"))
        
    except Exception as e:
        print(e)
        json.dump({"error": str(e)}, open(error_path, "w"))
    finally:
        # Clean up
        del env
        close_server(server_subprocess_id)
        
def extract_file_data_from_args(args, theory_file_path):
    return extract_file_data_from_params(args.jar_path, args.isabelle_dir, args.output_dir, args.working_dir, theory_file_path, args.resume)


if __name__ == '__main__':
    args = parse_args()
    if not args.files:
        args.files = get_theory_files(args.working_dir)

    for theory_file_path in args.files:
        print(f"Extracting data from {theory_file_path}")
        extract_file_data_from_args(args, theory_file_path)