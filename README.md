# setup_env

Scripts to quickly set up a development workstation or virtual machine (VM) **from scratch**.

Supports macOS and Fedora Silverblue.

## ⚡️ Quick Start

You can run the setup scripts remotely without cloning the repository:

- For **macOS**:

  ```bash
  bash <(curl -fsSL https://raw.githubusercontent.com/nicolascochin/setup_env/main/init_macos)
  ```

- For **Fedora Silverblue**:

  ```bash
  bash <(curl -fsSL https://raw.githubusercontent.com/nicolascochin/setup_env/main/init_silverblue)
  ```

## 🔧 Post-install Configuration

Once the base setup is done, you can run the `setup` script to install additional tools and configure your environment.

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/nicolascochin/setup_env/main/setup) [--shell] [--neovim] [--all] [--help]
```

### Available Options

| Option       | Description                                          |
|--------------|------------------------------------------------------|
| `--shell`    | Install ZSH, Oh My Zsh, and link configuration files |
| `--neovim`   | Install Neovim and its config                        |
| `--all`      | Run all setup steps                                  |
| `--help`     | Show the help message                                |

## 📁 Structure

```
setup_env/
├── init_macos         # macOS bootstrap script
├── init_silverblue    # Silverblue bootstrap script
├── setup              # Main setup script with modular options
├── shell/             # Shell config files
├── git/               # Git config files
└── neovim/            # Neovim config files
```

## 🎯 Goal

This project provides a reproducible and fast way to bootstrap a clean development environment — useful for personal machines, VMs, or cloud-based setups.


