from loopex import LoopEx

do_while = LoopEx().do_while
result = ''
i = 0

while do_while(i < 5):
    i += 1
    result += str(i)

print(result)
