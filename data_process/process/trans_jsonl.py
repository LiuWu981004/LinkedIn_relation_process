import  json

with open('/home/lw/桌面/google.jsonl')as one:
    lines = [line for line in one.readlines()]

# print(len(lines))
print(type(''.join(lines)))
new = json.loads(''.join(lines))
print(new,type(new))

with open('/home/lw/桌面/new_google.jsonl','w')as jl:
    jl.write(json.dumps(json.loads(''.join(lines)))+'\n')

