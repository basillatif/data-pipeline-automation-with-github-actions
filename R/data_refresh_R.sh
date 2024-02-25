#!/usr/bin/env bash
source /opt/$VENV_NAME/bin/activate 

rm -rf ./R/data_refresh_R_files
rm ./R/data_refresh_R.html
quarto render ./R/data_refresh_R.qmd --to html

rm -rf docs/data_refresh_R/
mkdir docs/data_refresh_R
cp ./R/data_refresh_R.html ./docs/data_refresh_R/
cp -R ./R/data_refresh_R_files ./docs/data_refresh_R/

echo "Finish"

p=$(pwd)
git config --global --add safe.directory $p

echo "Finish"
p=$(pwd)
git config --global --add safe.directory $p

if [[ "$(git status --porcelain)" != "" ]]; then
    quarto render dashboard_R/index.qmd
    git config --global user.name 'RamiKrispin'
    git config --global user.email 'ramkrisp@umich.edu'
    git add csv/*
    git add metadata/*
    git add docs/*
    git commit -m "Auto update of the data"
    git push origin stg
else
echo "Nothing to commit..."
fi