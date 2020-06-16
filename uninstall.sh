echo "A remoção do Sara consiste na remoção do ambiente SaraEnv"
echo "Deseja prosseguir?"
select yn in "S" "N"; do
    case $yn in
        S ) rm -rf SaraEnv; echo "Removido :)"; break;;
        N ) exit;;
    esac
done
