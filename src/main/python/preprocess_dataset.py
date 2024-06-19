import argparse
import glob
import json
import os

TRACKER_INIT = (0, 0) # (project_index, file_index)

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
    parser.add_argument('--name', '--dataset-name', default="afp")
    parser.add_argument('--dataset-dir', default="/pisa/afp/thys")
    parser.add_argument('--working-dirs', nargs='*', default=[])
    parser.add_argument('--output-dir', default="/pisa/output")
    parser.add_argument('--job-file', default="all_files.json")
    parser.add_argument('--tracker-file', default="current.json")
    parser.add_argument('--n-splits', type=int, default=1)
    args = parser.parse_args()

    dataset_dir = args.dataset_dir
    output_dir = os.path.join(args.output_dir, args.name)
    os.makedirs(output_dir, exist_ok=True) # create output directory if it doesn't exist

    job_file = args.job_file
    tracker_file = args.tracker_file
    if args.working_dirs:
        working_dirs = args.working_dirs
    else:
        working_dirs = [wd for wd in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir,wd))]
    
    dataset = []
    for i, wd in enumerate(working_dirs):
        full_working_dir = os.path.join(dataset_dir, wd)
        theory_files = glob.glob(os.path.join(dataset_dir, wd, "**/*.thy"), recursive=True)
        dataset.append({"wd": full_working_dir, "tf": theory_files})
        
    json.dump(dataset, open(os.path.join(output_dir, job_file), 'w'))
    json.dump(TRACKER_INIT, open(os.path.join(output_dir, tracker_file), 'w'))
    
    if args.n_splits > 1:
        splits = partition_dataset(args.n_splits, dataset)
        for i, split in enumerate(splits):
            split_file = f"split_{i}.json"
            json.dump(split, open(os.path.join(output_dir, split_file), 'w'))
            json.dump(TRACKER_INIT, open(os.path.join(output_dir, f"split_{i}_{args.tracker_file}"), 'w'))
    
    # TODO:
    # 2. generate current.json tracker for each worker

if __name__ == "__main__":
    main()