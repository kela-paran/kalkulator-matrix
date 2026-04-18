from sympy import Matrix, Rational

def to_rational_matrix(matrix):
    return Matrix([[Rational(x) for x in row] for row in matrix])


def analyze_solution(A):
    rows, cols = A.shape
    rank = A.rank()
    rank_aug = A[:, :-1].rank()

    if rank != rank_aug:
        return "Tidak ada solusi"
    elif rank == cols - 1:
        return "Solusi unik"
    else:
        return "Solusi tak hingga"


def gauss_jordan_steps(matrix):
    A = to_rational_matrix(matrix)
    rows, cols = A.shape
    steps = []

    for i in range(rows):
        pivot = A[i, i]

        if pivot == 0:
            return None, [], "Pivot 0 → tidak bisa lanjut"

        # bikin pivot jadi 1
        A[i, :] = A[i, :] / pivot
        steps.append({
            "desc": f"Bagi baris {i+1} dengan {pivot}",
            "matrix": A.copy(),
            "pivot": (i, i)
        })

        # eliminasi
        for j in range(rows):
            if i != j:
                faktor = A[j, i]
                A[j, :] = A[j, :] - faktor * A[i, :]
                steps.append({
                    "desc": f"Baris {j+1} - ({faktor}) × Baris {i+1}",
                    "matrix": A.copy(),
                    "pivot": (i, i)
                })

    solusi = analyze_solution(A)

    return A, steps, solusi