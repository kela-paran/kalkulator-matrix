from sympy import Matrix, Rational
import copy

def to_rational_matrix(matrix):
    return Matrix([[Rational(x) for x in row] for row in matrix])

def can_use_sarrus(matrix):
    """Check if matrix is 2x2 or 3x3"""
    return len(matrix) in [2, 3] and len(matrix[0]) in [2, 3]

def determinant_obe_steps(matrix):
    """Calculate determinant using Row Operations (OBE)"""
    A = to_rational_matrix(matrix)
    n = A.shape[0]
    steps = []
    det = 1
    factor = 1
    
    # Create a copy for tracking
    current = Matrix(A)
    
    for i in range(n):
        #--CARI PIVOT--
        pivot = current[i, i]
        pivot_row = i
        
        #--KALO PIVOT 0, SWAP--
        if pivot == 0:
            for k in range(i + 1, n):
                if current[k, i] != 0:
                    # Swap rows
                    current.row_swap(i, k)
                    det *= -1
                    steps.append({
                        "title": f"Tukar baris {i+1} dan {k+1}",
                        "desc": f"Menukar baris {i+1} dengan baris {k+1} (determinan dikali -1)",
                        "matrix": current.tolist()
                    })
                    pivot = current[i, i]
                    break
        
        if pivot == 0:
            return 0, steps
        
        #--ELIMINASI BARIS--
        for j in range(i + 1, n):
            if current[j, i] != 0:
                factor = current[j, i] / current[i, i]
                current.row_op(j, lambda x, k: x - factor * current[i, k])
                steps.append({
                    "title": f"Eliminasi baris {j+1}",
                    "desc": f"B{ j+1} = B{j+1} - ({factor}) × B{i+1}",
                    "matrix": current.tolist()
                })
    
    # Product of diagonal elements
    det = 1
    for i in range(n):
        det *= current[i, i]
    
    steps.append({
        "title": "Hasil Akhir",
        "desc": f"Determinan = hasil kali diagonal utama = {det}",
        "matrix": current.tolist()
    })
    
    return det, steps

def determinant_sarrus_steps(matrix):
    """Calculate determinant using Sarrus rule (2x2 or 3x3)"""
    if not can_use_sarrus(matrix):
        return None, []
    
    steps = []
    n = len(matrix)
    
    if n == 2:
        #--SARRUS 2x2--
        a, b = matrix[0][0], matrix[0][1]
        c, d = matrix[1][0], matrix[1][1]
        
        steps.append({
            "title": "Matriks Awal",
            "desc": f"Matriks {n}x{n}",
            "matrix": matrix
        })
        
        steps.append({
            "title": "Rumus Determinan 2x2",
            "desc": f"det = (a × d) - (b × c)"
        })
        
        steps.append({
            "title": "Substitusi Nilai",
            "desc": f"det = ({a} × {d}) - ({b} × {c})"
        })
        
        steps.append({
            "title": "Perkalian",
            "desc": f"det = {a*d} - {b*c}"
        })
        
        det = a*d - b*c
        
        steps.append({
            "title": "Hasil Akhir",
            "desc": f"det = {det}",
            "matrix": matrix
        })
        
        return det, steps
    
    else:  # n == 3
        #--SARRUS 3x3--
        a11, a12, a13 = matrix[0][0], matrix[0][1], matrix[0][2]
        a21, a22, a23 = matrix[1][0], matrix[1][1], matrix[1][2]
        a31, a32, a33 = matrix[2][0], matrix[2][1], matrix[2][2]
        
        steps.append({
            "title": "Matriks Awal",
            "desc": "Matriks 3x3 yang akan dihitung determinannya",
            "matrix": matrix
        })
        
        #--DIAGONAL POSITIF-- (top-left to bottom-right)
        pos1 = a11 * a22 * a33
        pos2 = a12 * a23 * a31
        pos3 = a13 * a21 * a32
        
        #--DIAGONAL MINUS-- (bottom-left to top-right)
        neg1 = a31 * a22 * a13
        neg2 = a32 * a23 * a11
        neg3 = a33 * a21 * a12
        
        steps.append({
            "title": "Diagonal Positif (ke kanan bawah)",
            "desc": f"({a11} × {a22} × {a33}) + ({a12} × {a23} × {a31}) + ({a13} × {a21} × {a32})\n= {pos1} + {pos2} + {pos3}\n= {pos1 + pos2 + pos3}"
        })
        
        steps.append({
            "title": "Diagonal Negatif (ke kiri bawah)",
            "desc": f"({a31} × {a22} × {a13}) + ({a32} × {a23} × {a11}) + ({a33} × {a21} × {a12})\n= {neg1} + {neg2} + {neg3}\n= {neg1 + neg2 + neg3}"
        })
        
        det = (pos1 + pos2 + pos3) - (neg1 + neg2 + neg3)
        
        steps.append({
            "title": "Hasil Akhir",
            "desc": f"det = (positif) - (negatif)\ndet = {pos1 + pos2 + pos3} - {neg1 + neg2 + neg3}\ndet = {det}",
            "matrix": matrix
        })
        
        return det, steps

def determinant_cofactor_steps(matrix):
    """Calculate determinant using cofactor expansion"""
    A = to_rational_matrix(matrix)
    n = A.shape[0]
    steps = []
    
    #--PILIH BARIS UNTUK EKSPANSI--
    steps.append({
        "title": "Pilih Baris untuk Ekspansi",
        "desc": "Kita akan melakukan ekspansi kofaktor sepanjang **BARIS 1**",
        "matrix": matrix
    })
    
    total = 0
    for j in range(n):
        #--buat minor dengan menghapus baris 0 dan kolom j
        minor_rows = []
        for r in range(1, n):
            row = []
            for c in range(n):
                if c != j:
                    row.append(A[r, c])
            minor_rows.append(row)
        
        minor = Matrix(minor_rows)
        minor_det = minor.det()
        cofactor = ((-1) ** (0 + j)) * minor_det
        kontribusi = A[0, j] * cofactor
        
        steps.append({
            "title": f"Elemen a₁{j+1} = {A[0, j]}",
            "desc": f"Minor M₁{j+1}:\n{minor.tolist()}\n\n"
                    f"det(M₁{j+1}) = {minor_det}\n\n"
                    f"C₁{j+1} = (-1)^(1+{j+1}) × {minor_det} = {cofactor}\n\n"
                    f"Kontribusi = {A[0, j]} × {cofactor} = {kontribusi}"
        })
        
        total += kontribusi
    
    steps.append({
        "title": "Jumlahkan Semua Kontribusi",
        "desc": f"det = {total}"
    })
    
    # Format hasil biar ga .0 kalo bulat
    if total == int(total):
        total = int(total)
    
    return total, steps
