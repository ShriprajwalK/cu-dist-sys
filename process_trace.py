login = []
rating = []

with open('./100.txt') as f:
    for line in f:
        if line[0] == 'L' and line[1] == 'O':
            print(line)
            login.append(float(line.split(':')[1].strip()))

        if line[0] == 'R':
            rating.append(float(line.split(':')[1].strip()))

print(len(login))
print(len(rating))
print('AVG LOGIN:', sum(login)/len(login))
print('AVG RATING:', sum(rating)/len(rating))

