import os
import time

current_time = time.time()

uploads_path = '/home/floydsteinberg/mysite/instance/uploads'

number_removed = 0

for filename in  os.listdir(uploads_path):
    file_path = os.path.join(uploads_path, filename)
    if (current_time - os.path.getmtime(file_path) > 3600):
        # only keep files created within the last hour
        os.remove(file_path)
        number_removed += 1

print('Done!')
print(f'{number_removed} files removed!')