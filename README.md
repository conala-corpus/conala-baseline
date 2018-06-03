# Conala Baseline

This is a baseline for the [Conala Code/Natural Language Challenge](https://conala-corpus.github.io). It makes a system to generate Python from English commands by training a standard neural machine translation model.

It requires a GPU machine, and uses the neural machine translation system [xnmt](https://github.com/neulab/xnmt/), so first install this. Make sure you also install all the packages in the requirements-extra.txt file by running `pip install -r /path/to/xnmt/requirements-extra.txt`.

Also, install the requirements for this package itself by running `pip install -r requirements.txt`.

After you it is installed, you can run

    bash conala-baseline.sh

And it should do the rest for you. Data will be downloaded to and preprocessed in the `conala-corpus/` directory, and output logs and scores will be written into the `results/` directory.
