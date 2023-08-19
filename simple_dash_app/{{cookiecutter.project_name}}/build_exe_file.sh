#!/bin/bash
ENV_NAME='venv' ## name of virtual environment. If different, change
cd $ENV_NAME/Scripts
PWD=`pwd`
echo $PWD
sed -i 's/\r$//' activate ## change windows file to unix file
cd ../../
CUR_DIR=`pwd`
source $PWD/$ENV_NAME/Scripts/activate
python setup_exe.py build_exe