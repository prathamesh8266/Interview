
a = {'is': {'for': {'geeks': 8}}, 'gfg': {'is': 4, 'best': 10}} 

def solve(temp_dict, flattened_list):
    
    for key in temp_dict.keys():
        if not isinstance(temp_dict[key], dict):
            flattened_list.extend([key, temp_dict[key]])
        else:
            flattened_list.append(key)
            solve(temp_dict[key], flattened_list)
        
    return flattened_list

a = {'is': {'for': {'geeks': 8}}, 'gfg': {'is': 4, 'best': 10, 'test':[1,2,3,4]}}
for i in a.keys():
    print(solve( {i:a[i]}, []))
        

# The original dictionary is : {'is': {'for': {'geeks': 8}}, 'gfg': {'is': 4, 'best': 10}} 
# The flattened dictionary elements : [['is', 'for', 'geeks', 8], ['gfg', 'is', 4, 'best', 10]]  