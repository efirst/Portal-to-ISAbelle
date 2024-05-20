from pisa_client import initialise_env
from data_extraction.extract_data import extract_test_file_from_params


if __name__ == '__main__':
    # env = initialise_env(
    #     8000, 
    #     "/pisa/Isabelle2022", 
    #     "/pisa/Isabelle2022/src/HOL/Computational_Algebra/Primes.thy",
    #     "/pisa/Isabelle2022/src/HOL/Computational_Algebra"
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

    # extract_a_file_from_params(
    output_data_path = "/home/ubuntu/Portal-to-ISAbelle/extracted"
    identifier = "testing"
    
    jar_path = "/home/ubuntu/Portal-to-ISAbelle/target/scala-2.13/pisa_2.13-0.1.jar"
    isabelle_path = "/home/ubuntu/Isabelle2022"
    working_directory = "/home/ubuntu/Isabelle2022/src/HOL/Cardinals"
    theory_file_path = "/home/ubuntu/Isabelle2022/src/HOL/Cardinals/Ordinal_Arithmetic.thy"
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
        sub_error_path,
    )




