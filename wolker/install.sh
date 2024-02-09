#!/bin/bash

for d in genouts genimgs qrcodes
do
    mkdir $d
    chmod a+rwx $d
done

