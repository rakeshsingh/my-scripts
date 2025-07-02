#!/bin/bash
#
# macOS Developer Tools Installer
# Automates installation of common development tools on macOS
#

# Exit on error
set -e

# Text formatting
BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

# Print formatted message
print_message() {
  echo -e "${BOLD}${2:-$GREEN}$1${RESET}"
}

# Check if Homebrew is installed
check_brew() {
  print_message "Checking if Homebrew is installed..."
  if ! command -v brew &>/dev/null; then
    print_message "Homebrew not found. Installing Homebrew..." "$YELLOW"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add Homebrew to PATH based on chip architecture
    if [[ $(uname -m) == "arm64" ]]; then
      print_message "Adding Homebrew to PATH for Apple Silicon..." "$YELLOW"
      echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >>~/.zprofile
      eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
  else
    print_message "Homebrew is already installed."
  fi
}

# Update Homebrew
update_brew() {
  print_message "Updating Homebrew..."
  brew update
}

# Install tools
install_tools() {
  print_message "Installing developer tools..."

  # Define tools to install
  tools=(
    "neovim"  # Modern vim text editor
    "bat"     # Cat clone with syntax highlighting
    "fd"      # Simple, fast alternative to find
    "ripgrep" # Fast grep alternative
    "fzf"     # Fuzzy finder
    "jq"      # JSON processor
    "git"     # Version control
    "tmux"    # Terminal multiplexer
    "htop"    # Process viewer
    "tree"    # Directory listing as tree
    "python3" # python programming language
    "sqlite"  # sqlite for simple data storage and queries
  )

  # Install each tool if not already installed
  for tool in "${tools[@]}"; do
    if brew list "$tool" &>/dev/null; then
      print_message "$tool is already installed." "$GREEN"
    else
      print_message "Installing $tool..." "$YELLOW"
      brew install "$tool"
      print_message "$tool installed successfully." "$GREEN"
    fi
  done
}

# Setup Neovim configuration
setup_neovim() {
  print_message "Setting up Neovim configuration..."

  # Create Neovim config directory if it doesn't exist
  nvim_config_dir="$HOME/.config/nvim"
  if [ ! -d "$nvim_config_dir" ]; then
    mkdir -p "$nvim_config_dir"
    print_message "Created Neovim config directory at $nvim_config_dir"
  fi

  # Create a basic init.vim config file if it doesn't exist
  init_vim="$nvim_config_dir/init.vim"
  if [ ! -f "$init_vim" ]; then
    cat >"$init_vim" <<EOF
" Basic Neovim Configuration

" General settings
set number          " Show line numbers
set relativenumber  " Show relative line numbers
set expandtab       " Use spaces instead of tabs
set tabstop=2       " Tab width is 2 spaces
set shiftwidth=2    " Indent with 2 spaces
set smartindent     " Enable smart indentation
set ignorecase      " Ignore case when searching
set smartcase       " Override ignorecase if search contains uppercase
set undofile        " Enable persistent undo
set termguicolors   " Enable true color support
set mouse=a         " Enable mouse support
set clipboard+=unnamedplus  " Use system clipboard

" Key mappings
let mapleader = " "  " Set leader key to space

" Basic key bindings
nnoremap <leader>w :w<CR>
nnoremap <leader>q :q<CR>
nnoremap <leader>h :nohl<CR>

" Split navigation
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Buffer navigation
nnoremap <leader>bn :bnext<CR>
nnoremap <leader>bp :bprevious<CR>
nnoremap <leader>bd :bdelete<CR>
EOF
    print_message "Created basic Neovim configuration at $init_vim"
  else
    print_message "Neovim configuration already exists. Skipping..." "$YELLOW"
  fi
}

# Create shell aliases
create_aliases() {
  print_message "Setting up useful shell aliases..."

  # Determine which shell configuration file to use
  if [ -f "$HOME/.zshrc" ]; then
    shell_config="$HOME/.zshrc"
  elif [ -f "$HOME/.bashrc" ]; then
    shell_config="$HOME/.bashrc"
  else
    print_message "Could not find .zshrc or .bashrc. Creating .zshrc..." "$YELLOW"
    touch "$HOME/.zshrc"
    shell_config="$HOME/.zshrc"
  fi

  # Add aliases if they don't already exist
  if ! grep -q "# Developer tool aliases" "$shell_config"; then
    cat >>"$shell_config" <<EOF

# Developer tool aliases
alias vim="nvim"
alias vi="nvim"
alias ls="exa --color=auto --icons"
alias ll="exa -l --color=auto --icons"
alias la="exa -la --color=auto --icons"
alias lt="exa --tree --level=2 --color=auto --icons"
alias cat="bat"
alias find="fd"
alias grep="rg"
#set up pretty git log
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
EOF
    print_message "Added useful aliases to $shell_config"
    print_message "Remember to run 'source $shell_config' to apply changes" "$YELLOW"
  else
    print_message "Aliases already exist in $shell_config. Skipping..." "$YELLOW"
  fi
}

# Main function
main() {
  print_message "Starting macOS developer tools installation..." "$BOLD"

  check_brew
  update_brew
  install_tools
  setup_neovim
  create_aliases

  print_message "Installation complete! 🎉" "$GREEN"
  print_message "Remember to restart your terminal or run 'source ~/.zshrc' (or ~/.bashrc) to apply all changes." "$YELLOW"
}

# Run the script
main
