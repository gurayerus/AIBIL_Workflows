#!/usr/bin/env bash
#
#$ -t 1-20
#$ -tc 20
#$ -o ./logs/$JOB_NAME-$JOB_ID.log

echo "Task id is $SGE_TASK_ID"

sh run_model.sh $SGE_TASK_ID
