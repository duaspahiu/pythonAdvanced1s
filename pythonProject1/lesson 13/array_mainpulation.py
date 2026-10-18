import numpy as np

array2d = np.array([
                   [1,2,3,4,5],
                   [6,7,8,9,10]
                   ])

print(array2d)

elemnti = array2d[0,2]
print(elemnti)

dimezioni = array2d.ndim
print(Dimenzioni)


arrayShape = array2d.shape
print(arrayShape)

arraySize = array2d.size
print(ArraySize)

ndaje = array2d[:2,:2]

print(ndaje)

shuma=np.sum(array2d)
print(shuma)

sum_column = np.sum(array2d,axis=0)
print(sum_column)