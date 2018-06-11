#!/usr/bin/env python
import json
import sys
import os
import os.path
import re
from StringIO import StringIO
import token
import tokenize

import bleu_score

# Main function for CodaLab evaluation purposes
def main():

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    submit_dir = os.path.join(input_dir, 'res')
    truth_dir = os.path.join(input_dir, 'ref')

    if not os.path.isdir(submit_dir):
        print "%s doesn't exist" % submit_dir

    if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_filename = os.path.join(output_dir, 'scores.txt')
        output_file = open(output_filename, 'wb')

        truth_file = os.path.join(truth_dir, "truth.txt")
        f_reference = open(truth_file)

        submission_answer_file = os.path.join(submit_dir, "answer.txt")
        f_submission = open(submission_answer_file)

        a = parse_file_list(f_reference)
        b = parse_file_list(f_submission)
        b = [tokenize_for_bleu_eval(s) for s in b]

        bleu = bleu_score.compute_bleu(a, b, smooth=True)[0]

        output_file.write('bleu:{0:.2f}\n'.format(bleu * 100))

        output_file.close()

""" Parses a file in the natural .jsonl format that the Conala corpus comes in.
    @param f: .jsonl file containing snippets
    @return: list of lists of tokens
"""
def parse_file_json(f):
    snippet_list = json.load(f)
    result = []
    for snippet in snippet_list:
        toks = tokenize_code(snippet['snippet'])
        result.append(toks)
    return result

def parse_file_list(f):
    return json.load(f)

""" The tokenizer that we use for code submissions, from Wang Ling et al., Latent Predictor Networks for Code Generation (2016)
    @param code: string containing a code snippet
    @return: list of code tokens
"""
def tokenize_for_bleu_eval(code):
    code = re.sub(r'([^A-Za-z0-9_])', r' \1 ', code)
    code = re.sub(r'([a-z])([A-Z])', r'\1 \2', code)
    code = re.sub(r'\s+', ' ', code)
    code = code.replace('"', '`')
    code = code.replace('\'', '`')
    tokens = [t for t in code.split(' ') if t]

    return tokens

""" This runs the built-in Python tokenizer. Note that it only works on correctly parseable Python programs.
    @param string: string containing a Python tokenizable code snippet
    @return: list of code tokens
"""
def tokenize_code(string, concat_symbol=None):
    tokens = []
    string = string.strip().decode('utf-8').encode('ascii', 'strict') #.decode('string_escape')
    for toknum, tokval, _, _, _  in tokenize.generate_tokens(StringIO(string).readline):
        # We ignore these tokens during evaluation.
        if toknum not in [token.ENDMARKER, token.INDENT, token.DEDENT]:
            tokens.append(tokval.lower())

    return tokens

""" This builds the reference list for BLEU scoring
    @param reference_file_name: The reference file can be downloaded from https://conala-corpus.github.io/ as
                                conala_annotations.v1.0.zip/examples.annotated.test.json
    @return: list of references ready for BLEU scoring
"""
# 
def get_reference_list(reference_file_name):
    f_reference = open(reference_file_name)
    a = parse_file_json(f_reference)
    a = [[l] for l in a]
    return a

""" This scores hypotheses against references using BLEU.
    @param reference_list: reference list returned by get_reference_list.
    @param hypothesis_list: list of lists of tokens that a model generates.
    @return: 3-Tuple with the BLEU score, n-gram precisions, geometric mean of n-gram
             precisions and brevity penalty.
"""
def evaluate_bleu(reference_list, hypothesis_list):
    b = [tokenize_for_bleu_eval(s) for s in hypothesis_list]
    return bleu_score.compute_bleu(reference_list, b, smooth=True)

if __name__ == '__main__':
    main()
