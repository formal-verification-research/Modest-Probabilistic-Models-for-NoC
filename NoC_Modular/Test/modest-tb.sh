# The main parsing function
RED='\033[0;31m'
GREEN='\033[0;32m'
NONE='\033[0m'
parse()
{
   results=$(echo "$@" | grep 'Property\|Probability' | tr ' ' '_' | tr '\n' ' ')
   for line in $results
   do
      if [ "$line" == "__Probability:_0_" ];
      then
         echo -e "    ${RED}Failed${NONE}"
      elif [ "$line" == "__Probability:_1_" ];
      then
         echo -e "    ${GREEN}Passed${NONE}"
      else
         test=$(echo "${line/+_Property_/  Property: }" | tr '_' ' ')
         echo "$test"
      fi
   done
}



# Run test
printf "\nStarting test...\n"
input=$(modest check $1)
parse "$input"



# Give some extra space
printf "\n"
