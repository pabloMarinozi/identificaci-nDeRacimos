file1 = open('nubes_circlenet0.9.csv', 'r')
Lines = file1.readlines()
file2 = open('nubes_circlenet0.9_saved.csv', 'a')
  
first = True
# Strips the newline character
for line in Lines:
	if first:
		print
		first=False
		file2.write(line[1:])
		continue
	line = line.split('"[')
	#print(len(line[1]))
	line = line[1].replace(']",','')
	line = line.replace("'","")
	file2.write(line)
	file2.write("\n")
