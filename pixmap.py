def save(data, filename, maxValue=2**16-1):
    width = len(data)
    hight = len(data[0])

    outFile = open(filename, 'w')
    outFile.write('P3\n{hight} {width}\n{max}\n'.format(
                      width=width,
                      hight=hight,
                      max=maxValue)
                 )

    for i in data:
        for j in i:
            outFile.write('{}\n{}\n{}\n'.format(*j))

if __name__ == '__main__':
    import numpy as np
    image = np.array([
        np.array([np.array([255,0,0]),np.array([0,255,0]),np.array([0,0,255])]),
        np.array([np.array([255,255,255]),np.array([255,255,255]),np.array([255,255,255])]),
        np.array([np.array([255,255,255]),np.array([255,0,0]),np.array([255,255,255])]),
        np.array([np.array([255,255,255]),np.array([255,255,255]),np.array([255,255,255])]),
        np.array([np.array([155,155,155]),np.array([155,155,155]),np.array([155,155,155])])])
    save(image, 'test.ppm')
