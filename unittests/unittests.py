from utils import *
from unittest import TestCase

"""
For each operation, you should write tests to test  on matrices of different sizes.
Hint: use dp_mc_matrix to generate dumbpy and numc matrices with the same data and use
      cmp_dp_nc_matrix to compare the results
"""


class TestAdd(TestCase):
    def test_func(self):
        # valid input
        _, nc_mat1 = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])
        _, nc_mat2 = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])
        cmp_dp_nc_matrix(nc.Matrix([[2, 4, 6], [4, 10, 12]]), nc_mat1 + nc_mat2)

        # TypeError if b is not of type numc.Matrix
        with self.assertRaises(TypeError):
            result = nc_mat1 + 1

        # ValueError if a and b don't have the same dim
        with self.assertRaises(ValueError):
            result = nc_mat1 + nc.Matrix([1, 2, 3])

    def test_small_add(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(2, 2, seed=1)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat1, dp_mat2] * 10, [nc_mat1, nc_mat2] * 10, "add")
            self.assertTrue(is_correct)
            print_speedup(speed_up)

    def test_medium_add(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(100, 100, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(100, 100, seed=1)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat1, dp_mat2] * 10, [nc_mat1, nc_mat2] * 10, "add")
            self.assertTrue(is_correct)
            print_speedup(speed_up)

        dp_mat1, nc_mat1 = dp_nc_matrix(100, 100, 1)
        is_correct, speed_up = compute([dp_mat1, dp_mat1] * 10, [nc_mat1, nc_mat1] * 10, "add")
        self.assertTrue(is_correct)
        print("fill + add speed up: ")
        print_speedup(speed_up)

    def test_large_add(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(20000, 20000, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(20000, 20000, seed=1)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat1, dp_mat2] * 10, [nc_mat1, nc_mat2] * 10, "add")
            self.assertTrue(is_correct)
            print_speedup(speed_up)


class TestSub(TestCase):
    def test_func(self):
        _, nc_mat1 = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])
        _, nc_mat2 = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])
        cmp_dp_nc_matrix(nc.Matrix([[0, 0, 0], [0, 0, 0]]), nc_mat1 - nc_mat2)

        # TypeError if b is not of type numc.Matrix
        with self.assertRaises(TypeError):
            result = nc_mat1 - 1

        # ValueError if a and b don't have the same dim
        with self.assertRaises(ValueError):
            result = nc_mat1 - nc.Matrix([1, 2, 3])

    def test_small_sub(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(2, 2, seed=1)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "sub")
            self.assertTrue(is_correct)
            print_speedup(speed_up)

    def test_medium_sub(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(100, 100, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(100, 100, seed=1)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat1, dp_mat2] * 10, [nc_mat1, nc_mat2] * 10, "sub")
            self.assertTrue(is_correct)
            print_speedup(speed_up)

    def test_large_sub(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(20000, 20000, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(20000, 20000, seed=1)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat1, dp_mat2] * 10, [nc_mat1, nc_mat2] * 10, "sub")
            self.assertTrue(is_correct)
            print_speedup(speed_up)


class TestAbs(TestCase):
    def test_func(self):
        _, nc_mat1 = dp_nc_matrix([[1, -2, 3], [-4, 5, -6]])
        cmp_dp_nc_matrix(nc.Matrix([[1, 2, 3], [4, 5, 6]]), abs(nc_mat1))
        cmp_dp_nc_matrix(nc.Matrix([[1, -2, 3], [-4, 5, -6]]), nc_mat1)

    def test_small_abs(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat], [nc_mat], "abs")
            self.assertTrue(is_correct)
            print_speedup(speed_up)

    def test_medium_abs(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2000, 2000, seed=0)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat], [nc_mat], "abs")
            self.assertTrue(is_correct)
            print_speedup(speed_up)

    def test_large_abs(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(20000, 20000, seed=0)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat], [nc_mat], "abs")
            self.assertTrue(is_correct)
            print_speedup(speed_up)


class TestNeg(TestCase):
    def test_func(self):
        _, nc_mat1 = dp_nc_matrix([[1, -2, 3], [-4, 5, -6]])
        cmp_dp_nc_matrix(nc.Matrix([[-1, 2, -3], [4, -5, 6]]), -nc_mat1)
        cmp_dp_nc_matrix(nc.Matrix([[1, -2, 3], [-4, 5, -6]]), nc_mat1)

    def test_small_neg(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat], [nc_mat], "neg")
            self.assertTrue(is_correct)
            print_speedup(speed_up)

    def test_medium_neg(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(1000, 1000, seed=0)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat], [nc_mat], "neg")
            self.assertTrue(is_correct)
            print_speedup(speed_up)

    def test_large_neg(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(20000, 20000, seed=0)
        print("")
        for _ in range(10):
            is_correct, speed_up = compute([dp_mat], [nc_mat], "neg")
            self.assertTrue(is_correct)
            print_speedup(speed_up)


class TestMul(TestCase):
    def test_func(self):
        _, nc_mat1 = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])
        _, nc_mat2 = dp_nc_matrix([[1, 2], [3, 4], [5, 6]])
        cmp_dp_nc_matrix(nc.Matrix([[22, 28], [49, 64]]), nc_mat1 * nc_mat2)

        # TypeError if b is not of type numc.Matrix
        with self.assertRaises(TypeError):
            result = nc_mat1 * 1

        # ValueError if the dim not match
        with self.assertRaises(ValueError):
            result = nc_mat1 * nc.Matrix([1, 2, 3])

    def test_small_mul(self):
        pass
        # TODO: YOUR CODE HERE
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(2, 2, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_medium_mul(self):
        # TODO: YOUR CODE HERE
        pass

    def test_large_mul(self):
        # TODO: YOUR CODE HERE
        pass


class TestPow(TestCase):
    def test_func(self):
        _, nc_mat1 = dp_nc_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        _, nc_mat2 = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])
        cmp_dp_nc_matrix(nc.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), nc_mat1 ** 0)
        cmp_dp_nc_matrix(nc.Matrix([[468, 576, 684], [1062, 1305, 1543], [1656, 2034, 2412]]), nc_mat1 ** 3)
        cmp_dp_nc_matrix(nc.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), nc_mat1)

        # TypeError if b is not of type numc.Matrix
        with self.assertRaises(TypeError):
            result = nc_mat1 ** 1.0

        # ValueError if pow is negative, or a is not a square matrix
        with self.assertRaises(ValueError):
            result = nc_mat1 ** -1
        with self.assertRaises(ValueError):
            result = nc_mat2 ** 3

    def test_small_pow(self):
        pass
        # TODO: YOUR CODE HERE
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        is_correct, speed_up = compute([dp_mat, 3], [nc_mat, 3], "pow")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_medium_pow(self):
        # TODO: YOUR CODE HERE
        pass

    def test_large_pow(self):
        # TODO: YOUR CODE HERE
        pass


class TestGet(TestCase):
    def test_get(self):
        # valid input
        _, nc_mat = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])
        print(nc_mat.get(1, 1))
        cmp_dp_nc_matrix(nc.Matrix([[1, 2, 3], [4, 5, 6]]), nc_mat)

        # TypeError if number of args is not 2, if i or j are not ints
        with self.assertRaises(TypeError):
            nc_mat.get(1, 1, 1)
        with self.assertRaises(TypeError):
            nc_mat.get(1.0, 1)
        with self.assertRaises(TypeError):
            nc_mat.get(1, 1.0)

        # IndexError if i or j or both are out of range
        with self.assertRaises(IndexError):
            nc_mat.get(10, 1)
        with self.assertRaises(IndexError):
            nc_mat.get(1, 10)
        with self.assertRaises(IndexError):
            nc_mat.get(10, 10)

    def test_get(self):
        # TODO: YOUR CODE HERE
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        rand_row = np.random.randint(dp_mat.shape[0])
        rand_col = np.random.randint(dp_mat.shape[1])
        self.assertEqual(round(dp_mat[rand_row][rand_col], decimal_places),
                         round(nc_mat[rand_row][rand_col], decimal_places))


class TestSet(TestCase):
    def test_set(self):
        # valid input
        _, nc_mat = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])
        nc_mat.set(1, 1, 10)
        cmp_dp_nc_matrix(nc.Matrix([[1, 2, 3], [4, 10, 6]]), nc_mat)

        # TypeError if number of args is not 3, if i or j are not ints, or val is not a float/int
        with self.assertRaises(TypeError):
            nc_mat.set(1, 1, 1, 10)
        with self.assertRaises(TypeError):
            nc_mat.set(1.0, 1, 10)
        with self.assertRaises(TypeError):
            nc_mat.set(1, 1.0, 10)
        with self.assertRaises(TypeError):
            nc_mat.set(1, 1, [1, 2, 3])

        # IndexError if i or j or both are out of range
        with self.assertRaises(IndexError):
            nc_mat.set(10, 1, 10)
        with self.assertRaises(IndexError):
            nc_mat.set(1, 10, 10)
        with self.assertRaises(IndexError):
            nc_mat.set(10, 10, 10)

    def test_set(self):
        pass
        # TODO: YOUR CODE HERE
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        rand_row = np.random.randint(dp_mat.shape[0])
        rand_col = np.random.randint(dp_mat.shape[1])
        self.assertEquals(round(dp_mat[rand_row][rand_col], decimal_places),
                          round(nc_mat[rand_row][rand_col], decimal_places))


class TestShape(TestCase):
    def test_shape(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        self.assertTrue(dp_mat.shape == nc_mat.shape)


class TestSubscript(TestCase):
    def test_1d_valid_access(self):
        _, nc_mat = dp_nc_matrix(1, 3, 1)
        _, nc_mat1 = dp_nc_matrix(3, 1, 2)

        # test single value access
        for i in range(nc_mat.shape[0]):
            self.assertEqual(nc_mat[i], 1)
            self.assertEqual(nc_mat1[i], 2)

        # test slice access
        cmp_dp_nc_matrix(nc.Matrix(1, 2, [1, 1]), nc_mat[0:2])
        cmp_dp_nc_matrix(nc.Matrix(1, 2, [2, 2]), nc_mat[0:2])
        self.assertEqual(nc_mat[0:1], 1)
        cmp_dp_nc_matrix(nc.Matrix(1, 2, [1, 1]), nc_mat[0:2:1])

    def test_1d_invalid_access(self):
        _, nc_mat = dp_nc_matrix(1, 3, 1)

        # raise TypeError if not an integer or a slice
        self.assertRaises(TypeError, lambda: nc_mat[1.0])
        self.assertRaises(TypeError, lambda: nc_mat[1, 1])
        self.assertRaises(TypeError, lambda: nc_mat[0:2, 0:2])

        # raise ValueError if slice step size != 1, or length of slice < 1
        self.assertRaises(ValueError, lambda: nc_mat[0:3:2])
        self.assertRaises(ValueError, lambda: nc_mat[0:0])

        # IndexError if index out of bounds
        self.assertRaises(IndexError, lambda: nc_mat[10])

    def test_2d_valid_access(self):
        _, nc_mat = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])

        # the key could be an integer, a single slice
        cmp_dp_nc_matrix(nc.Matrix([[4, 5, 6]]), nc_mat[1])
        cmp_dp_nc_matrix(nc.Matrix([[1, 2, 3], [4, 5, 6]]), nc_mat[0:2])

        # the key could be a tuple of two ints/slices
        self.assertEqual(nc_mat[1, 2], 6)
        cmp_dp_nc_matrix(nc.Matrix([[1, 2], [4, 5]]), nc_mat[0:2, 0:2])

        # return a number if the resulting slice is 1 by 1
        self.assertEqual(nc_mat[1][0], 4)
        self.assertEqual(nc_mat[1, 1], 5)
        self.assertEqual(nc_mat[0:1, 0:1], 1)

    def test_2d_invalid_access(self):
        _, nc_mat = dp_nc_matrix([[1, 2, 3], [4, 5, 6]])

        # TypeError if not an integer, a slice or a length-2 tuple of slices/ints
        self.assertRaises(TypeError, lambda: nc_mat[2.0])
        self.assertRaises(TypeError, lambda: nc_mat[1, 2, 3])
        self.assertRaises(TypeError, lambda: nc_mat[0:1, 1:2, 2:3])

        # ValueError if step size != 1, or length of slice < 1
        self.assertRaises(ValueError, lambda: nc_mat[0:3:2])
        self.assertRaises(ValueError, lambda: nc_mat[0:2:1, 0:3:2])
        self.assertRaises(ValueError, lambda: nc_mat[0:2:2, 0:3:1])
        self.assertRaises(ValueError, lambda: nc_mat[0:0, 0:1])
        self.assertRaises(ValueError, lambda: nc_mat[0:1, 1:1])

        # IndexError if key is an integer but out of range, or integer in tuple out of range
        self.assertRaises(IndexError, lambda: nc_mat[10])
        self.assertRaises(IndexError, lambda: nc_mat[1, 10])
        self.assertRaises(IndexError, lambda: nc_mat[10, 1])
        self.assertRaises(IndexError, lambda: nc_mat[10, 0:2])
        self.assertRaises(IndexError, lambda: nc_mat[0:2, 10])
        cmp_dp_nc_matrix(nc.Matrix([[4, 5, 6]]), nc_mat[1, 0:100])


class TestSetSubscript(TestCase):
    def test_1d_valid_set(self):
        _, nc_mat = dp_nc_matrix(1, 3, 1)

        # test single int key to set
        nc_mat[2] = 99
        cmp_dp_nc_matrix(nc.Matrix([[1, 1, 99]]), nc_mat)

        # test slice key to set
        nc_mat[0:2] = [99, 100]
        cmp_dp_nc_matrix(nc.Matrix([[99, 100, 1]]), nc_mat)
        nc_mat[0:1] = 101
        cmp_dp_nc_matrix(nc.Matrix([[101, 100, 1]]), nc_mat)
        nc_mat[1:3:1] = [77, 66]
        cmp_dp_nc_matrix(nc.Matrix([[99, 77, 66]]), nc_mat)
        nc_mat[1] = 99.0
        cmp_dp_nc_matrix(nc.Matrix([[99, 99, 66]]), nc_mat)

    def test_1d_invalid_set(self):
        _, nc_mat = dp_nc_matrix(1, 3, 1)

        # invalid keys for errors showed in subscript function
        # raise TypeError if not an integer or a slice
        with self.assertRaises(TypeError):
            nc_mat[1.0] = 10
        with self.assertRaises(TypeError):
            nc_mat[1, 1] = 10
        with self.assertRaises(TypeError):
            nc_mat[0:2, 0:2] = 10

        # raise ValueError if slice step size != 1, or length of slice < 1
        with self.assertRaises(ValueError):
            nc_mat[0:3:2] = [1, 1]
        with self.assertRaises(ValueError):
            nc_mat[0:0] = 10

        # IndexError if index out of bounds
        with self.assertRaises(IndexError):
            nc_mat[10] = 100

        # additional errors for set_subscript function
        # slice is 1 by 1, but v is not an int/float
        with self.assertRaises(TypeError):
            nc_mat[1] = [1, 2, 3]
        with self.assertRaises(TypeError):
            nc_mat[0:1] = [1, 2, 3]
        with self.assertRaises(TypeError):
            nc_mat[0:1:1] = [1, 2, 3]

        # slice is not 1 by 1, but v is not a list
        with self.assertRaises(TypeError):
            nc_mat[1:3] = 10

        # resulting slice is 1d,
        # but v has wrong length
        with self.assertRaises(ValueError):
            nc_mat[1:3] = [1, 2, 3]
        with self.assertRaises(ValueError):
            nc_mat[1:3] = [1]

        # but any elem of v is not int/float
        with self.assertRaises(ValueError):
            nc_mat[1:3] = [1, [1, 2, 3]]

    def test_2d_valid_set(self):
        _, nc_mat = dp_nc_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        # the key could be an integer, a single slice
        nc_mat[1] = [99, 100, 101]
        cmp_dp_nc_matrix(nc.Matrix([[1, 2, 3], [99, 100, 101], [7, 8, 9]]), nc_mat)
        nc_mat[0:2] = [[10, 11, 12], [13, 14, 15]]
        cmp_dp_nc_matrix(nc.Matrix([[10, 11, 12], [13, 14, 15], [7, 8, 9]]), nc_mat)

        # the key could be a tuple of two ints/slices
        nc_mat[1, 2] = 88
        cmp_dp_nc_matrix(nc.Matrix([[10, 11, 12], [13, 14, 88], [7, 8, 9]]), nc_mat)
        nc_mat[0:2, 0:2] = [[1, 2], [3, 4]]
        cmp_dp_nc_matrix(nc.Matrix([[1, 2, 12], [3, 4, 88], [7, 8, 9]]), nc_mat)
        nc_mat[1][0] = 99
        cmp_dp_nc_matrix(nc.Matrix([[1, 2, 12], [99, 4, 88], [7, 8, 9]]), nc_mat)
        nc_mat[0:1, 0:1] = 77
        cmp_dp_nc_matrix(nc.Matrix([[77, 2, 12], [99, 4, 88], [7, 8, 9]]), nc_mat)

        # check modifications to sliced mat will/won't show in original mat
        mat_slice = nc_mat[0]
        mat_slice[:] = [10, 10, 10]
        cmp_dp_nc_matrix(nc.Matrix([[10, 10, 10], [3, 4, 88], [7, 8, 9]]), nc_mat)

    def test_2d_invalid_set(self):
        _, nc_mat = dp_nc_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        # Invalid keys for error showed in subscript function
        # TypeError if not an integer, a slice or a length-2 tuple of slices/ints
        with self.assertRaises(TypeError):
            nc_mat[2.0] = 10
        with self.assertRaises(TypeError):
            nc_mat[1, 2, 3] = 10
        with self.assertRaises(TypeError):
            nc_mat[0:1, 1:2, 2:3] = 10

        # ValueError if step size != 1, or length of slice < 1
        with self.assertRaises(ValueError):
            nc_mat[0:3:2] = [1, 2]
        with self.assertRaises(ValueError):
            nc_mat[0:2:1, 0:3:2] = [[1, 2], [3, 4]]
        with self.assertRaises(ValueError):
            nc_mat[0:2:2, 0:3:1] = [[1, 2, 3]]
        with self.assertRaises(ValueError):
            nc_mat[0:0, 0:1] = 10
        with self.assertRaises(ValueError):
            nc_mat[0:1, 1:1] = 10

        # IndexError if key is an integer but out of range, or integer in tuple out of range
        with self.assertRaises(IndexError):
            nc_mat[10] = [1, 2, 3]
        with self.assertRaises(IndexError):
            nc_mat[1, 10] = 10
        with self.assertRaises(IndexError):
            nc_mat[10, 1] = 100
        with self.assertRaises(IndexError):
            nc_mat[10, 0:2] = [1, 2]
        with self.assertRaises(IndexError):
            nc_mat[0:2, 10] = [1, 2]
        nc_mat[1, 0:100] = [99, 100, 101]
        cmp_dp_nc_matrix(nc.Matrix([[1, 2, 3], [99, 100, 101], [7, 8, 9]]), nc_mat)

        # Additional errors for set_subscript function
        # Resulting slice is 1 by 1, but v is not a int/float
        with self.assertRaises(TypeError):
            nc_mat[1, 2] = [1, 2, 3]
        with self.assertRaises(TypeError):
            nc_mat[0:1, 0:1] = [1, 2, 3]

        # slice is not 1 by 1, but v is not a list
        with self.assertRaises(TypeError):
            nc_mat[1] = 1.0
        with self.assertRaises(TypeError):
            nc_mat[0:2, 0:2] = 10
        with self.assertRaises(TypeError):
            nc_mat[0:2, 1] = 10

        # resulting slice is 1d, but v has wrong length or not float/int elem
        with self.assertRaises(ValueError):
            nc_mat[1] = [0, 1, 2, 3, 4]
        with self.assertRaises(ValueError):
            nc_mat[1] = [0]
        with self.assertRaises(ValueError):
            nc_mat[1] = [0, 1, [1, 2, 3]]

        # resulting slice is 2d, but v has wrong length, or any elem of v has wrong length, or any elem of v includes
        # not float/int elem
        with self.assertRaises(ValueError):
            nc_mat[0:2, 0:2] = [[1, 2, 3]]
        with self.assertRaises(ValueError):
            nc_mat[0:2, 0:2] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        with self.assertRaises(ValueError):
            nc_mat[0:2, 0:2] = [[1], [1, 2, 3]]
        with self.assertRaises(ValueError):
            nc_mat[0:2, 0:2] = [[1, 2, 3, 4], [1, 2, 3]]
        with self.assertRaises(ValueError):
            nc_mat[0:2, 0:2] = [[1, 2, 3], [4]]
        with self.assertRaises(ValueError):
            nc_mat[0:2, 0:2] = [[1, 2, 3], [4, 5, 6, 7]]
        with self.assertRaises(ValueError):
            nc_mat[0:2, 0:2] = [[1, 2, 3], [1, 2, [1, 2, 3]]]
