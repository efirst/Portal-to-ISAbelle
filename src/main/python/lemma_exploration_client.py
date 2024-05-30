import json
import os
from pisa_client import initialise_env
from data_extraction.extract_data import extract_test_file_from_params, analyse_file_string_with_defs
from utils.pisa_server_control import start_server, close_server
from lemma_exploration_utils import get_global_facts, get_local_facts, get_constants_from_theorem_statement

def init_server(jar_path, isabelle_path, theory_file_path, working_directory, sub_saving_path, sub_error_path, resume=False):
    port = 8000
    server_subprocess_id = start_server(jar_path, port,
        outputfile=sub_saving_path, errorfile=sub_error_path)
    env = initialise_env(
        port=port,
        isa_path=isabelle_path,
        theory_file_path=theory_file_path,
        working_directory=working_directory,
    )
    return server_subprocess_id, env

def init_client(jar_path, isabelle_path, theory_file_path, working_directory, saving_path, error_path, sub_saving_path, sub_error_path, resume=False):
    if os.path.isfile(saving_path):
        if resume: return
        # clean old directory
        os.remove(saving_path)
    try:
        # Figure out the parameters to start the server
        server_subprocess_id, env = init_server(jar_path, isabelle_path, theory_file_path, working_directory, sub_saving_path, sub_error_path, resume)

        # Extract data from input file
        whole_file_string = env.post("PISA extract data")
        env.proceed_to_line('end', 'before')
        env.initialise()

        # Parse data
        analysed_file = analyse_file_string_with_defs(whole_file_string)
        # analysed_file["global_facts"] = get_global_facts(env, "default")
        analysed_file["local_facts"] = get_local_facts(env, "default")
        # analysed_file["whole_thing"] = whole_file_string
        # analysed_file["theory_file_path"] = theory_file_path
        # analysed_file["working_directory"] = working_directory

        theorem_string = "lemma [simp]: \"bval (less a1 a2) s = (aval a1 s < aval a2 s)\""
        analysed_file["all_defs"] = get_constants_from_theorem_statement(env, theorem_string)

        json.dump(analysed_file, open(saving_path, "w"))
        
    except Exception as e:
        raise(e)
        print(e)
        json.dump({"error": str(e)}, open(error_path, "w"))
    finally:
        # Clean up
        del env
        close_server(server_subprocess_id)

if __name__ == '__main__':
    jar_path = "/pisa/target/scala-2.13/pisa_2.13-0.1.jar"
    isabelle_path = "/pisa/Isabelle2022"
    theory_file_path = "/pisa/Isabelle2022/src/HOL/IMP/BExp.thy"
    working_directory = "/pisa/Isabelle2022/src/HOL/IMP"
    output_data_path = "/pisa/extracted"
    identifier = "testing"
    saving_path = f"{output_data_path}/{identifier}_output.json"
    error_path = f"{output_data_path}/{identifier}_error.json"
    sub_saving_path = f"{output_data_path}/{identifier}_subout.json"
    sub_error_path = f"{output_data_path}/{identifier}_suberr.json"
    resume = False

    init_client(jar_path, isabelle_path, theory_file_path, working_directory, saving_path, error_path, sub_saving_path, sub_error_path, resume)
