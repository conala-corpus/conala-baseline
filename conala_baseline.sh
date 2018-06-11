#!/bin/bash
set -e

SDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WDIR=`pwd`

# Get the data
wget http://www.phontron.com/download/conala-corpus-v1.0.zip
unzip conala-corpus-v1.0.zip

# Extract data 
cd $WDIR/conala-corpus

python $SDIR/preproc/extract_raw_data.py

python $SDIR/preproc/json_to_seq2seq.py conala-train.json.seq2seq conala-train.intent conala-train.snippet
python $SDIR/preproc/json_to_seq2seq.py conala-test.json.seq2seq conala-test.intent conala-test.snippet
python $SDIR/preproc/json_to_seq2seq.py conala-mined.jsonl.seq2seq conala-mined.intent conala-mined.snippet

# Split off a 400-line dev set from the training set
# Also, concatenate the first 100000 lines of mined data
for f in intent snippet; do
  head -n 400 < conala-train.$f > conala-dev.$f
  tail -n +401 < conala-train.$f > conala-trainnodev.$f
  cat conala-trainnodev.$f <(head -n 100000 conala-mined.$f) > conala-trainnodev+mined.$f
done

cd $WDIR

# Train and package seq2seq models on annotated+mined and annotated only data
for setting in annotmined annot; do

  # Train and test a seq2seq model
  xnmt --dynet-gpu $SDIR/$setting.yaml
  
  # Package the output in the appropriate way
  python $SDIR/preproc/seq2seq_output_to_code.py results/$setting.test.hyp conala-corpus/conala-test.json.seq2seq results/$setting.test.json

  # Calculate the BLEU score
  python $SDIR/eval/conala_eval.py --strip_ref_metadata --input_ref conala-corpus/conala-test.json --input_hyp results/$setting.test.json
  
  # Package the output for CodaLab
  cd $WDIR/results
  cp $setting.test.json answer.txt
  zip $setting.zip answer.txt

  cd $WDIR

done

# annotmined.zip and annot.zip can be submitted to the CodaLab leaderboard:
# 
