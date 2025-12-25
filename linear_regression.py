import numpy as np
x = np.array([8, 10, 12])
y = np.array([10, 13, 16])

#for simple linear regression
deviation_of_x = x - np.mean(x)
deviation_of_y = y - np.mean(y)

a = np.sum(deviation_of_x * deviation_of_y) / np.sum(deviation_of_x ** 2)
#intercept of the function
b = np.mean(y) - a*np.mean(x)
#the linear regression equation
def linear_regression(x):
    return a*x + b
#testing the function
test_case = int(input("Enter a value for x: "))
print("Predicted value of y:", linear_regression(test_case))
