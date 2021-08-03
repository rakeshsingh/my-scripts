# some setup to have consistent environment
brew update
#install essential softwares
brew install vim
brew install python3 

# install and setup git
brew install git
#set up pretty git log
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# install spark to support battery
brew install spark 

# install battery
brew tap Goles/battery
brew install battery

#install python organize
pip3 install -U organize-tool
organize config --path ~/personal/my-scripts/config/organize-tool.yaml
