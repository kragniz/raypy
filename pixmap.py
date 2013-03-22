def save(data, filename):
    width = len(data)
    hight = len(data[0])

    outFile = open(filename, 'w')
    outFile.write('P3\n{width} {hight}\n'.format(width=width, hight=hight))

    for i in data:
        for j in i:
            outFile.write('{} {} {}  '.format(*j))
        outFile.write('\n')

if __name__ == '__main__':
    import numpy as np
    image = np.array([
        np.array([np.array([255,255,255]),np.array([255,255,255]),np.array([255,255,255])]),
        np.array([np.array([255,255,255]),np.array([255,255,255]),np.array([255,255,255])]),
        np.array([np.array([255,255,255]),np.array([255,0,0]),np.array([255,255,255])]),
        np.array([np.array([255,255,255]),np.array([255,255,255]),np.array([255,255,255])]),
        np.array([np.array([155,155,155]),np.array([155,155,155]),np.array([155,155,155])])])
    save(image, 'test.ppm')
