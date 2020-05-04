echo "atualizando ambiente"
sudo apt-get update
echo "Instalando pip"
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
sudo apt install python3-pip
apt-get install -y python3-venv
echo "Instalando virtualenv"
sudo pip install virtualenv
echo "Criando o ambiente"
python3 -m venv saraEnv
echo "env Criado :)"
source saraEnv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
