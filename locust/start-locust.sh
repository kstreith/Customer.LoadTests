#! /bin/sh

if [ "$show_ui" = "" ]
then
    locust -f locustfile.py
    
else
    locust -f locustfile.py --no-web -c $user_count -r $hatch_rate
fi