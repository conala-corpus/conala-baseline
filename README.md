# CoNaLa Preprocessing Scripts/Baseline

This repository contains preprocessing scripts and a baseline for the [CoNaLa Code/Natural Language Challenge](https://conala-corpus.github.io).

## CoNaLa Preprocessing Scripts

In the `preproc` directory, there are a number of preprocessing/evaluation scripts that you can use to extract the data and convert it into a format that is easy to use for training models. The best way to see their usage is to take a look at the CoNaLa baseline below, but we'll first briefly describe them here.

* `process_raw_data.py`: perform some tokenization on the source code, etc.
* `json_to_seq2seq.py`: convert the json file resulting from `extract_data.py` to source/target files used by seq2seq models
* `seq2seq_output_to_code.py`: take a decode file outputted by the seq2seq model, and "detokenize" it to the original source code for evaluation

## CoNaLa Baseline

The baseline makes a system to generate Python from English commands by training a standard neural machine translation model.

It requires a GPU machine, and uses the neural machine translation system [xnmt](https://github.com/neulab/xnmt/) (specifically, commit `d9e227b`), so first install this. Make sure you also install all the packages in the requirements-extra.txt file by running `pip install -r /path/to/xnmt/requirements-extra.txt`.

Also, install the requirements for this package itself by running `pip install -r requirements.txt`.

After you it is installed, you can run

    bash conala_baseline.sh

And it should do the rest for you. Data will be downloaded to and preprocessed in the `conala-corpus/` directory, and output logs and scores will be written into the `results/` directory.
