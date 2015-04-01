#!/bin/bash
LIMIT=$1;
P=$PWD;
#echo "Moving $LIMIT steps above"
for ((i=1; i <= LIMIT; i++))
do
    echo $i
    P=$P/..
done;
echo $P;
cd $P;

