# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

import json
import sys
import nltk
import traceback

from canonicalize import *
from util import get_encoded_code_tokens, detokenize_code, encode_tokenized_code, encoded_code_tokens_to_code, tokenize, compare_ast

if __name__ == '__main__':
    for file_path, file_type in [('conala-train.json', 'annotated'), ('conala-test.json', 'annotated'), ('conala-mined.jsonl', 'mined')]:
        print('extracting {} file {}'.format(file_type, file_path), file=sys.stderr)

        if file_type == 'annotated':
            dataset = json.load(open(file_path))
        elif file_type == 'mined':
            dataset = []
            with open(file_path, 'r') as f:
                for line in f:
                    dataset.append(json.loads(line.strip()))

        for i, example in enumerate(dataset):
            intent = example['intent']
            if file_type == 'annotated':
              rewritten_intent = example['rewritten_intent']
            elif file_type == 'mined':
              rewritten_intent = example['intent']
            snippet = example['snippet']
            # print(i)
            # code_tokens = get_encoded_code_tokens(snippet)
            # print(' '.join(code_tokens))

            failed = False
            intent_tokens = []
            if rewritten_intent:
                try:
                    canonical_intent, slot_map = canonicalize_intent(rewritten_intent)
                    snippet = snippet
                    canonical_snippet = canonicalize_code(snippet, slot_map)
                    intent_tokens = nltk.word_tokenize(canonical_intent)
                    decanonical_snippet = decanonicalize_code(canonical_snippet, slot_map)

                    snippet_reconstr = astor.to_source(ast.parse(snippet)).strip()
                    decanonical_snippet_reconstr = astor.to_source(ast.parse(decanonical_snippet)).strip()
                    encoded_reconstr_code = get_encoded_code_tokens(decanonical_snippet_reconstr)
                    decoded_reconstr_code = encoded_code_tokens_to_code(encoded_reconstr_code)

                    if not compare_ast(ast.parse(decoded_reconstr_code), ast.parse(snippet)):
                        print(i)
                        print('Original Snippet: %s' % snippet_reconstr)
                        print('Tokenized Snippet: %s' % ' '.join(encoded_reconstr_code))
                        print('decoded_reconstr_code: %s' % decoded_reconstr_code)

                except:
                    print('*' * 20, file=sys.stderr)
                    print(i, file=sys.stderr)
                    print(intent, file=sys.stderr)
                    print(snippet, file=sys.stderr)
                    traceback.print_exc()

                    failed = True
                finally:
                    example['slot_map'] = slot_map

            if rewritten_intent is None:
                encoded_reconstr_code = get_encoded_code_tokens(snippet.strip())
            else:
                encoded_reconstr_code = get_encoded_code_tokens(canonical_snippet.strip())

            if not intent_tokens:
                intent_tokens = nltk.word_tokenize(intent)

            example['intent_tokens'] = intent_tokens
            example['snippet_tokens'] = encoded_reconstr_code

        json.dump(dataset, open(file_path + '.seq2seq', 'w'), indent=2)
