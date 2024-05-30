#! /bin/bash

## The "data" folder keeps all input and output data.
## This script deletes the data folder, creates a new empty 
## data folder, and creates sym links to input data.
## This way, the user can clean all processed data, and 
## reproduce all results from initial data.

echo "WARNING: This command will delete all files inside the data folder!!!"
read -p "Do you want to proceed (yes/no)? " user_answer
if [ "${user_answer}" == 'yes' ]; then
    echo "Deleting the data folder ..."
    rm -rf ../data
    echo "Creating empty data folder ..."
    mkdir -p ../data
    echo "Copying input to data folder ..."
    for ll in $(ls -1 ../input); do
        cp -r ../input/${ll} ../data
    done
    echo "Clean data folder created with links to input data!"
    echo "You can now run Snakemake to reproduce the results!"
else
    echo "Operation canceled, bye ..."
fi


