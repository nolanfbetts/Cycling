X = [70000, 156000, 800000, 605005, 1200980]
Y = [30000, 90100, 210000, 155005, 329989]
# avergae of X
x_bar = sum(X) / len(X)
y_bar = sum(Y) / len(Y)
n = 5
# Cov(X,Y) = SUM((X - X_bar)(Y - Y_bar)) / (n)
cov_xy = sum((X[i] - x_bar) * (Y[i] - y_bar) for i in range(n)) / n
print("Cov(X,Y):", cov_xy)
for i in range(n):
    print(i)
print(x_bar)
print(y_bar)

q4 = sum((X[i] - x_bar) + (Y[i] - y_bar) for i in range(n))
print(q4)