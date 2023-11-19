#include "numc.h"
#include <structmember.h>

PyTypeObject Matrix61cType;

/* Helper functions for initalization of matrices and vectors */

/*
 * Return a tuple given rows and cols
 */
PyObject *get_shape(int rows, int cols) {
  if (rows == 1 || cols == 1) {
    return PyTuple_Pack(1, PyLong_FromLong(rows * cols));
  } else {
    return PyTuple_Pack(2, PyLong_FromLong(rows), PyLong_FromLong(cols));
  }
}
/*
 * Matrix(rows, cols, low, high). Fill a matrix random double values
 */
int init_rand(PyObject *self, int rows, int cols, unsigned int seed, double low,
              double high) {
    matrix *new_mat;
    int alloc_failed = allocate_matrix(&new_mat, rows, cols);
    if (alloc_failed) return alloc_failed;
    rand_matrix(new_mat, seed, low, high);
    ((Matrix61c *)self)->mat = new_mat;
    ((Matrix61c *)self)->shape = get_shape(new_mat->rows, new_mat->cols);
    return 0;
}

/*
 * Matrix(rows, cols, val). Fill a matrix of dimension rows * cols with val
 */
int init_fill(PyObject *self, int rows, int cols, double val) {
    matrix *new_mat;
    int alloc_failed = allocate_matrix(&new_mat, rows, cols);
    if (alloc_failed)
        return alloc_failed;
    else {
        fill_matrix(new_mat, val);
        ((Matrix61c *)self)->mat = new_mat;
        ((Matrix61c *)self)->shape = get_shape(new_mat->rows, new_mat->cols);
    }
    return 0;
}

/*
 * Matrix(rows, cols, 1d_list). Fill a matrix with dimension rows * cols with 1d_list values
 */
int init_1d(PyObject *self, int rows, int cols, PyObject *lst) {
    if (rows * cols != PyList_Size(lst)) {
        PyErr_SetString(PyExc_ValueError, "Incorrect number of elements in list");
        return -1;
    }
    matrix *new_mat;
    int alloc_failed = allocate_matrix(&new_mat, rows, cols);
    if (alloc_failed) return alloc_failed;
    int count = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            set(new_mat, i, j, PyFloat_AsDouble(PyList_GetItem(lst, count)));
            count++;
        }
    }
    ((Matrix61c *)self)->mat = new_mat;
    ((Matrix61c *)self)->shape = get_shape(new_mat->rows, new_mat->cols);
    return 0;
}

/*
 * Matrix(2d_list). Fill a matrix with dimension len(2d_list) * len(2d_list[0])
 */
int init_2d(PyObject *self, PyObject *lst) {
    int rows = PyList_Size(lst);
    if (rows == 0) {
        PyErr_SetString(PyExc_ValueError,
                        "Cannot initialize numc.Matrix with an empty list");
        return -1;
    }
    int cols;
    if (!PyList_Check(PyList_GetItem(lst, 0))) {
        PyErr_SetString(PyExc_ValueError, "List values not valid");
        return -1;
    } else {
        cols = PyList_Size(PyList_GetItem(lst, 0));
    }
    for (int i = 0; i < rows; i++) {
        if (!PyList_Check(PyList_GetItem(lst, i)) ||
                PyList_Size(PyList_GetItem(lst, i)) != cols) {
            PyErr_SetString(PyExc_ValueError, "List values not valid");
            return -1;
        }
    }
    matrix *new_mat;
    int alloc_failed = allocate_matrix(&new_mat, rows, cols);
    if (alloc_failed) return alloc_failed;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            set(new_mat, i, j,
                PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(lst, i), j)));
        }
    }
    ((Matrix61c *)self)->mat = new_mat;
    ((Matrix61c *)self)->shape = get_shape(new_mat->rows, new_mat->cols);
    return 0;
}

/*
 * This deallocation function is called when reference count is 0
 */
void Matrix61c_dealloc(Matrix61c *self) {
    deallocate_matrix(self->mat);
    Py_TYPE(self)->tp_free(self);
}

/* For immutable types all initializations should take place in tp_new */
PyObject *Matrix61c_new(PyTypeObject *type, PyObject *args,
                        PyObject *kwds) {
    /* size of allocated memory is tp_basicsize + nitems*tp_itemsize*/
    Matrix61c *self = (Matrix61c *)type->tp_alloc(type, 0);
    return (PyObject *)self;
}

/*
 * This matrix61c type is mutable, so needs init function. Return 0 on success otherwise -1
 */
int Matrix61c_init(PyObject *self, PyObject *args, PyObject *kwds) {
    /* Generate random matrices */
    if (kwds != NULL) {
        PyObject *rand = PyDict_GetItemString(kwds, "rand");
        if (!rand) {
            PyErr_SetString(PyExc_TypeError, "Invalid arguments");
            return -1;
        }
        if (!PyBool_Check(rand)) {
            PyErr_SetString(PyExc_TypeError, "Invalid arguments");
            return -1;
        }
        if (rand != Py_True) {
            PyErr_SetString(PyExc_TypeError, "Invalid arguments");
            return -1;
        }

        PyObject *low = PyDict_GetItemString(kwds, "low");
        PyObject *high = PyDict_GetItemString(kwds, "high");
        PyObject *seed = PyDict_GetItemString(kwds, "seed");
        double double_low = 0;
        double double_high = 1;
        unsigned int unsigned_seed = 0;

        if (low) {
            if (PyFloat_Check(low)) {
                double_low = PyFloat_AsDouble(low);
            } else if (PyLong_Check(low)) {
                double_low = PyLong_AsLong(low);
            }
        }

        if (high) {
            if (PyFloat_Check(high)) {
                double_high = PyFloat_AsDouble(high);
            } else if (PyLong_Check(high)) {
                double_high = PyLong_AsLong(high);
            }
        }

        if (double_low >= double_high) {
            PyErr_SetString(PyExc_TypeError, "Invalid arguments");
            return -1;
        }

        // Set seed if argument exists
        if (seed) {
            if (PyLong_Check(seed)) {
                unsigned_seed = PyLong_AsUnsignedLong(seed);
            }
        }

        PyObject *rows = NULL;
        PyObject *cols = NULL;
        if (PyArg_UnpackTuple(args, "args", 2, 2, &rows, &cols)) {
            if (rows && cols && PyLong_Check(rows) && PyLong_Check(cols)) {
                return init_rand(self, PyLong_AsLong(rows), PyLong_AsLong(cols), unsigned_seed, double_low,
                                 double_high);
            }
        } else {
            PyErr_SetString(PyExc_TypeError, "Invalid arguments");
            return -1;
        }
    }
    PyObject *arg1 = NULL;
    PyObject *arg2 = NULL;
    PyObject *arg3 = NULL;
    if (PyArg_UnpackTuple(args, "args", 1, 3, &arg1, &arg2, &arg3)) {
        /* arguments are (rows, cols, val) */
        if (arg1 && arg2 && arg3 && PyLong_Check(arg1) && PyLong_Check(arg2) && (PyLong_Check(arg3)
                || PyFloat_Check(arg3))) {
            if (PyLong_Check(arg3)) {
                return init_fill(self, PyLong_AsLong(arg1), PyLong_AsLong(arg2), PyLong_AsLong(arg3));
            } else
                return init_fill(self, PyLong_AsLong(arg1), PyLong_AsLong(arg2), PyFloat_AsDouble(arg3));
        } else if (arg1 && arg2 && arg3 && PyLong_Check(arg1) && PyLong_Check(arg2) && PyList_Check(arg3)) {
            /* Matrix(rows, cols, 1D list) */
            return init_1d(self, PyLong_AsLong(arg1), PyLong_AsLong(arg2), arg3);
        } else if (arg1 && PyList_Check(arg1) && arg2 == NULL && arg3 == NULL) {
            /* Matrix(rows, cols, 1D list) */
            return init_2d(self, arg1);
        } else if (arg1 && arg2 && PyLong_Check(arg1) && PyLong_Check(arg2) && arg3 == NULL) {
            /* Matrix(rows, cols, 1D list) */
            return init_fill(self, PyLong_AsLong(arg1), PyLong_AsLong(arg2), 0);
        } else {
            PyErr_SetString(PyExc_TypeError, "Invalid arguments");
            return -1;
        }
    } else {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return -1;
    }
}

/*
 * List of lists representations for matrices
 */
PyObject *Matrix61c_to_list(Matrix61c *self) {
    int rows = self->mat->rows;
    int cols = self->mat->cols;
    PyObject *py_lst = NULL;
    if (self->mat->is_1d) {  // If 1D matrix, print as a single list
        py_lst = PyList_New(rows * cols);
        int count = 0;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                PyList_SetItem(py_lst, count, PyFloat_FromDouble(get(self->mat, i, j)));
                count++;
            }
        }
    } else {  // if 2D, print as nested list
        py_lst = PyList_New(rows);
        for (int i = 0; i < rows; i++) {
            PyList_SetItem(py_lst, i, PyList_New(cols));
            PyObject *curr_row = PyList_GetItem(py_lst, i);
            for (int j = 0; j < cols; j++) {
                PyList_SetItem(curr_row, j, PyFloat_FromDouble(get(self->mat, i, j)));
            }
        }
    }
    return py_lst;
}

PyObject *Matrix61c_class_to_list(Matrix61c *self, PyObject *args) {
    PyObject *mat = NULL;
    if (PyArg_UnpackTuple(args, "args", 1, 1, &mat)) {
        if (!PyObject_TypeCheck(mat, &Matrix61cType)) {
            PyErr_SetString(PyExc_TypeError, "Argument must of type numc.Matrix!");
            return NULL;
        }
        Matrix61c* mat61c = (Matrix61c*)mat;
        return Matrix61c_to_list(mat61c);
    } else {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }
}

/*
 * Add class methods
 */
PyMethodDef Matrix61c_class_methods[] = {
    {"to_list", (PyCFunction)Matrix61c_class_to_list, METH_VARARGS, "Returns a list representation of numc.Matrix"},
    {NULL, NULL, 0, NULL}
};

/*
 * Matrix61c string representation. For printing purposes.
 */
PyObject *Matrix61c_repr(PyObject *self) {
    PyObject *py_lst = Matrix61c_to_list((Matrix61c *)self);
    return PyObject_Repr(py_lst);
}

/* NUMBER METHODS */

/*
 * Add the second numc.Matrix (Matrix61c) object to the first one. The first operand is
 * self, and the second operand can be obtained by casting `args`.
 */
PyObject *Matrix61c_add(Matrix61c* self, PyObject* args) {
    PyObject *mat = NULL;
    if (PyArg_UnpackTuple(args, "args", 1, 1, &mat)) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }
    if (!PyObject_TypeCheck(mat, &Matrix61cType)) {
        PyErr_SetString(PyExc_TypeError, "Argument must of type numc.Matrix!");
        return NULL;
    }
    Matrix61c *mat61c = (Matrix61c *) mat;

    Matrix61c *result = (Matrix61c *) Matrix61c_new(&Matrix61cType, NULL, NULL);
    matrix *result_mat = NULL;
    int alloc_failed = allocate_matrix(&result_mat, self->mat->rows, self->mat->cols);
    if (alloc_failed) {
        PyErr_SetString(PyExc_RuntimeError, "Alloc failed");
        return NULL;
    }

    int error_code = add_matrix(result_mat, self->mat, mat61c->mat);
    if (error_code != 0) {
        free(result_mat);
        if (error_code == -2) {
            PyErr_SetString(PyExc_ValueError, "Matrices have different dimensions");
        } else if (error_code == -3) {
            PyErr_SetString(PyExc_RuntimeError, "Internal Error: result matrix dimension not match");
        }
        return NULL;
    }

    result->mat = result_mat;
    result->shape = self->shape;
    return (PyObject *) result;
}

/*
 * Substract the second numc.Matrix (Matrix61c) object from the first one. The first operand is
 * self, and the second operand can be obtained by casting `args`.
 */
PyObject *Matrix61c_sub(Matrix61c* self, PyObject* args) {
    PyObject *mat = NULL;
    if (PyArg_UnpackTuple(args, "args", 1, 1, &mat)) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }
    if (!PyObject_TypeCheck(mat, &Matrix61cType)) {
        PyErr_SetString(PyExc_TypeError, "Argument must of type numc.Matrix!");
        return NULL;
    }
    Matrix61c *mat61c = (Matrix61c *) mat;

    Matrix61c *result = (Matrix61c *) Matrix61c_new(&Matrix61cType, NULL, NULL);
    matrix *result_mat = NULL;
    int alloc_failed = allocate_matrix(&result_mat, self->mat->rows, self->mat->cols);
    if (alloc_failed) {
        PyErr_SetString(PyExc_RuntimeError, "Alloc failed");
        return NULL;
    }

    int error_code = sub_matrix(result_mat, self->mat, mat61c->mat);
    if (error_code != 0) {
        free(result_mat);
        if (error_code == -2) {
            PyErr_SetString(PyExc_ValueError, "Matrices have different dimensions!");
        } else if (error_code == -3) {
            PyErr_SetString(PyExc_RuntimeError, "Internal Error: result matrix dimension not match");
        }
        return NULL;
    }

    result->mat = result_mat;
    result->shape = self->shape;
    return (PyObject *) result;
}

/*
 * NOT element-wise multiplication. The first operand is self, and the second operand
 * can be obtained by casting `args`.
 */
PyObject *Matrix61c_multiply(Matrix61c* self, PyObject *args) {
    PyObject *mat = NULL;
    if (PyArg_UnpackTuple(args, "args", 1, 1, &mat)) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }
    if (!PyObject_TypeCheck(mat, &Matrix61cType)) {
        PyErr_SetString(PyExc_TypeError, "Argument must of type numc.Matrix!");
        return NULL;
    }
    Matrix61c *mat61c = (Matrix61c *) mat;

    Matrix61c *result = (Matrix61c *) Matrix61c_new(&Matrix61cType, NULL, NULL);
    matrix *result_mat = NULL;
    int alloc_failed = allocate_matrix(&result_mat, self->mat->rows, self->mat->cols);
    if (alloc_failed) {
        PyErr_SetString(PyExc_RuntimeError, "Alloc failed");
        return NULL;
    }

    int error_code = mul_matrix(result_mat, self->mat, mat61c->mat);
    if (error_code != 0) {
        free(result_mat);
        if (error_code == -2) {
            PyErr_SetString(PyExc_ValueError, "matrices dimension not match");
        } else if (error_code == -3) {
            PyErr_SetString(PyExc_RuntimeError, "Internal Error: result matrix dimension not match");
        }
        return NULL;
    }

    result->mat = result_mat;
    result->shape = get_shape(result_mat->rows, result_mat->cols);
    return (PyObject *) result;
}

/*
 * Negates the given numc.Matrix.
 */
PyObject *Matrix61c_neg(Matrix61c* self) {
    Matrix61c *result = (Matrix61c *) Matrix61c_new(&Matrix61cType, NULL, NULL);
    matrix *result_mat = NULL;
    int alloc_failed = allocate_matrix(&result_mat, self->mat->rows, self->mat->cols);
    if (alloc_failed) {
        PyErr_SetString(PyExc_RuntimeError, "Alloc failed");
        return NULL;
    }

    int error_code = neg_matrix(result_mat, self->mat);
    if (error_code == -2) {
        free(result_mat);
        PyErr_SetString(PyExc_RuntimeError, "Internal error: Result matrix dimension not match");
        return NULL;
    }
    result->mat = result_mat;
    result->shape = self->shape;
    return (PyObject *) result;
}

/*
 * Take the element-wise absolute value of this numc.Matrix.
 */
PyObject *Matrix61c_abs(Matrix61c *self) {
    Matrix61c *result = (Matrix61c *) Matrix61c_new(&Matrix61cType, NULL, NULL);
    matrix *result_mat = NULL;
    int alloc_failed = allocate_matrix(&result_mat, self->mat->rows, self->mat->cols);
    if (alloc_failed) {
        PyErr_SetString(PyExc_RuntimeError, "Alloc failed");
        return NULL;
    }

    int error_code = abs_matrix(result_mat, self->mat);
    if (error_code == -2) {
        free(result_mat);
        PyErr_SetString(PyExc_RuntimeError, "Internal error: Result matrix dimension not match");
        return NULL;
    }
    result->mat = result_mat;
    result->shape = self->shape;
    return (PyObject *) result;
}

/*
 * Raise numc.Matrix (Matrix61c) to the `pow`th power. You can ignore the argument `optional`.
 */
PyObject *Matrix61c_pow(Matrix61c *self, PyObject *pow, PyObject *optional) {
    if (!PyLong_Check(pow)) {
        PyErr_SetString(PyExc_TypeError, "Invalid value for argument pow");
        return NULL;
    }
    int pow_num = (int) PyLong_AsLong(pow);

    Matrix61c *result = (Matrix61c *) Matrix61c_new(&Matrix61cType, NULL, NULL);
    matrix *mat = NULL;
    int alloc_failed = allocate_matrix(&mat, self->mat->rows, self->mat->cols);
    if (alloc_failed) {
        PyErr_SetString(PyExc_RuntimeError, "Internal error, doing abs failed");
        return NULL;
    }

    int error_code = pow_matrix(mat, self->mat, pow_num);
    if (error_code != 0) {
        free(mat);
        if (error_code == -2) {
            PyErr_SetString(PyExc_ValueError, "pow is negative or the matrix is not a square matrix");
        } else if (error_code == -3) {
            PyErr_SetString(PyExc_RuntimeError, "Internal Error: result matrix dimension not match");
        }
        return NULL;
    }

    result->mat = mat;
    result->shape = self->shape;
    return (PyObject *) result;
}

/*
 * Create a PyNumberMethods struct for overloading operators with all the number methods you have
 * define. You might find this link helpful: https://docs.python.org/3.6/c-api/typeobj.html
 */
PyNumberMethods Matrix61c_as_number = {
        (binaryfunc) Matrix61c_add,
        (binaryfunc) Matrix61c_sub,
        (binaryfunc) Matrix61c_multiply,
        NULL, NULL,
        (ternaryfunc) Matrix61c_pow,
        (unaryfunc) Matrix61c_neg,
        NULL,
        (unaryfunc) Matrix61c_abs,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
};


/* INSTANCE METHODS */

/*
 * Given a numc.Matrix self, parse `args` to (int) row, (int) col, and (double/int) val.
 * Return None in Python (this is different from returning null).
 */
PyObject *Matrix61c_set_value(Matrix61c *self, PyObject* args) {
    PyObject *row = NULL;
    PyObject *col = NULL;
    PyObject *val = NULL;
    if (PyArg_UnpackTuple(args, "args", 3, 3, &row, &col, &val) ||
        !(row && col && val && PyLong_Check(row) && PyLong_Check(col) &&
        (PyLong_Check(val) || PyFloat_Check(val)))) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }
    int i = (int) PyLong_AsLong(row);
    int j = (int) PyLong_AsLong(col);
    double val_c = (double) PyFloat_AsDouble(val);

    int rows = self->mat->rows;
    int cols = self->mat->cols;
    if (i >= rows || j >= cols) {
        PyErr_SetString(PyExc_IndexError, "i or j or both out of bounds");
        return NULL;
    }

    set(self->mat, i, j, val_c);
    return Py_None;
}

/*
 * Given a numc.Matrix `self`, parse `args` to (int) row and (int) col.
 * Return the value at the `row`th row and `col`th column, which is a Python
 * float/int.
 */
PyObject *Matrix61c_get_value(Matrix61c *self, PyObject* args) {
    PyObject *row = NULL;
    PyObject *col = NULL;
    if (PyArg_UnpackTuple(args, "args", 2, 2, &row, &col) ||
        !(row && col) ||
        !(PyLong_Check(row) && PyLong_Check(col))) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }
    int i = (int) PyLong_AsLong(row);
    int j = (int) PyLong_AsLong(col);

    int rows = self->mat->rows;
    int cols = self->mat->cols;
    if (i >= rows || j >= cols) {
        PyErr_SetString(PyExc_IndexError, "i or j or both out of bounds");
        return NULL;
    }

    return PyFloat_FromDouble(get(self->mat, i, j));
}

/*
 * Create an array of PyMethodDef structs to hold the instance methods.
 * Name the python function corresponding to Matrix61c_get_value as "get" and Matrix61c_set_value
 * as "set"
 * You might find this link helpful: https://docs.python.org/3.6/c-api/structures.html
 */
PyMethodDef Matrix61c_methods[] = {
    {"set", (PyCFunction) Matrix61c_set_value, METH_VARARGS, "set value at specified position row(i) and col(j)"},
    {"get", (PyCFunction) Matrix61c_get_value, METH_VARARGS, "get value at specified position with row(i) and col(j)"},
        {NULL, NULL, 0, NULL} // sentinel indicating the end of the method table
};

/* INDEXING */

/*
 * Helper function: if a index has two possible types, integer or slice, change it to one type(slice)
 * for convenience.
*/
PyObject *convert_to_slice(PyObject *index) {
    if (PyLong_Check(index)) {
        PyObject *start = index;
        PyObject *stop = PyNumber_Add(index, PyLong_FromLong(1));
        PyObject *step = PyLong_FromLong(1);
        return PySlice_New(start, stop, step);
    }
    return index;
}

/*
 * Helper function, to check whether the slice or ints in key are valid
 */
int check_keys(Matrix61c *self, PyObject *key, PyObject **index, PyObject **index1) {
    // if key is a single int or a single slice
    if (PyLong_Check(key) || PySlice_Check(key)) {
        *index = key;
        return 0;
    }
    // if key is a tuple, only 2d-matrix is valid
    if (PyTuple_Check(key) && !self->mat->is_1d) {
        if (PyArg_UnpackTuple(key, "key", 1, 2, index, index1) &&
            index && index1 &&
            ((PyLong_Check(index) || PySlice_Check(index)) && ((PyLong_Check(index1) || PySlice_Check(index1))))) {
            return 0;
        }
    }
    // other situations are invalid
    PyErr_SetString(PyExc_TypeError, "Invalid arguments");
    return -1;
}

/*
 * Helper function, to extract info from slices and check their validation
 */
int extract_slice(PyObject *slice, Py_ssize_t length,
    Py_ssize_t *start, Py_ssize_t *stop, Py_ssize_t *step, Py_ssize_t *slice_length) {
    if (PySlice_GetIndicesEx(slice, length, start, stop, step, slice_length)) {
        PyErr_SetString(PyExc_RuntimeError, "Internal error: get indices from slice failed");
        return -1;
    }
    if (*step > 1 || *slice_length < 1) {
        PyErr_SetString(PyExc_ValueError, "Slice info not valid");
        return -1;
    }
    return 0;
}

/* Helper function, to create a new Matrix from slice */
PyObject *matrix61c_from_slice(PyObject* slice, PyObject *slice1, Matrix61c *source) {
    Matrix61c *result = (Matrix61c *) Matrix61c_new(&Matrix61cType, NULL, NULL);
    Py_ssize_t start = 0, stop = 0, step = 0, length = source->mat->rows, slice_length = 0;
    Py_ssize_t start1 = 0, stop1 = 0, step1 = 0, length1 = source->mat->cols, slice_length1 = 0;

    // extract slice
    int extract_failed = extract_slice(slice, length, &start, &stop, &step, &slice_length) ||
            extract_slice(slice1, length1, &start1, &stop1, &step1, &slice_length1);
    if (extract_failed) {
        return NULL;
    }

    int alloc_failed = allocate_matrix_ref(&(result->mat), source->mat,
        (int) start, (int) start1, (int) slice_length, (int) slice_length1);
    if (alloc_failed) {
        PyErr_SetString(PyExc_RuntimeError, "Slice failed: can't allocate ref matrix");
        return NULL;
    }
    result->shape = get_shape((int) slice_length, (int) slice_length1);

    return (PyObject *) result;
}

/*
 * Given a numc.Matrix `self`, index into it with `key`. Return the indexed result.
 */
PyObject *Matrix61c_subscript(Matrix61c* self, PyObject* key) {
    PyObject *index = NULL;
    PyObject *index1 = NULL;
    if (check_keys(self, key, &index, &index1)) {
        return NULL;
    }

    PyObject *row_slice = NULL;
    PyObject *col_slice = NULL;
    // if only one index
    if (index1 == NULL) {
        // 1d matrix
        if (self->mat->is_1d) {
            if (PyLong_Check(index)) {
                int value = (int) PyLong_AsLong(index);
                if (self->mat->rows == 1) {
                    return PyFloat_FromDouble(self->mat->data[0][value]);
                }
                return PyFloat_FromDouble(self->mat->data[value][0]);
            }
            if (self->mat->rows == 1) {
                row_slice = PySlice_New(PyLong_FromLong(0), PyLong_FromLong(1), PyLong_FromLong(1));
                col_slice = index;
            } else {
                row_slice = index;
                col_slice = PySlice_New(PyLong_FromLong(0), PyLong_FromLong(1), PyLong_FromLong(1));
            }
        } else {
        // 2d matrix
            if (PyLong_Check(index)) {
                int value = (int) PyLong_AsLong(index);
                row_slice = PySlice_New(PyLong_FromLong(value), PyLong_FromLong(value + 1), PyLong_FromLong(1));
            } else {
                row_slice = index;
            }
            col_slice = PySlice_New(PyLong_FromLong(0), PyLong_FromLong(self->mat->cols), PyLong_FromLong(1));
        }
    } else {
        // if two indexes
        row_slice = PyLong_Check(index) ? convert_to_slice(index) : index;
        col_slice = PyLong_Check(index1) ? convert_to_slice(index1) : index1;
    }

    return matrix61c_from_slice(row_slice, col_slice, self);
}

/*
 * Given a numc.Matrix `self`, index into it with `key`, and set the indexed result to `v`.
 */
int Matrix61c_set_subscript(Matrix61c* self, PyObject *key, PyObject *v) {
    PyObject *index = NULL;
    PyObject *index1 = NULL;
    if (check_keys(self, key, &index, &index1)) {
        return -1;
    }

    // if the args are integers, convert to slice for uniform operation
    PyObject *slice = convert_to_slice(index);
    PyObject *slice1 = NULL;
    if (!index1) {
        slice1 = convert_to_slice(index1);
    }

    Py_ssize_t start = 0, stop = 0, step = 0, length = 0, slice_length = 0;
    Py_ssize_t start1 = 0, stop1 = 0, step1 = 0, length1 = 0, slice_length1 = 0;

    if (self->mat->is_1d) {
        length = self->mat->rows > 1 ? self->mat->rows + 1 : self->mat->cols + 1;
        // if index is an integer, just need to set the value
        if (PyLong_Check(index)) {
            int value = (int) PyLong_AsLong(index);
            if (value >= length) {
                PyErr_SetString(PyExc_IndexError, "Index out of bounds");
                return -1;
            }
            if (!PyFloat_Check(v)) {
                PyErr_SetString(PyExc_TypeError, "v is not valid for 1D matrix with an integer to index");
                return -1;
            }
            set(self->mat, 0, value, PyFloat_AsDouble(v));
            return 0;
        }

        // if not, should set a list of value
        if (extract_slice(slice, length, &start, &stop, &step, &slice_length)) {
            if (!PyList_Check(v)) {
                PyErr_SetString(PyExc_TypeError, "v is not valid for 1D matrix with a slice");
                return -1;
            }

            if (length != PyList_Size(v)) {
                PyErr_SetString(PyExc_ValueError, "v has wrong length");
            }
            for (int i = 0; i < PyList_Size(v); ++i) {
                PyObject *item = PyList_GetItem(v, (Py_ssize_t) i);
                if (!(PyLong_Check(item) || PyFloat_Check(item))) {
                    PyErr_SetString(PyExc_ValueError, "some element of v is not a float or int");
                    return -1;
                }
            }

            for (Py_ssize_t i = start; i < stop; i += step) {
                set(self->mat, 0, (int) i, PyFloat_AsDouble(PyList_GetItem(v, i)));
            }
            return 0;
        }
    } else {
        length = self->mat->rows + 1;
        length1 = self->mat->cols + 1;
        // if two index are integer, just set the value
        if (PyLong_Check(index) && PyLong_Check(index1)) {
            int row = (int) PyLong_AsLong(index);
            int col = (int) PyLong_AsLong(index1);
            if (row >= length || col > length1) {
                PyErr_SetString(PyExc_IndexError, "Index out of bounds");
            }
            if (!PyFloat_Check(v)) {
                PyErr_SetString(PyExc_TypeError, "v is not valid for 2D matrix with two integers");
                return -1;
            }
            set(self->mat, (int) row, (int) col, PyFloat_AsDouble(v));
            return 0;
        }

        // if not, should return a new matrix which inherits part of its parent's data
        if (extract_slice(slice, length, &start, &stop, &step, &slice_length) ||
            extract_slice(slice1, length1, &start1, &stop1, &step1, &slice_length1)) {
            if (slice_length == 1 && slice_length1 == 1) {
                if (!(PyLong_Check(v) || PyFloat_Check(v))) {
                    PyErr_SetString(PyExc_TypeError, "v is not valid for 1 by 1 slice");
                    return -1;
                }
            } else {
                if (!PyList_Check(v)) {
                    PyErr_SetString(PyExc_TypeError, "v is not valid for not 1 by 1 slice");
                    return -1;
                }
            }

            if (length == 1) {
                if (length1 != PyList_Size(v)) {
                    PyErr_SetString(PyExc_ValueError, "v has the wrong length");
                }
                for (int i = 0; i < PyList_Size(v); ++i) {
                    PyObject *item = PyList_GetItem(v, (Py_ssize_t) i);
                    if (!(PyLong_Check(item) || PyFloat_Check(item))) {
                        PyErr_SetString(PyExc_ValueError, "some element of v is not a float or int");
                        return -1;
                    }
                }
            } else {
                if (length != PyList_Size(v)) {
                    PyErr_SetString(PyExc_TypeError, "v has wrong number of items");
                }
                for (int i = 0; i < PyList_Size(v); ++i) {
                    PyObject *item_list = PyList_GetItem(v, (Py_ssize_t) i);
                    if (length1 != PyList_Size(item_list) || !PyList_Check(item_list)) {
                        PyErr_SetString(PyExc_ValueError, "v has wrong number of items or is not a list");
                    }
                    for (int j = 0; j < PyList_Size(item_list); ++j) {
                        PyObject *item = PyList_GetItem(item_list, (Py_ssize_t) j);
                        if (!PyLong_Check(item) || PyFloat_Check(item)) {
                            PyErr_SetString(PyExc_ValueError, "some element of v is not a float or int");
                            return -1;
                        }
                    }
                }
            }

            for (Py_ssize_t i = start; i < stop; i += step) {
                for (Py_ssize_t j = start1; j < stop; j += step1) {
                    set(self->mat, (int) i, (int) j,
                        PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(v, (Py_ssize_t) i), (Py_ssize_t) j)));
                }
            }
        }
    }
    return 0;
}

PyMappingMethods Matrix61c_mapping = {
    NULL,
    (binaryfunc) Matrix61c_subscript,
    (objobjargproc) Matrix61c_set_subscript,
};

/* INSTANCE ATTRIBUTES*/
PyMemberDef Matrix61c_members[] = {
    {
        "shape", T_OBJECT_EX, offsetof(Matrix61c, shape), 0,
        "(rows, cols)"
    },
    {NULL}  /* Sentinel */
};

PyTypeObject Matrix61cType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "numc.Matrix",
    .tp_basicsize = sizeof(Matrix61c),
    .tp_dealloc = (destructor)Matrix61c_dealloc,
    .tp_repr = (reprfunc)Matrix61c_repr,
    .tp_as_number = &Matrix61c_as_number,
    .tp_flags = Py_TPFLAGS_DEFAULT |
    Py_TPFLAGS_BASETYPE,
    .tp_doc = "numc.Matrix objects",
    .tp_methods = Matrix61c_methods,
    .tp_members = Matrix61c_members,
    .tp_as_mapping = &Matrix61c_mapping,
    .tp_init = (initproc)Matrix61c_init,
    .tp_new = Matrix61c_new
};


struct PyModuleDef numcmodule = {
    PyModuleDef_HEAD_INIT,
    "numc",
    "Numc matrix operations",
    -1,
    Matrix61c_class_methods
};

/* Initialize the numc module */
PyMODINIT_FUNC PyInit_numc(void) {
    PyObject* m;

    if (PyType_Ready(&Matrix61cType) < 0)
        return NULL;

    m = PyModule_Create(&numcmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&Matrix61cType);
    PyModule_AddObject(m, "Matrix", (PyObject *)&Matrix61cType);
    printf("CS61C Fall 2020 Project 4: numc imported!\n");
    fflush(stdout);
    return m;
}