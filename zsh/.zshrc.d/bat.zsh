if cmd_exists bat
then
  export MANPAGER="sh -c 'col -bx | bat -l man -p'"
  export FORGIT_PAGER=bat

  function help() {
    "$@" --help 2>&1 | bat --plain --language=help
  }
#  unalias help

  export BAT_THEME=Dracula
fi

if cmd_exists batdiff
then
  unalias gd
  # Pretty git diff
  function gd() {
    git status -s \
      | fzf --no-sort --reverse \
      --preview 'batdiff --color --delta {+2}' \
      --bind=ctrl-j:preview-down --bind=ctrl-k:preview-up \
      --preview-window=right:60%:wrap
    }
fi
