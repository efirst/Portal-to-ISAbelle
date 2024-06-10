import json
import os
from pisa_client import initialise_env
from data_extraction.extract_data import extract_test_file_from_params, analyse_file_string_with_defs
from utils.pisa_server_control import start_server, close_server

counter = 0

def clone_top_level_state(env, tls_name):
    global counter
    tls_unique_name = f"{tls_name}_{counter}"
    env.clone_to_new_name(tls_unique_name)
    counter += 1
    return tls_unique_name

def get_definitions_from_theorem_statement(env, theorem_string):
    return env.post(f"<get all definitions> {theorem_string}")    

def get_premises_and_their_definitions(env, proof_string):
    for premise, premise_defn in env.get_premises_and_their_definitions("default", "aval_plus", "plus.induct"):
        print("~"*80)
        print(f"Premise name: {premise}")
        print(f"Premise defn: {premise_defn}")

def test():
    global counter
    output_data_path = "/pisa/extracted"
    identifier = "testing"
    
    jar_path = "/pisa/target/scala-2.13/pisa_2.13-0.1.jar"
    isabelle_path = "/isabelle"
    working_directory = "/isabelle/src/HOL/IMP"
    theory_file_path = "/isabelle/src/HOL/IMP/BExp.thy"
    saving_path = f"{output_data_path}/{identifier}_output.json"
    error_path = f"{output_data_path}/{identifier}_error.json"
    sub_saving_path = f"{output_data_path}/{identifier}_subout.json"
    sub_error_path = f"{output_data_path}/{identifier}_suberr.json"

    env = None
    resume = False

    if os.path.isfile(saving_path):
        if resume:
            return
        # delete the file
        os.remove(saving_path)
    try:
        # Figure out the parameters to start the server
        rank = 0
        port = 8000 + rank
        server_subprocess_id = start_server(jar_path, port, 
            outputfile=sub_saving_path, errorfile=sub_error_path)
        # Getting the environment
        env = initialise_env(
            port=port,
            isa_path=isabelle_path,
            theory_file_path=theory_file_path,
            working_directory=working_directory,
        )
        whole_file_string = env.post("PISA extract data")
        # Parse the string and dump
        analysed_file = analyse_file_string_with_defs(whole_file_string)
        # analysed_file = {}
        analysed_file["whole_thing"] = whole_file_string
        analysed_file["theory_file_path"] = theory_file_path
        analysed_file["working_directory"] = working_directory

        env.proceed_to_line('end', 'before')
        env.initialise()
        theorem_string = "lemma [simp]: \"bval (less a1 a2) s = (aval a1 s < aval a2 s)\""
        analysed_file["all_defs"] = get_definitions_from_theorem_statement(env, theorem_string)

        json.dump(analysed_file, open(saving_path, "w"))
        
    except Exception as e:
        print(e)
        json.dump({"error": str(e)}, open(error_path, "w"))

    # for premise, premise_defn in env.get_premises_and_their_definitions("default", "aval_plus", "plus.induct"):
    #     print("~"*80)
    #     print(f"Premise name: {premise}")
    #     print(f"Premise defn: {premise_defn}")

    # Clean up
    del env
    close_server(server_subprocess_id)
    counter += 1


if __name__ == '__main__':
    # env = initialise_env(
    #     8000, 
    #     "/isabelle", 
    #     "/isabelle/src/HOL/Computational_Algebra/Primes.thy",
    #     "/isabelle/src/HOL/Computational_Algebra"
    # )
    # env = initialise_env(
    #     8000, 
    #     "/home/ubuntu/Isabelle2022", 
    #     "/home/ubuntu/Isabelle2022/src/HOL/Cardinals/Cardinal_Arithmetic.thy",
    #     "/home/ubuntu/Isabelle2022/src/HOL/Cardinals"
    # )

    # env = initialise_env(
    #     8000, 
    #     "/home/ubuntu/Isabelle2022", 
    #     "/home/ubuntu/Isabelle2022/src/HOL/Cardinals/Ordinal_Arithmetic.thy",
    #     "/home/ubuntu/Isabelle2022/src/HOL/Cardinals"
    # )

    # Cardinals/Cardinal_Arithmetic.thy
    # csum_Cnotzero2
    # env.proceed_to_line('end', 'before')
    # env.initialise()
    
    # for premise, premise_defn in env.get_premises_and_their_definitions("default", "prime_int_naive", "by (auto simp add: prime_int_iff')"):
    #     print("~"*80)
    #     print(f"Premise name: {premise}")
    #     print(f"Premise defn: {premise_defn}")

    # for premise, premise_defn in env.get_premises_and_their_definitions("default", "cone_Cnotzero", "by (simp add: cone_not_czero Card_order_cone)"):
    #     print("~"*80)
    #     print(f"Premise name: {premise}")
    #     print(f"Premise defn: {premise_defn}")

    output_data_path = "/home/ubuntu/Portal-to-ISAbelle/extracted"
    identifier = "Signature_Groebner"

    jar_path = "/home/ubuntu/Portal-to-ISAbelle/target/scala-2.13/pisa_2.13-0.1.jar"
    isabelle_path = "/home/ubuntu/Isabelle2022"
    # working_directory = "/home/ubuntu/Isabelle2022/src/HOL/IMP"
    # theory_file_path = "/home/ubuntu/Isabelle2022/src/HOL/IMP/AExp.thy"
    working_directory = "/home/ubuntu/afp-2022-12-06/thys/Signature_Groebner"
    theory_file_path = "/home/ubuntu/afp-2022-12-06/thys/Signature_Groebner/Signature_Groebner.thy"
    saving_path = f"{output_data_path}/{identifier}_output.json"
    error_path = f"{output_data_path}/{identifier}_error.json"
    sub_saving_path = f"{output_data_path}/{identifier}_subout.json"
    sub_error_path = f"{output_data_path}/{identifier}_suberr.json"

    extract_test_file_from_params(
        jar_path, 
        isabelle_path, 
        working_directory, 
        theory_file_path,
        saving_path, 
        error_path,
        sub_saving_path,
        sub_error_path
    )
    # test()
