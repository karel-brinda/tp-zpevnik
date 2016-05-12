#! /usr/bin/env bash

find output -type d | while read d; do
    ./make_index_html.py $d > ${d}/index.html
done