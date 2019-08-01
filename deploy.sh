# !bin/bash

# ctrl-c exit
trap 'exit 1'  1 2 3 15

msg="committed `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git add .
git commit -m "$msg"
git push origin master
