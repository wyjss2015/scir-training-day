awk 'BEGIN{FS=", "}{print $2}' 2.dat | sed "s/'\(.*\)'/\1/g"
