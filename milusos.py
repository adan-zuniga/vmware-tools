import os

new_path = r'C:\Program Files\Cisco\JTAPI64Tools'

joined = os.path.join(new_path, 'dan.txt')

print(joined)
print(type(joined))