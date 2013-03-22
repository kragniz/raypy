def save(data, filename):
    width = len(data)
    hight = len(data[0])

    outFile = open(filename, 'w')
    outFile.write('P3\n{width} {hight}\n'.format(width=width, hight=hight))

    for i in data:
        for j in i:
            outFile.write('{} {} {}  '.format(*j))
        outFile.write('\n')
