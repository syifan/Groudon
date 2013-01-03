import sys

a = [',','\n','\r','\'','<','>','&','"','\\']
b = [' ','<br>',' ','&#39;','&lt;','&gt;','&amp;','&#34;','&#92;']

def trim(data):
	i = 0
	while i < len(data):
		for j in [0,1,2,3,4,5,6,7,8]:
			if data[i] == a[j]:
				data = data.replace(data[i],' ')
		
		i +=1
	return data

