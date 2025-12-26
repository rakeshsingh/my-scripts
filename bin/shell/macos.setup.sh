# some setup to have consistent environment
brew update
#install essential softwares
brew install neovim #alternate to vim
brew install python3

# install and setup git
brew install git
#set up pretty git log
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

#install python organize
pip3 install -U organize-tool
organize config --path ~/personal/my-scripts/config/organize-tool.yaml

brew install sqlite #sqlite for basic data manipulation

# intstall modern equivalents of common command line tools
brew install bat  #replace cat with bat
brew install fd   #replace find with fd
brew install htop #alternate of top
brew install jq   #alternate of sed for json files
