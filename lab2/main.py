a = int(input())
b = int(input())
c = int(input())
d = (b * b) - (4 * a * c)
if d < 0:
    print("Нет корней")
if d == 0:
    print("X = " + str((b * -1) / (2 * a)))
if d > 0:
    print("X1 = " + str(((b * -1) + d ** 0.5) / (2 * a)) + "\n" + "X2 = " + str(((b * -1) - d ** 0.5) / (2 * a)))
#4 0 8
#1 17 -18
#1 -6 9