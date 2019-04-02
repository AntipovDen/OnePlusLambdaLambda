filenames = ['one-plus-lambda-lambda-{}.out'.format(i) for i in range(1, 10)]


data = dict()
for file in filenames:
    with open(file, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines) // 2):
            if lines[2 * i] not in data.keys():
                data[lines[2 * i]] = []
            data[lines[2 * i]] += [int(s) for s in lines[2 * i + 1].split()]

with open("one-plus-lambda-lambda.out", 'w') as f:
    for key in data.keys():
        f.write(key)
        # f.write('len{} '.format(len(data[key])))
        for i in data[key]:
            f.write('{} '.format(i))
        f.write('\n')
