"""
Last configured for 23.04 on 03/05/2023
"""

# Google chrome

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# Dependencies

sudo apt update
sudo apt install -y \
build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Tools

sudo apt install -y git curl

# Python

# Install python3.10
# This may need changed for different versions. Also, check to see if the deadsnakes PPA has the correct version first.
wget https://www.python.org/ftp/python/3.10.6/
tar –xf python-3.10.*.tgz
sudo make –j $(nproc)
sudo make install
sudo apt install python3-pip

# Then adding deadsnakes for the other python versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-dev

# Redis

sudo snap install redis

# Postgresql

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
sudo apt -y install postgresql-15 postgresql-server-dev-15

# Other programs

snap install sublime-text --classic
sudo apt install peek
sudo snap install micro --classic
sudo snap install spotify
sudo snap install heroku --classic
sudo snap install pycharm-professional --classic
sudo snap install slack --classic
sudo pip3 install virtualenv awscli devtools
sudo apt install gh xclip

# Yarn/NPM

curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn npm -y

# Generate RSA key

ssh-keygen -t rsa -b 4096 -C "tomhamiltonstubber@gmail.com"
ssh-add ~/.ssh/id_rsa
xclip -sel clip < ~/.ssh/id_rsa.pub
echo "RSA key copied to clipboard. Paste into https://github.com/settings/keys then press a key to continue"
read -n 1 -s

# Clone repos

git clone git@github.com:tomhamiltonstubber/setup repos
git clone git@github.com:tutorcruncher/TutorCruncher2 repos/TutorCruncher2
git clone git@github.com:tutorcruncher/tutorcruncher.com  repos/tutorcruncher.com

# Update .bashrc with custom files

echo -e "\nif [ -f ~/repos/.bash_custom ]; then\n  . ~/repos/.bash_custom\nfi" >> .bashrc

# Add .gitconfig file

touch ".gitconfig"
echo -e "[user]\n\tname = Tom Hamilton Stubber\n\temail = tomhamiltonstubber@gmail.com\n[include]\n\tpath = ~/repos/.git_custom" >> .gitconfig

# Create the .data dir for tests/linting

mkdir repos/.data