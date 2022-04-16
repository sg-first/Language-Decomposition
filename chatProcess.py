f=open('富农大.txt','r',encoding='utf-8')
content=[]
while True:
    line = f.readline()
    if line:
        if line=='' or line[0]=='2':
            continue
        else:
            content.append(line)
    else:
        break
f.close()

content.sort(key=lambda x:len(x),reverse=True)

num=0
for i in content:
    print(i)
    num+=1
    if num==100:
        break
