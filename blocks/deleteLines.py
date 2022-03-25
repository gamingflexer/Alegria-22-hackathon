"""import hashlib


def removeWords():
    bad_words = ['Message', 'logo', 'See credential', 'Expiration Date','followers','See all','�','comments','.pdf']
    for i in range(12):
        with open(str(i + 1) + 'bclean.txt') as oldfile, open(str(i + 1) + 'b.txt', 'w') as newfile:
            for line in oldfile:
                if not any(bad_word in line for bad_word in bad_words):
                    newfile.write(line)


def removeDupes():
    for i in range(12):
        inputFile = str(i + 1) + 'b.txt'
        outputFile = str(i + 1) + 'bclean.txt'
        completed_lines_hash = set()
        output_file = open(outputFile, "w")
        for line in open(inputFile, "r"):
            hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
            if hashValue not in completed_lines_hash:
                output_file.write(line)
                completed_lines_hash.add(hashValue)
        output_file.close()


removeDupes()
removeWords()
"""