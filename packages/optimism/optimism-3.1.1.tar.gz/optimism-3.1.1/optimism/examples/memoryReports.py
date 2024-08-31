import optimism as opt

words = ['hi', 'bye']
pair = [words, words]
print(opt.memoryReport(words=words, pair=pair))

knot = [pair, words]
knot.append(knot)
print(opt.memoryReport(pair=pair, words=words, knot=knot))
