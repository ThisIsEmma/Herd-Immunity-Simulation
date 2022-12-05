
from datetime import datetime


this_name = 'Edith'

my_object = [{'name' : this_name},
                {'age': 32}
            ]

for i in my_object:
 for key, value in i.items():
    print(key,value)

print(datetime.now())