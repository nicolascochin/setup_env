#!/usr/bin/env bash

USER=""
INSTALL_SHELL=false
INSTALL_DOCKER=false
INSTALL_HEROKU=false

while getopts "u:hsdk" opt; do
  case $opt in
    s)
        INSTALL_SHELL=true 
        ;;
    u) 
        USER="$OPTARG"
        ;;        
    d) 
        INSTALL_DOCKER=true
        ;;
    k) 
        INSTALL_HEROKU=true
        ;;
    h) 
        echo "Usage $0 [options]" 
        echo 
        echo "Options"
        echo "  -s          Install dependencies required by the Shell (script init_env)"
        echo "  -u [user]   Target user"
        echo "  -d          Install Docker"
        echo "  -k          Install Heroku cli"
        echo "  -h          Display the usage"
        ;;
  esac
done

if $INSTALL_SHELL; then 
  if [ -z $USER ]; then 
    echo "Option user is mandatory"
    exit 1
  fi
  sudo apt update -y
  echo "===== Install Shell dependencies ====="
  sudo apt install -y  \
      git              \
      zsh              \
      python3-pygments \
      most
  sudo usermod --shell /bin/zsh ${USER}
  echo "=========="
fi

if $INSTALL_HEROKU; then 
  curl https://cli-assets.heroku.com/install.sh | sh
fi

if $INSTALL_DOCKER; then 
  # Docker
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo apt-key fingerprint 0EBFCD88
  sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
  sudo apt update
  sudo apt install -y          \
    apt-transport-https        \
    ca-certificates            \
    build-essential            \
    curl                       \
    gnupg-agent                \
    software-properties-common \
    docker-ce                  \
    containerd.io
  sudo usermod -aG docker ${USER}
  # Docker-compose
  sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo ln -fs /usr/local/bin/docker-compose /usr/bin/docker-compose
fi 
echo "OK"