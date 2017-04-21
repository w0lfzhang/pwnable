
shellcode = "eb165b31c0884307895b0889"  #put your shellcode here
result = ""
sclen = len(shellcode)
for i in range(0, sclen, 2):
	result += "\\x" + shellcode[i:i+2]

print result
	      
