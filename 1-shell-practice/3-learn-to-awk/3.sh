awk '{for(i=1;i<=NF;i++){split($i,seg,"_");printf("%s",seg[1])};printf "\n"}' 3.dat
