#!/bin/bash

files=$(find . -name '*.txt')

for file in $files; do
    full_filename=$(basename $file)
    third_line=$(sed -n '3p' $file)
    prefix=${full_filename::-4}
    grepping=$(grep -w -e $prefix $file | wc -l)

    echo $file" : "$third_line" | "$grepping
    # length=${#full_filename}
    # prefix_filename=${full_filename:-4}

    # greppin=$(grep -e $filename $file)
done
