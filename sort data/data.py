set = {}
with open("../data.txt", "r") as f:
    data = f.read().splitlines()
    for d in data:
        q.put(p)