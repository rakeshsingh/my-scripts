# some setup to have consistent environment
brew update

# install and setup git
brew install git
#set up pretty git log
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# install spark to support battery
brew install spark 

# install battery
brew tap Goles/battery
brew install battery
