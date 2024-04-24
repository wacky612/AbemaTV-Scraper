#!/bin/sh

cd gh-pages
git add timetable.json
git commit --amend --no-edit
git -c core.sshCommand="ssh -i ../.ssh/id_ed25519 -F /dev/null" push -f
