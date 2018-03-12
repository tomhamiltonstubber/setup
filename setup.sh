wget -qO - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

sudo apt-get update
sudo apt-get install google-chrome-stable xclip git sublime-text python-pip git vim unzip python-dev python3.6-dev libjpeg-dev libmemcached-dev postgresql-client postgresql postgresql-contrib redis-server libfreetype6-dev libffi-dev postgresql-server-dev-10 curl

curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
sudo apt-get install yarn

sudo pip install virtualenv
sudo snap install micro --classic
sudo snap install spotify
sudo snap install heroku --classic

mkdir repos
cd repos/
ssh-keygen -t rsa -b 4096 -C "tomhamiltonstubber@gmail.com"
ssh-add ~/.ssh/id_rsa
xclip -sel clip < ~/.ssh/id_rsa.pub
gpg --full-generate-key
gpg --list-secret-keys --keyid-format LONG

git clone git@github.com:tomhamiltonstubber/setup.git .
git clone git@github.com:tutorcruncher/TutorCruncher2 AATutorCruncher
git clone git@github.com:tutorcruncher/TutorCruncher2 TC2
git clone git@github.com:tutorcruncher/socket-server
git clone git@github.com:tutorcruncher/socket-frontend
git clone git@github.com:tutorcruncher/help.tutorcruncher.com
git clone git@github.com:tutorcruncher/dinotutors.com
git clone git@github.com:samuelcolvin/byt.co.uk
