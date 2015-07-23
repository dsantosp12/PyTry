__author__ = 'dsantos'


def prepare_items(items=""):

    list = items.split(')')

    new = []
    for x in list:
        new.append(x.replace('(', ''))

    last = []
    for i in new:
        last.append(tuple(i.split(',')))

    return last

if __name__ == '__main__':
    print(prepare_items("(2, 1 G. Supra Cuaba Liquid Soap, 30, 60)(1, 30 Onz. Supra Cuaba Liquid Soap, 26, 26)(3, 50 Onz. Supra Cuaba Liquid Soap, 28, 84)"))