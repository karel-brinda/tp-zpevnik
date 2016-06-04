#! /usr/bin/env bash

set -e -o pipefail

for zpevnik in Snakefile.*; do
	snakemake -p -s $zpevnik --cores &
done
wait

