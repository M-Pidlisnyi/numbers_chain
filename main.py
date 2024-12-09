

with open("numbers.txt", "r") as file:
    numbers = [line.replace("\n", "") for line in file] #file contains linebreaks, gotta remove them


#numbers = ["608017", "248460", "962282", "994725", "177092"] # smaller list for testing


def remove_non_joinable_numbers(numbers:list[str]):
    """ 
    Args:
    `numbers`: List of strings containing numbers
    
    Returns:
    `list`: Filtered list containing only numbers that can be part of a join chain
    """

    # set to track indexes of joinable numbers
    join_indexes = set()
    
    for i, num1 in enumerate(numbers):
        found_join = False
        for j, num2 in enumerate(numbers):
            if i != j:
                # Check if first two digits of num1 match last two digits of num2
                if num2[-2:] == num1[:2]:
                    found_join = True
                    break

        if not found_join:
            for j, num2 in enumerate(numbers):
                if i != j:
                    # Check if last two digits of num1 match first two digits of num2
                    if num1[-2:] == num2[:2]:
                        found_join = True
                        break
        

        if found_join:
            join_indexes.add(i)
    
    # Return list of original numbers that are joinable
    return [numbers[idx] for idx in join_indexes]


def build_chain(start_index: int, numbers: list[str]):
    """
        starts at `start_index` and looks for numbers in list to add to chain

        first tries to add numbers to the right of the first number
        then the to the left

        Args:
        `start_index`: index of first number in chain

        `numbers`: list of numbers to build chain

        Returns:
        `list`: list of numbers that represent chain starting with number at `start_index`
    
    """

    used = [False] * len(numbers) #list of used indexes
    used[start_index] = True
    chain = [numbers[start_index]]
    current = numbers[start_index]
    
    #try to join numbers to the right in the forward chain
    while True:
        found_next = False
        for j in range(len(numbers)):
            if not used[j] and numbers[j][:2] == current[-2:]:
                chain.append(numbers[j])
                used[j] = True
                current = numbers[j]
                found_next = True
                break
        
        if not found_next:
            break
    
    # Try building chain backwards(to the left)
    used = [False] * len(numbers)
    used[start_index] = True
    backwards_chain = [numbers[start_index]]
    current = numbers[start_index]
    
    while True:
        found_prev = False
        for j in range(len(numbers)):
            if not used[j] and current[:2] == numbers[j][-2:]:
                backwards_chain.insert(0, numbers[j])
                used[j] = True
                current = numbers[j]
                found_prev = True
                break
        
        if not found_prev:
            break
    
    # Combine backward and forward chains
    full_chain = backwards_chain + chain[1:]  # Skip the first number in the forward chain since it is already in the backward chain.
    return full_chain


numbers = remove_non_joinable_numbers(numbers)
longest_chain = []
for  i in range(len(numbers)):
    current_chain = build_chain(i, numbers)
    if len(current_chain) > len(longest_chain):
        longest_chain = current_chain

print(longest_chain)
    
#build result string from longest chain e.g. 248460 & 608017 & 177092 -> 2484(60)80(17)7092 -> 24846080177092
result = []
for i in range(1,len(longest_chain)):
    current = longest_chain[i-1]
    current_trimmed = current[:-2]
    result.append(current_trimmed)
    
result.append(longest_chain[-1])
result = "".join(result)
print(result)