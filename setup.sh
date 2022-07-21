wget -qO - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
sudo apt-add-repository https://cli.github.com/packages -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo add-apt-repository ppa:peek-developers/stable -y

sudo apt-get update &&
sudo apt-get install -y \
python3.9 python3.9-dev python3-pip python3-distutils python3.9-distutils \
google-chrome-stable xclip git gh sublime-text vim unzip \
libjpeg-dev libmemcached-dev postgresql-client postgresql postgresql-server-dev-14 \
postgresql-contrib redis-server libfreetype6-dev libffi-dev \
curl gnome-tweaks chrome-gnome-shell peek python3-virtualenv

curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

sudo apt-get install yarn npm -y

sudo pip install virtualenv awscli
sudo pip3 install devtools
sudo snap install micro --classic
sudo snap install spotify
sudo snap install heroku --classic
sudo snap install pycharm-professional --classic
sudo snap install slack --classic

ssh-keygen -t rsa -b 4096 -C "tomhamiltonstubber@gmail.com"
ssh-add ~/.ssh/id_rsa
xclip -sel clip < ~/.ssh/id_rsa.pub
gpg --full-generate-key
gpg --list-secret-keys --keyid-format LONG

cd ~/
mkdir repos
cd repos/
git clone git@github.com:tutorcruncher/TutorCruncher2 && \
git clone git@github.com:tutorcruncher/socket-frontend && \
git clone git@github.com:tutorcruncher/tutorcruncher.com && \
git clone git@github.com:tomhamiltonstubber/setup .
