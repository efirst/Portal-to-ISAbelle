import pisa_client

counter = 0
def clone_top_level_state(env, tls_name):
    global counter
    tls_unique_name = f"{tls_name}_{counter}"
    env.clone_to_new_name(tls_unique_name)
    counter += 1
    return tls_unique_name

def get_global_facts(env, tls_name):
    return env.post(f"<global facts and defs> {tls_name}")

def get_local_facts(env, tls_name):
    return env.post(f"<local facts and defs> {tls_name}")

def get_constants_from_theorem_statement(env, theorem_statement):
    return env.post(f"<get all definitions> {theorem_statement}").split("\n")

def get_fact_definition(env, tls_name, fact_name):
    return env.get_fact_definition(tls_name, fact_name)
  
def get_premises_from_proof(env, proof_string):
  pass
  # for premise, premise_defn in env.get_premises_and_their_definitions("default", "aval_plus", "plus.induct"):
  #   print("~"*80)
  #   print(f"Premise name: {premise}")
  #   print(f"Premise defn: {premise_defn}")
  
def get_module_name(filename):
    if filename.endswith(".thy"):
        return filename.split("/")[-1].split(".")[0]