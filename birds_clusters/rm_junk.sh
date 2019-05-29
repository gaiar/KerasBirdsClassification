#!/bin/bash

for i in Junk/*
do
rm  "$(readlink -f $i)"
rm "$i"
done

