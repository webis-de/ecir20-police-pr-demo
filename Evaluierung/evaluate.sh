#!/bin/bash -e

RUN=${1}

echo "Evaluations on ${RUN} complete-qrels:"
./Evaluierung/trec_eval -m P.1 Evaluierung/qrelall.test results/${RUN}
./Evaluierung/trec_eval -m ndcg_cut.5 Evaluierung/qrelall.test results/${RUN}

echo "Evaluations on ${RUN} level-1-qrels:"
./Evaluierung/trec_eval -m P.1 results/level-1-difficulty-qrel.txt results/level-1-${RUN}.txt
./Evaluierung/trec_eval -m ndcg_cut.5 results/level-1-difficulty-qrel.txt results/level-1-${RUN}.txt

echo "Evaluations on ${RUN} level-2-qrels:"
./Evaluierung/trec_eval -m P.1 results/level-2-difficulty-qrel.txt results/level-2-${RUN}.txt
./Evaluierung/trec_eval -m ndcg_cut.5 results/level-2-difficulty-qrel.txt results/level-2-${RUN}.txt

echo "Evaluations on ${RUN} level-3-qrels:"
./Evaluierung/trec_eval -m P.1 results/level-3-difficulty-qrel.txt results/level-3-${RUN}.txt
./Evaluierung/trec_eval -m ndcg_cut.5 results/level-3-difficulty-qrel.txt results/level-3-${RUN}.txt

