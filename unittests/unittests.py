from utils import *
from unittest import TestCase

"""
For each operation, you should write tests to test  on matrices of different sizes.
Hint: use dp_mc_matrix to generate dumbpy and numc matrices with the same data and use
      cmp_dp_nc_matrix to compare the results
"""


class TestAdd(TestCase):
    def test_small_add(self):
        # TODO: YOUR CODE HERE
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(2, 2, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_medium_add(self):
        # TODO: YOUR CODE HERE
        pass

    def test_large_add(self):
        # TODO: YOUR CODE HERE
        pass


class TestSub(TestCase):
    def test_small_sub(self):
        # TODO: YOUR CODE HERE
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(2, 2, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_medium_sub(self):
        # TODO: YOUR CODE HERE
        pass

    def test_large_sub(self):
        # TODO: YOUR CODE HERE
        pass


class TestAbs(TestCase):
    def test_small_abs(self):
        # TODO: YOUR CODE HERE
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        is_correct, speed_up = compute([dp_mat], [nc_mat], "abs")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_medium_abs(self):
        # TODO: YOUR CODE HERE
        pass

    def test_large_abs(self):
        # TODO: YOUR CODE HERE
        pass


class TestNeg(TestCase):
    def test_small_neg(self):
        # TODO: YOUR CODE HERE
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        is_correct, speed_up = compute([dp_mat], [nc_mat], "neg")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_medium_neg(self):
        # TODO: YOUR CODE HERE
        pass

    def test_large_neg(self):
        # TODO: YOUR CODE HERE
        pass


class TestMul(TestCase):
    def test_small_mul(self):
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
    def test_small_pow(self):
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
        # TODO: YOUR CODE HERE
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        rand_row = np.random.randint(dp_mat.shape[0])
        rand_col = np.random.randint(dp_mat.shape[1])
        self.assertEqual(round(dp_mat[rand_row][rand_col], decimal_places),
                         round(nc_mat[rand_row][rand_col], decimal_places))


class TestSet(TestCase):
    def test_set(self):
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
        slice_nc_mat = nc_mat[0:2]
        cmp_dp_nc_matrix(nc.Matrix(1, 2, [1, 1]), slice_nc_mat)
        slice_nc_mat1 = nc_mat1[0:2]
        cmp_dp_nc_matrix(nc.Matrix(1, 2, [2, 2]), slice_nc_mat1)

        # check modification to sliced mat shows in original mat
        # slice_nc_mat[0] = 10
        # self.assertEqual(nc_mat[0], 10)

    def test_1d_invalid_access(self):
        _, nc_mat = dp_nc_matrix(1, 3, 1)

        # raise TypeError if not an integer or a slice
        self.assertRaises(TypeError, lambda: nc_mat[1.0])
        self.assertRaises(TypeError, lambda: nc_mat[1, 1])
        self.assertRaises(TypeError, lambda: nc_mat[0:2, 0:2])

        # raise ValueError if slice step size != 1, or length of slice < 1
        self.assertEquals(nc.Matrix(1, 2, [1, 1]), nc_mat[0:2:1])
        self.assertRaises(ValueError, lambda: nc_mat[0:3:2])
        self.assertRaises(ValueError, lambda: nc_mat[0:0])

        # IndexError if index out of bounds
        self.assertRaises(IndexError, lambda: nc_mat[10])

    def test_2d_valid_access(self):
        dp_mat, nc_mat = dp_nc_matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        rand_row = np.random.randint(nc_mat.shape[0])
        rand_col = np.random.randint(nc_mat.shape[1])

        # the key could be an integer, a single slice
        cmp_dp_nc_matrix(dp_mat[rand_row], nc_mat[rand_row])
        cmp_dp_nc_matrix(dp_mat[0:rand_row], nc_mat[0:rand_row])

        # the key could be a tuple of two ints/slices
        self.assertEquals(dp_mat[rand_row, rand_col], nc_mat[rand_row, rand_col])
        cmp_dp_nc_matrix(dp_mat[0:2, 0:2], nc_mat[0:2, 0:2])

        # check modifications to sliced mat will/won't show in original mat
        # nc_mat[0] = [10, 10, 10]
        # cmp_dp_nc_matrix(nc.Matrix(2, 3, [[10, 10, 10], [4, 5, 6]]), nc_mat)
        # nc_mat[0][0] = 100
        # cmp_dp_nc_matrix(nc.Matrix(2, 3, [[10, 10, 10], [4, 5, 6]]), nc_mat)

        # return a number if the resulting slice is 1 by 1
        self.assertEquals(nc_mat[1][0], 4)
        self.assertEquals(nc_mat[1, 1], 5)
        self.assertEquals(nc_mat[0:1, 0:1], 4)

    def test_2d_invalid_access(self):
        dp_mat, nc_mat = dp_nc_matrix(2, 3, [[1, 2, 3], [4, 5, 6]])

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
        cmp_dp_nc_matrix(dp_mat[1, 0:100], nc_mat[1, 0:100])



