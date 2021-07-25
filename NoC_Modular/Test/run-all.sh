# The main parsing function
RED='\033[0;31m'
GREEN='\033[0;32m'
NONE='\033[0m'
parse()
{
   results=$(echo "$@" | grep 'Property\|Probability' | tr ' ' '_' | tr '\n' ' ')
   for line in $results
   do
      if [ "$line" == "__Probability:_0" ];
      then
         echo -e "    ${RED}Failed${NONE}"
      elif [ "$line" == "__Probability:_1" ];
      then
         echo -e "    ${GREEN}Passed${NONE}"
      else
         test=$(echo "${line/+_Property_/  Property: }" | tr '_' ' ')
         echo "$test"
      fi
   done
}



# Run test 1
printf "\nStarting test 1...\n"
input=$(modest check 1-is-in-row.modest)
parse "$input"

# Run test 2
printf "\nStarting test 2...\n"
input=$(modest check 2-send.modest)
parse "$input"

# Run test 3
printf "\nStarting test 3...\n"
input=$(modest check 3-receive-send.modest)
parse "$input"

# Run test 4
printf "\nStarting test 4...\n"
input=$(modest check 4-prioritize.modest)
parse "$input"



# Give some extra space
printf "\n\n\n"
