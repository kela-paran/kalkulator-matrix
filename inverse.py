from sympy import Matrix, Rational, eye
import copy

def to_rational_matrix(matrix):
    return Matrix([[Rational(x) for x in row] for row in matrix])

def matrix_to_list(matrix):
    return [[float(matrix[i, j]) for j in range(matrix.shape[1])] for i in range(matrix.shape[0])]

def inverse_adjoint_steps(matrix):
    """Calculate inverse using adjoint method"""
    A = to_rational_matrix(matrix)
    n = A.shape[0]
    steps = []
    
    # Calculate determinant
    det = A.det()
    
    steps.append({
        "title": "Langkah 1: Hitung Determinan",
        "desc": f"det(A) = {det}",
        "matrix": matrix
    })
    
    if det == 0:
        return None, steps, "❌ Matriks singular (determinan = 0), tidak memiliki invers"
    
    # Calculate cofactor matrix
    steps.append({
        "title": "Langkah 2: Hitung Matriks Kofaktor",
        "desc": "Setiap elemen Cij = (-1)^(i+j) × det(Mij), dimana Mij adalah minor",
        "matrix": None
    })
    
    cofactor_matrix = []
    for i in range(n):
        cofactor_row = []
        for j in range(n):
            minor = A.minor_submatrix(i, j)
            minor_det = minor.det()
            cofactor = (-1) ** (i + j) * minor_det
            cofactor_row.append(cofactor)
            
            steps.append({
                "title": f"Kofaktor C{i+1}{j+1}",
                "desc": f"C{i+1}{j+1} = (-1)^{i+j} × det(M{i+1}{j+1}) = {(-1)**(i+j)} × {minor_det} = {cofactor}",
                "minor": minor.tolist() if minor.shape[0] <= 4 else None,
                "cofactor": cofactor
            })
        cofactor_matrix.append(cofactor_row)
    
    steps.append({
        "title": "Matriks Kofaktor",
        "desc": f"Matriks kofaktor:",
        "matrix": cofactor_matrix
    })
    
    # Transpose to get adjoint
    adjoint = Matrix(cofactor_matrix).T
    
    steps.append({
        "title": "Langkah 3: Transpos Matriks Kofaktor (Adjoin)",
        "desc": "Adjoin(A) = (Matriks Kofaktor)ᵀ",
        "matrix": adjoint.tolist()
    })
    
    # Calculate inverse
    inverse = adjoint / det
    
    steps.append({
        "title": "Langkah 4: Hitung Invers",
        "desc": f"A⁻¹ = (1/det(A)) × Adjoin(A) = (1/{det}) × Adjoin(A)",
        "matrix": inverse.tolist()
    })
    
    steps.append({
        "title": "Hasil Akhir",
        "desc": "Invers matriks",
        "matrix": inverse.tolist()
    })
    
    return matrix_to_list(inverse), steps, "✅ Berhasil"

def inverse_obe_steps(matrix):
    """Calculate inverse using Row Operations (OBE)"""
    A = to_rational_matrix(matrix)
    n = A.shape[0]
    
    # Check determinant
    det = A.det()
    steps = []
    
    steps.append({
        "title": "Langkah 1: Cek Determinan",
        "desc": f"det(A) = {det}",
        "matrix": matrix
    })
    
    if det == 0:
        return None, steps, "❌ Matriks singular (determinan = 0), tidak memiliki invers"
    
    # Create augmented matrix [A | I]
    I = eye(n)
    augmented = Matrix.hstack(A, I)
    
    steps.append({
        "title": "Langkah 2: Bentuk Matriks Augmented",
        "desc": "[A | I]",
        "matrix": augmented.tolist()
    })
    
    step_counter = 3
    
    # Gauss-Jordan elimination
    for i in range(n):
        # Make pivot 1
        pivot = augmented[i, i]
        if pivot == 0:
            # Find row to swap
            for k in range(i + 1, n):
                if augmented[k, i] != 0:
                    augmented.row_swap(i, k)
                    steps.append({
                        "title": f"Langkah {step_counter}: Tukar baris {i+1} dan {k+1}",
                        "desc": f"Menukar baris {i+1} dengan baris {k+1}",
                        "matrix": augmented.tolist()
                    })
                    step_counter += 1
                    pivot = augmented[i, i]
                    break
        
        if pivot != 1 and pivot != 0:
            augmented.row_op(i, lambda x, j: x / pivot)
            steps.append({
                "title": f"Langkah {step_counter}: Buat pivot baris {i+1} menjadi 1",
                "desc": f"B{i+1} = B{i+1} / {pivot}",
                "matrix": augmented.tolist()
            })
            step_counter += 1
        
        # Eliminate other rows
        for j in range(n):
            if i != j and augmented[j, i] != 0:
                factor = augmented[j, i]
                augmented.row_op(j, lambda x, k: x - factor * augmented[i, k])
                steps.append({
                    "title": f"Langkah {step_counter}: Eliminasi baris {j+1} kolom {i+1}",
                    "desc": f"B{j+1} = B{j+1} - ({factor}) × B{i+1}",
                    "matrix": augmented.tolist()
                })
                step_counter += 1
    
    # Extract inverse from right half
    inverse = augmented[:, n:]
    
    steps.append({
        "title": f"Langkah {step_counter}: Hasil Akhir",
        "desc": "Invers matriks adalah bagian kanan dari matriks augmented",
        "matrix": inverse.tolist()
    })
    
    return matrix_to_list(inverse), steps, "✅ Berhasil"