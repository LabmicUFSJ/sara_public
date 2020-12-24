for i in 'ansiedade_retweet/median'  'ansiedade_retweet/top'
do
    for entry in "brasnam/sample_users_name/$i"/*
    do
        echo $entry
        python3 sarabot_by_names.py 'mestrado' 'ansiedade' $entry
    done
done

for i in 'stf_retweet/median'  'stf_retweet/top'
do
    for entry in "brasnam/sample_users_name/$i"/*
    do
        echo $entry
        python3 sarabot_by_names.py 'mestrado' 'stf' $entry
    done
done

for i in 'vacina_retweet/median'  'vacina_retweet/top'
do
    for entry in "brasnam/sample_users_name/$i"/*
    do
        echo $entry
        python3 sarabot_by_names.py 'mestrado' 'vacina_all_databases' $entry
    done
done
