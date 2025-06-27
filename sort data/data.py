data = {}
with open("data.txt", "r") as f:
    lines = f.read().split("\n")
    print(lines[1])
    for l in lines:
       s = l.split()
       print(s)
       if(len(s) > 1):
        data[s[1]] = s[0]

sorted_data = dict(sorted(data.items(), key=lambda item: item[1]))
print(sorted_data)