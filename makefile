JAR_PATH = /pisa/target/scala-2.13/pisa_2.13-0.1.jar
ISABELLE_DIR = /pisa/Isabelle2022
OUTPUT_DIR = /pisa/output

DATASET = hol
DATASET_DIR = /pisa/Isabelle2022/src/HOL

# DATASET = afp
# DATASET_DIR = /pisa/afp/thys

preprocess:
	python3 src/main/python/preprocess_dataset.py --name $(DATASET) --dataset-dir $(DATASET_DIR)

extract:
	bash scripts/parse_loop.sh

clean-processes:
	bash scripts/clean_processes.sh

clean-data:
	rm -rf $(OUTPUT_DIR)