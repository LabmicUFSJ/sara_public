echo "Bem vindo a instalação da Sara"
echo "O processo de instalação consiste na criação do ambiente SaraEnv"
echo "Atualizando ambiente"
sudo apt-get update
echo "Instalando pip."
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
sudo apt install python3-pip
sudo apt-get install -y python3-venv
echo "Instalando virtualenv."
python3 -m pip install virtualenv
echo "Criando o ambiente virtual."
python3 -m venv SaraEnv
echo "env Criado :)"
source SaraEnv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade wheels setuptools
python3 -m pip install -r requirements.txt
echo "A Sara foi instalado com sucesso :)"
echo "Agora, acesse o ambiente e começe a utilizar o Framework :)"
echo "Você pode acessar o ambiente com source/SaraEnv/bin/activate"
