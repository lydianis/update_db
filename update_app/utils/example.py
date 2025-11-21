# test: global for recursion

numbers = ['a', 'b', 'c', 'd', 'e']

layer = {}
counter = 0

def recursive_function(number):
    global counter
    counter += 1
    layer[number] = {'lft': counter}
    print("NUMBER: ", number, layer[number])
    subnumbers = [i for i in numbers if i > number]
    print("SUBNUMBERS: ", subnumbers)
    
    if subnumbers != []:
        recursive_function(subnumbers[0])
        counter += 1
        layer[number] = {'rgt': counter}
        print("NUMBER: ", number, layer[number])
    else:
        counter += 1
        layer[number] = {'rgt': counter}
        print("NUMBER: ", number, layer[number])
        return layer
        

number = numbers[0]
l = recursive_function(number)
print(l)