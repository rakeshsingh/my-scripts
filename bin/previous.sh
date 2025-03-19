#!/bin/bash
TODO_HOME="$HOME/Documents/notes"
TODAYS_DATE="$( date "+%Y-%m-%d" )"
MOST_RECENT="$( ls "$TODO_HOME"/todo-*-todo.txt | sed 's/^.*todo-//g' | sed 's/-todo.txt//g' ; echo "$TODAYS_DATE" | sort )"
PREVIOUS="$( echo "$MOST_RECENT" | awk -- "BEGIN { YET=0 } /^$TODAYS_DATE/ { YET=1 } { if ( !YET ) PREV=\$0 } END { print( PREV ) }" )"
PREVIOUS_FILE="$( echo "$TODO_HOME/todo-$PREVIOUS-todo.txt" )"
echo "$( realpath "$PREVIOUS_FILE" )
