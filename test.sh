# start cassandra
~/git/cassandra/bin/cassandra -p PIDFILE

sleep 30

# schedule leap second in the background for 10 seconds from now
# TODO: remove unnecessary bits from leap-a-day
echo -n 'starting leap-a-day at ' 
date -u +%s
sudo ./bin/leap-a-day -i1 -s & &>/dev/null

# insert values for 30 seconds
python insert-keys.py

kill $(cat PIDFILE)

