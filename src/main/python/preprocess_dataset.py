import argparse
import glob
import json
import os

def partition_dataset(n_splits, dataset):
    n = len(dataset)
    split_size = n // n_splits
    splits = []
    for i in range(n_splits):
        start = i * split_size
        end = (i+1) * split_size
        splits.append(dataset[start:end])
    return splits

def main():
    parser = argparse.ArgumentParser(description='Extracting transition data from theory files.')
    parser.add_argument('--name', default="afp")
    parser.add_argument('--dataset-dir', default="/pisa/afp/thys")
    parser.add_argument('--working-dirs', nargs='*', default=[])
    parser.add_argument('--output-dir', default="/pisa/output")
    parser.add_argument('--output-file', default="all_files.json")
    args = parser.parse_args()

    dataset_dir = args.dataset_dir
    output_dir = args.output_dir
    output_file = f"{args.name}_{args.output_file}"
    if args.working_dirs:
        working_dirs = args.working_dirs
    else:
        working_dirs = [wd for wd in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir,wd))]
    
    dataset = []
    for i, wd in enumerate(working_dirs):
        theory_files = glob.glob(os.path.join(dataset_dir, wd, "**/*.thy"), recursive=True)
        dataset.append({"wd": wd, "tf": theory_files})
        
    json.dump(dataset, open(os.path.join(output_dir, output_file), 'w'))
    
    # TODO:
    # 1. partition dataset into splits, one for each worker
    # 2. generate current.json tracker for each worker

if __name__ == "__main__":
    main()