#!/bin/sh

cd gh-pages
git add timetable.json
git commit --amend --no-edit
git push -f
