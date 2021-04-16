#!/bin/bash
# ====
# Check that the last changes increment correctly the number of updates to the last release
# in the info.json file
# ====
# Get the last changes folder
latest=$(ls updates| sort -n | tail -n1)
# Count the number of lines in the updates files
lines=$(sed -n '=' updates/$latest/updates.sql | wc -l | cut -d' ' -f1)
# Obtain from the info.json file the number of updates for the last version
expected=$(cat updates/info.json | jq --arg latest "$latest" '.updates[$latest]')
if [ $expected -eq $(expr $lines / 2) ];then
    exit 0
else
    echo "Expected" $expected "changes according to file updates/info.json but got" $(expr $lines / 2) " for version" $latest 
    exit 1
fi