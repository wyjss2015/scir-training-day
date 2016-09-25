awk 'BEGIN{total=0}{total+=$2;$3=total;print}' 2.dat
