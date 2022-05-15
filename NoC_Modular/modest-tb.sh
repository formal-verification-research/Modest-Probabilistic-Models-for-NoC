# The main parsing function
RED='\033[0;31m'
GREEN='\033[0;32m'
NONE='\033[0m'
parse()
{
   results=$(echo "$@" | grep 'Property\|Probability\|Decision' | tr ' ' '_' | tr '\n' ' ')
   for line in $results
   do
      if [ "$line" == "____Decision:______________False_" ];
      then
         echo -e "        ${RED}Failed${NONE}"
      elif [ "$line" == "____Decision:______________True_" ];
      then
         echo -e "        ${GREEN}Passed${NONE}"
      else
         test=$(echo "${line/+_Property_/  Property: }" | tr '_' ' ')
         echo "$test"
      fi
   done
}



# Run test
printf "\nStarting test...\n"
input=$(modest simulate --max-run-length 0 $1)
parse "$input"



# Give some extra space
printf "\n"
