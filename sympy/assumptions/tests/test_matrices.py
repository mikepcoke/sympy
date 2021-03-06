from sympy import Q, ask
from sympy.matrices.expressions import (MatrixSymbol, Identity, ZeroMatrix,
        Trace, MatrixSlice, Determinant)
from sympy.utilities.pytest import XFAIL
from sympy.assumptions import assuming

X = MatrixSymbol('X', 2, 2)
Y = MatrixSymbol('Y', 2, 3)
Z = MatrixSymbol('Z', 2, 2)

def test_square():
    assert ask(Q.square(X))
    assert not ask(Q.square(Y))
    assert ask(Q.square(Y*Y.T))

def test_invertible():
    assert ask(Q.invertible(X), Q.invertible(X))
    assert ask(Q.invertible(Y)) is False
    assert ask(Q.invertible(X*Y), Q.invertible(X)) is False
    assert ask(Q.invertible(X*Z), Q.invertible(X)) is None
    assert ask(Q.invertible(X*Z), Q.invertible(X) & Q.invertible(Z)) is True
    assert ask(Q.invertible(X.T)) is None
    assert ask(Q.invertible(X.T), Q.invertible(X)) is True
    assert ask(Q.invertible(X.I)) is True
    assert ask(Q.invertible(Identity(3))) is True
    assert ask(Q.invertible(ZeroMatrix(3, 3))) is False
    assert ask(Q.invertible(X), Q.fullrank(X) & Q.square(X))

def test_singular():
    assert ask(Q.singular(X)) is None
    assert ask(Q.singular(X), Q.invertible(X)) is False
    assert ask(Q.singular(X), ~Q.invertible(X)) is True

@XFAIL
def test_invertible_fullrank():
    assert ask(Q.invertible(X), Q.fullrank(X))


def test_symmetric():
    assert ask(Q.symmetric(X), Q.symmetric(X))
    assert ask(Q.symmetric(X*Z), Q.symmetric(X)) is None
    assert ask(Q.symmetric(X*Z), Q.symmetric(X) & Q.symmetric(Z)) is True
    assert ask(Q.symmetric(X + Z), Q.symmetric(X) & Q.symmetric(Z)) is True
    assert ask(Q.symmetric(Y)) is False
    assert ask(Q.symmetric(Y*Y.T)) is True
    assert ask(Q.symmetric(Y.T*X*Y)) is None
    assert ask(Q.symmetric(Y.T*X*Y), Q.symmetric(X)) is True
    assert ask(Q.symmetric(X*X*X*X*X*X*X*X*X*X), Q.symmetric(X)) is True


def _test_orthogonal_unitary(predicate):
    assert ask(predicate(X), predicate(X))
    assert ask(predicate(X.T), predicate(X)) is True
    assert ask(predicate(X.I), predicate(X)) is True
    assert ask(predicate(Y)) is False
    assert ask(predicate(X)) is None
    assert ask(predicate(X*Z*X), predicate(X) & predicate(Z)) is True
    assert ask(predicate(Identity(3))) is True
    assert ask(predicate(ZeroMatrix(3, 3))) is False
    assert ask(Q.invertible(X), predicate(X))
    assert not ask(predicate(X + Z), predicate(X) & predicate(Z))

def test_orthogonal():
    _test_orthogonal_unitary(Q.orthogonal)

def test_unitary():
    _test_orthogonal_unitary(Q.unitary)
    assert ask(Q.unitary(X), Q.orthogonal(X))

def test_fullrank():
    assert ask(Q.fullrank(X), Q.fullrank(X))
    assert ask(Q.fullrank(X.T), Q.fullrank(X)) is True
    assert ask(Q.fullrank(X)) is None
    assert ask(Q.fullrank(Y)) is None
    assert ask(Q.fullrank(X*Z), Q.fullrank(X) & Q.fullrank(Z)) is True
    assert ask(Q.fullrank(Identity(3))) is True
    assert ask(Q.fullrank(ZeroMatrix(3, 3))) is False
    assert ask(Q.invertible(X), ~Q.fullrank(X)) == False


def test_positive_definite():
    assert ask(Q.positive_definite(X), Q.positive_definite(X))
    assert ask(Q.positive_definite(X.T), Q.positive_definite(X)) is True
    assert ask(Q.positive_definite(X.I), Q.positive_definite(X)) is True
    assert ask(Q.positive_definite(Y)) is False
    assert ask(Q.positive_definite(X)) is None
    assert ask(Q.positive_definite(X*Z*X),
            Q.positive_definite(X) & Q.positive_definite(Z)) is True
    assert ask(Q.positive_definite(X), Q.orthogonal(X))
    assert ask(Q.positive_definite(Y.T*X*Y),
            Q.positive_definite(X) & Q.fullrank(Y)) is True
    assert not ask(Q.positive_definite(Y.T*X*Y), Q.positive_definite(X))
    assert ask(Q.positive_definite(Identity(3))) is True
    assert ask(Q.positive_definite(ZeroMatrix(3, 3))) is False
    assert ask(Q.positive_definite(X + Z), Q.positive_definite(X) &
            Q.positive_definite(Z)) is True
    assert not ask(Q.positive_definite(-X), Q.positive_definite(X))
    assert ask(Q.positive(X[1, 1]), Q.positive_definite(X))

def test_triangular():
    assert ask(Q.upper_triangular(X + Z.T + Identity(2)), Q.upper_triangular(X) &
            Q.lower_triangular(Z)) is True
    assert ask(Q.upper_triangular(X*Z.T), Q.upper_triangular(X) &
            Q.lower_triangular(Z)) is True
    assert ask(Q.lower_triangular(Identity(3))) is True
    assert ask(Q.lower_triangular(ZeroMatrix(3, 3))) is True
    assert ask(Q.triangular(X), Q.unit_triangular(X))


def test_diagonal():
    assert ask(Q.diagonal(X + Z.T + Identity(2)), Q.diagonal(X) &
               Q.diagonal(Z)) is True
    assert ask(Q.diagonal(ZeroMatrix(3, 3)))
    assert ask(Q.lower_triangular(X) & Q.upper_triangular(X), Q.diagonal(X))
    assert ask(Q.diagonal(X), Q.lower_triangular(X) & Q.upper_triangular(X))
    assert ask(Q.symmetric(X), Q.diagonal(X))
    assert ask(Q.triangular(X), Q.diagonal(X))


def test_non_atoms():
    assert ask(Q.real(Trace(X)), Q.positive(Trace(X)))

@XFAIL
def test_non_trivial_implies():
    X = MatrixSymbol('X', 3, 3)
    Y = MatrixSymbol('Y', 3, 3)
    assert ask(Q.lower_triangular(X+Y), Q.lower_triangular(X) &
               Q.lower_triangular(Y))
    assert ask(Q.triangular(X), Q.lower_triangular(X))
    assert ask(Q.triangular(X+Y), Q.lower_triangular(X) &
               Q.lower_triangular(Y))

def test_MatrixSlice():
    X = MatrixSymbol('X', 4, 4)
    B = MatrixSlice(X, (1, 3), (1, 3))
    C = MatrixSlice(X, (0, 3), (1, 3))
    assert ask(Q.symmetric(B), Q.symmetric(X))
    assert ask(Q.invertible(B), Q.invertible(X))
    assert ask(Q.diagonal(B), Q.diagonal(X))
    assert ask(Q.orthogonal(B), Q.orthogonal(X))
    assert ask(Q.upper_triangular(B), Q.upper_triangular(X))

    assert not ask(Q.symmetric(C), Q.symmetric(X))
    assert not ask(Q.invertible(C), Q.invertible(X))
    assert not ask(Q.diagonal(C), Q.diagonal(X))
    assert not ask(Q.orthogonal(C), Q.orthogonal(X))
    assert not ask(Q.upper_triangular(C), Q.upper_triangular(X))

def test_det_trace_positive():
    X = MatrixSymbol('X', 4, 4)
    assert ask(Q.positive(Trace(X)), Q.positive_definite(X))
    assert ask(Q.positive(Determinant(X)), Q.positive_definite(X))

def test_field_assumptions():
    X = MatrixSymbol('X', 4, 4)
    Y = MatrixSymbol('Y', 4, 4)
    assert ask(Q.real_elements(X), Q.real_elements(X))
    assert not ask(Q.integer_elements(X), Q.real_elements(X))
    assert ask(Q.complex_elements(X), Q.real_elements(X))
    assert ask(Q.real_elements(X+Y), Q.real_elements(X)) is None
    assert ask(Q.real_elements(X+Y), Q.real_elements(X) & Q.real_elements(Y))
    assert ask(Q.complex_elements(X+Y), Q.real_elements(X) & Q.complex_elements(Y))

    assert ask(Q.real_elements(X.T), Q.real_elements(X))
    assert ask(Q.real_elements(X.I), Q.real_elements(X) & Q.invertible(X))
    assert ask(Q.real_elements(Trace(X)), Q.real_elements(X))
    assert ask(Q.integer_elements(Determinant(X)), Q.integer_elements(X))
    assert not ask(Q.integer_elements(X.I), Q.integer_elements(X))

def test_matrix_element_sets():
    X = MatrixSymbol('X', 4, 4)
    assert ask(Q.real(X[1, 2]), Q.real_elements(X))
    assert ask(Q.integer(X[1, 2]), Q.integer_elements(X))
    assert ask(Q.complex(X[1, 2]), Q.complex_elements(X))
    assert ask(Q.integer_elements(Identity(3)))
    assert ask(Q.integer_elements(ZeroMatrix(3, 3)))
    from sympy.matrices.expressions.fourier import DFT
    assert ask(Q.complex_elements(DFT(3)))
