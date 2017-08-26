import os
import re

filenames = os.listdir(os.getcwd())
for name in filenames:
    print(name)
for num in range(0, len(filenames)):
    matchObj = re.match(r'.* \((\d*)\)(.*)', filenames[num], re.M|re.I)
    if matchObj:
        os.rename(filenames[num], "hioEffect" + matchObj.group(1) + matchObj.group(2))
