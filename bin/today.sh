#!/bin/bash
TODO_HOME="$HOME/Documents/notes"
TODAY="$( date "+%Y-%m-%d" )"
TODAY_FILE="$TODO_HOME/todo-$TODAY-todo.txt"
PREVIOUS_FILE="$( ~/bin/previous )"
if [[ ! -f "$TODAY_FILE" ]]; then
  cp "$PREVIOUS_FILE" "$TODAY_FILE"
fi
report "$TODAY_FILE"
printf "Press Enter to Continue, Ctrl-C to exit." && read -r PROMPT
open "$TODAY_FILE"
echo "$TODAY"
