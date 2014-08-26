import os
import sys
from separator import sep
from envelope import env


if __name__ == '__main__':
	filepath = sys.argv[1]
	files = os.popen('dir /b '+filepath+'*.wav').readlines()
	print files
	for url in files:
		url= filepath+url[:-1]
		print url
		li1 = env(url)
		print('env success for '+url)
		li2 = sep(url)
		print('sep success for '+url)
		WriteFileData = open(url[:-4]+'.txt','w')
		WriteFileData.write(' '.join(map(str,li1+li2)))
		WriteFileData.close()
