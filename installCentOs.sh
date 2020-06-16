echo "Bem vindo a instalação da Sara"
echo "Executando o script para CentOS 7"
echo "O processo de instalação consiste na criação do ambiente SaraEnv"
echo "Atualizando ambiente"
sudo yum -y update
echo "Instalando pip"
yum -y install python3-pip
echo "Instalando virtualenv"
python3 -m pip install virtualenv
echo "Criando o ambiente virtual."
virtualenv saraEnv
echo "env Criado :)"
source saraEnv/bin/activate
echo "Instalando dependências."
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade wheels setuptools
python3 -m pip install -r requirements.txt
echo "A Sara foi instalado com sucesso :)"
echo "Agora, acesse o ambiente e começe a utilizar o Framework :)"
echo "Você pode acessar o ambiente com source saraEnv/bin/activate"