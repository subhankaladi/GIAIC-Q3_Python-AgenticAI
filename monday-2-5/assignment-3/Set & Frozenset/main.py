#Sets and Frozensets in Python 

numbers_set = {1,2,3,4,5,2} #duplicates will be removed automatically
print("Set Of Numbers", numbers_set)



numbers_set.add(6)
print("After Adding 6:", numbers_set)

numbers_set.remove(3)
print("After removing 3:", numbers_set)

print("Is 2 in set?", 2 in numbers_set)

for num in numbers_set:
    print("Number:", num)

set_a = {1,2,3,4}
set_b = {3,4,5,6}

print("Union:", set_a.union(set_b)) # combine both sets
print("InterSection:", set_a.intersection(set_b)) #Common elements
print("Difference (A - B):", set_a.difference(set_b)) #Elements in A but nor in B
print("Symmetric Difference:", set_a.symmetric_difference(set_b)) #Elements in A or B but not both


frozen_numbers = frozenset(numbers_set)
print('Frozen Set:', frozen_numbers)

#Frozenset do not support modification 

# frozen_numbers.add(7) #This will be Cause and error

#Checking Membership in fronzenset
print("Is 4 in frozenset:", 4 in frozen_numbers)
 
for num in frozen_numbers:
    print("Frozen Number:", num)

frozen_a = frozenset({1,2,3})
frozen_b = frozenset({3,4,5})

print("Frozen Union", frozen_a | frozen_b)
print("Frozen Intersection:", frozen_a & frozen_b)
print("Frozen Differnce:", frozen_a - frozen_b)
print("Frozen Symmetric Difference:", frozen_a ^ frozen_b)