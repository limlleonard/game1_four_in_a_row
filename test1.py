import numpy as np

# Create a 3x4 numpy array
array_3x4 = np.array([[1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 11, 12]])

# Transform it into a 1D array with 12 elements
array_1d_ravel = array_3x4.ravel()  # Using ravel
array_1d_flatten = array_3x4.flatten()  # Using flatten
array_1d_reshape = array_3x4.reshape(-1)  # Using reshape

print("Original 3x4 array:")
print(array_3x4)

print("\n1D array using ravel:")
print(array_1d_ravel)

print("\n1D array using flatten:")
print(array_1d_flatten)

print("\n1D array using reshape:")
print(array_1d_reshape)
