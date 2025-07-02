linux_dev() {
  local action="$1"
  shift
  bash <(curl -fsSL https://raw.githubusercontent.com/nicolascochin/distrobox/main/$action) "$@"
}

list_distroboxes() {
  ls -1 $HOME/Distroboxes | tr -d ' ' | sort -u
}

_comp_distros() {
  compadd $(list_distroboxes)
}

dev_create() {
  local name="$1"
  shift

  if [[ -z "$name" ]]; then
    echo "Error: No name was given"
    return 1
  fi

  case $(uname -s) in
   Linux)
      linux_dev create --name $name --image debian:latest --package figlet --package fuse --docker
      ;;
    Darwin)
      lima -- zsh -lic "linux_dev create --name $name --image debian:latest --package figlet --package fuse --docker --host_home /Users/$(whoami)"
;;
  esac
}

dev_enter() {
  local name="$1"
  shift

  if [[ -z "$name" ]]; then
    echo "Error: No name was given"
    exit 1
  fi
  case $(uname -s) in
    Darwin)
      lima -- zsh -lic "linux_dev enter $name --root"
      ;;
    Linux)
      linux_dev enter $name --root
      ;;
  esac
}
compdef _comp_distros dev_enter

dev_delete() {
  local name="$1"
  shift

  if [[ -z "$name" ]]; then
    echo "Error: No name was given"
    exit 1
  fi
  case $(uname -s) in
    Darwin)
      lima -- zsh -lic "linux_dev delete $name --root"
      ;;
    Linux)
      linux_dev delete $name --root
      ;;
  esac
}
compdef _comp_distros dev_delete
