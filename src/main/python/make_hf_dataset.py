# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import csv
import glob
import json
import os

import datasets
import datasets.data_files

def read_json_file(output_path):
    return json.load(open(output_path))
  
# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
author={huggingface, Inc.
},
year={2020}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
A dataset for lemma exploration in Isabelle. This dataset contains multiple domains (HOL, AFP).
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = ""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
DATA_PATHS = {
    "hol": "/pisa/output/hol",
    "afp": "/pisa/output/afp",
}


# TODO: Name of the dataset usually matches the script name with CamelCase instead of snake_case
class LemExpDataset(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.0.1")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name=name, version=datasets.Version("0.0.1"), description=f"{name} source theory files", data_files=datasets.data_files.DataFilesDict.from_local_or_remote({"train": ["**/*_output.json"]}, path)) for name, path in DATA_PATHS.items()
    ]

    # DEFAULT_CONFIG_NAME = "hol"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "defs": datasets.Value("string"),
                "symbols": datasets.Value("string"),
                "lemma": datasets.Value("string")
                # These are the features of your dataset like images, labels ...
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        name = self.config.name
        files = self.config.data_files
        
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": files,
                    "split": "train",
                },
            )
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepaths, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        key = 0
        for split in filepaths:
            for filepath in filepaths[split]:
                raw_data = read_json_file(filepath)
                assert "lemma_symbols" in raw_data
                for lemma, symbols in raw_data["lemma_symbols"]:
                    yield key, {
                        "defs": raw_data["def_names"],
                        "symbols": symbols,
                        "lemma": lemma,
                    }
                    key += 1

if __name__ == "__main__":
    for name in DATA_PATHS:
        dataset = datasets.load_dataset("/home/ubuntu/lemma-exploration/Portal-to-ISAbelle/src/main/python/make_hf_dataset.py", name)
        
        # push to huggingface hub
        # datasets.push_to_hub(dataset, name)