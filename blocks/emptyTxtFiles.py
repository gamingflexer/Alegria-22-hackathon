def emptyB():
    for i in range(12):
        print(i + 1)
        f = open(str(i + 1) + "b.txt", "w")
        f.write('')
        f.close()


def emptyBClean():
    for i in range(12):
        print(i + 1)
        f = open(str(i + 1) + "bclean.txt", "w")
        f.write('')
        f.close()


emptyB()
emptyBClean()

