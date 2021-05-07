#!/bin/bash -e

RUN_DIR=results
ORIGINAL_RUN_FILES=(runBlaulichtTitleSearch runcomplex_query runtitle_query runfull_text_query runBlaulichtFullTextSearch)
ORIGINAL_QRELS=Evaluierung/qrelall.test

echo "level 1 difficulty"
cat Evaluierung/qrelall.test  |grep -E '1_1 0|1_2 0|1_4 0|1_5 0|1_9 0|1_10 0|1_12 0|2_2 0|2_3 0|2_4 0|2_5 0|2_6 0|2_9 0|2_10 0|2_11 0|2_13 0|3_2 0|3_3 0|3_5 0|3_15 0|4_6 0|4_14 0|5_3 0|5_6 0|5_14 0|6_3 0|6_4 0|7_2 0|7_7 0' > ${RUN_DIR}/level-1-difficulty-qrel.txt

echo "level 2 difficulty"
cat Evaluierung/qrelall.test  |grep -E '1_3 0|1_6 0|1_8 0|1_11 0|1_13 0|1_15 0|2_1 0|2_8 0|2_12 0|2_14 0|3_1 0|3_4 0|3_6 0|3_7 0|3_8 0|3_11 0|3_12 0|3_13 0|3_14 0|4_1 0|4_2 0|4_3 0|4_4 0|4_5 0|4_7 0|4_8 0|4_11 0|4_15 0|5_1 0|5_2 0|5_5 0|5_8 0|5_9 0|5_10 0|5_11 0|5_12 0|5_15 0|6_2 0|6_5 0|6_6 0|6_7 0|6_8 0|6_9 0|6_10 0|6_11 0|6_12 0|6_13 0|6_14 0|6_15 0|7_1 0|7_3 0|7_4 0|7_5 0|7_6 0|7_8 0|7_9 0|7_10 0|7_11 0|7_12 0|7_13 0|7_14 0|7_15 0' > ${RUN_DIR}/level-2-difficulty-qrel.txt

echo "level 3 difficulty"
cat Evaluierung/qrelall.test  |grep -E '1_7 0|1_14 0|2_7 0|2_15 0|3_9 0|3_10 0|4_9 0|4_10 0|4_12 0|4_13 0|5_4 0|5_7 0|5_13 0|6_1 0|8_1 0'  > ${RUN_DIR}/level-3-difficulty-qrel.txt

for RUN_FILE in ${ORIGINAL_RUN_FILES[@]}
do
	TARGET_RUN_FILE=${RUN_FILE}
	RUN_FILE="${RUN_DIR}/${RUN_FILE}"
	echo "level 1 difficulty for ${RUN_FILE}" 
	cat ${RUN_FILE}  |grep -E '1_1 Q0|1_2 Q0|1_4 Q0|1_5 Q0|1_9 Q0|1_10 Q0|1_12 Q0|2_2 Q0|2_3 Q0|2_4 Q0|2_5 Q0|2_6 Q0|2_9 Q0|2_10 Q0|2_11 Q0|2_13 Q0|3_2 Q0|3_3 Q0|3_5 Q0|3_15 Q0|4_6 Q0|4_14 Q0|5_3 Q0|5_6 Q0|5_14 Q0|6_3 Q0|6_4 Q0|7_2 Q0|7_7 Q0' > ${RUN_DIR}/level-1-${TARGET_RUN_FILE}.txt

	echo "level 2 difficulty for ${RUN_FILE}"
	cat ${RUN_FILE} |grep -E '1_3 Q0|1_6 Q0|1_8 Q0|1_11 Q0|1_13 Q0|1_15 Q0|2_1 Q0|2_8 Q0|2_12 Q0|2_14 Q0|3_1 Q0|3_4 Q0|3_6 Q0|3_7 Q0|3_8 Q0|3_11 Q0|3_12 Q0|3_13 Q0|3_14 Q0|4_1 Q0|4_2 Q0|4_3 Q0|4_4 Q0|4_5 Q0|4_7 Q0|4_8 Q0|4_11 Q0|4_15 Q0|5_1 Q0|5_2 Q0|5_5 Q0|5_8 Q0|5_9 Q0|5_10 Q0|5_11 Q0|5_12 Q0|5_15 Q0|6_2 Q0|6_5 Q0|6_6 Q0|6_7 Q0|6_8 Q0|6_9 Q0|6_10 Q0|6_11 Q0|6_12 Q0|6_13 Q0|6_14 Q0|6_15 Q0|7_1 Q0|7_3 Q0|7_4 Q0|7_5 Q0|7_6 Q0|7_8 Q0|7_9 Q0|7_10 Q0|7_11 Q0|7_12 Q0|7_13 Q0|7_14 Q0|7_15 Q0' > ${RUN_DIR}/level-2-${TARGET_RUN_FILE}.txt

	echo "level 3 difficulty for ${RUN_FILE}"
	cat ${RUN_FILE} |grep -E '1_7 Q0|1_14 Q0|2_7 Q0|2_15 Q0|3_9 Q0|3_10 Q0|4_9 Q0|4_10 Q0|4_12 Q0|4_13 Q0|5_4 Q0|5_7 Q0|5_13 Q0|6_1 Q0|8_1 Q0'  > ${RUN_DIR}/level-3-${TARGET_RUN_FILE}.txt

done
