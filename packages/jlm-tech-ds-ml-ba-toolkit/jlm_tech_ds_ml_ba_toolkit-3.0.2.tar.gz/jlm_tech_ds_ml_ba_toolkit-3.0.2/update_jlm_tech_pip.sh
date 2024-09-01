#!/bin/bash

# remove current pip dist folder
pip uninstall jlm-tech-ds-ml-ba-toolkit -y

# install current pip dist folder w/o cache
pip install --no-cache-dir jlm-tech-ds-ml-ba-toolkit

# print the version installed.
pip list | grep -i jlm-tech-ds-ml-ba-toolkit

# show the version info of jlm-tech-ds-ml-ba-toolkit
pip show jlm-tech-ds-ml-ba-toolkit
