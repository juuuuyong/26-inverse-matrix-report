"""
역행렬을 구하는 프로그램
----------------------------------------------------
구성 조건
 1. 행렬 입력 기능          : input_matrix()
 2. 행렬식을 이용한 역행렬   : inverse_by_determinant()
 3. 가우스-조던 소거법       : inverse_by_gauss_jordan()
 4. 결과 출력 및 비교 기능   : compare_matrices(), main()

추가기능
 - 구한 역행렬이 올바른지 A x A^-1 = I 검증 (verify_inverse)
"""

# =========================================================
# 1. 행렬 입력 기능
# =========================================================
def input_matrix():
    """사용자로부터 정수 n을 입력받아 n x n 정방행렬을
    행 단위로 입력받고, 2차원 리스트(배열)로 반환한다."""
    while True:
        try:
            n = int(input("행렬의 크기 n을 입력하세요 (n x n): "))
            if n < 1:
                print("  -> 행렬의 크기는 1 이상이어야 합니다. 다시 입력하세요.")
                continue
            break
        except ValueError:
            print("  -> 정수 크기를 입력하세요. 다시 입력하세요.")

    print(f"{n} x {n} 행렬을 한 행씩, 숫자는 공백으로 구분하여 입력하세요.")

    matrix = []
    for i in range(n):
        while True:
            row_input = input(f" {i + 1}행 입력: ").split()
            if len(row_input) != n:
                print(f"  -> {n}개의 숫자를 입력해야 합니다. 다시 입력하세요.")
                continue
            try:
                row = [float(x) for x in row_input]
            except ValueError:
                print("  -> 숫자만 입력할 수 있습니다. 다시 입력하세요.")
                continue
            matrix.append(row)
            break
    return matrix


def print_matrix(matrix, title="", precision=4):
    """행렬을 보기 좋게 출력한다."""
    if title:
        print(f"\n[{title}]")
    for row in matrix:
        formatted = [f"{val:>10.{precision}f}" for val in row]
        print(" ".join(formatted))


# =========================================================
# 2. 행렬식을 이용한 역행렬 계산 기능
# =========================================================
def get_minor(matrix, row, col):
    """matrix에서 row행, col열을 제거한 소행렬(minor)을 반환한다."""
    return [r[:col] + r[col + 1:] for i, r in enumerate(matrix) if i != row]


def determinant(matrix):
    """여인수 전개(라플라스 전개)를 이용해 행렬식을 재귀적으로 계산한다."""
    n = len(matrix)

    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for col in range(n):
        minor = get_minor(matrix, 0, col)
        cofactor = ((-1) ** col) * matrix[0][col] * determinant(minor)
        det += cofactor
    return det


def cofactor_matrix(matrix):
    """여인수 행렬(cofactor matrix)을 구한다."""
    n = len(matrix)

    # 1×1 행렬에서 0×0 소행렬의 행렬식은 1로 정의된다.
    # 따라서 [a]의 여인수 행렬은 [[1]]이다.
    if n == 1:
        return [[1.0]]

    cofactors = []
    for i in range(n):
        cof_row = []
        for j in range(n):
            minor = get_minor(matrix, i, j)
            sign = (-1) ** (i + j)
            cof_row.append(sign * determinant(minor))
        cofactors.append(cof_row)
    return cofactors


def transpose(matrix):
    """전치행렬을 구한다."""
    n = len(matrix)
    m = len(matrix[0])
    return [[matrix[i][j] for i in range(n)] for j in range(m)]


def inverse_by_determinant(matrix):
    """행렬식(여인수 전개)을 사용하여 역행렬을 계산한다.
    역행렬이 존재하지 않을 경우(행렬식이 0인 경우) None을 반환한다."""
    n = len(matrix)
    det = determinant(matrix)

    if abs(det) < 1e-10:
        print("[오류] 행렬식이 0입니다. 역행렬이 존재하지 않습니다. (행렬식 방법)")
        return None

    # 여인수 행렬 -> 전치(adjugate, 수반행렬) -> 1/det 곱하기
    cofactors = cofactor_matrix(matrix)
    adjugate = transpose(cofactors)

    inverse = [[adjugate[i][j] / det for j in range(n)] for i in range(n)]
    return inverse


# =========================================================
# 3. 가우스-조던 소거법을 이용한 역행렬 계산 기능
# =========================================================
def inverse_by_gauss_jordan(matrix):
    """가우스-조던 소거법을 사용하여 역행렬을 계산한다.
    [A | I] 를 [I | A^-1] 형태로 만든다.
    역행렬이 존재하지 않을 경우(피벗이 0이 되는 경우) None을 반환한다."""
    n = len(matrix)

    # 증대행렬 [A | I] 생성 (원본 matrix는 변경하지 않도록 복사)
    aug = [matrix[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    for col in range(n):
        # --- 피벗(기준행) 찾기: 현재 열에서 절댓값이 가장 큰 행을 선택 (부분 피벗팅) ---
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))

        if abs(aug[pivot_row][col]) < 1e-10:
            print("[오류] 피벗이 0입니다. 역행렬이 존재하지 않습니다. (가우스-조던 소거법)")
            return None

        # 필요하면 행 교환
        if pivot_row != col:
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

        # 피벗을 1로 만들기
        pivot_val = aug[col][col]
        aug[col] = [val / pivot_val for val in aug[col]]

        # 다른 모든 행에서 현재 열을 0으로 만들기
        for r in range(n):
            if r != col:
                factor = aug[r][col]
                aug[r] = [aug[r][k] - factor * aug[col][k] for k in range(2 * n)]

    # 오른쪽 절반(n ~ 2n-1 열)이 역행렬
    inverse = [row[n:] for row in aug]
    return inverse


# =========================================================
# 4. 결과 출력 및 비교 기능
# =========================================================
def compare_matrices(m1, m2, tol=1e-6):
    """두 행렬이 (오차범위 내에서) 같은지 비교한다."""
    if m1 is None or m2 is None:
        return False
    n = len(m1)
    for i in range(n):
        for j in range(n):
            if abs(m1[i][j] - m2[i][j]) > tol:
                return False
    return True


# =========================================================
# 추가기능 : A x A^-1 = I 검증
# =========================================================
def multiply_matrix(a, b):
    n = len(a)
    result = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = sum(a[i][k] * b[k][j] for k in range(n))
    return result


def is_identity(matrix, tol=1e-6):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            expected = 1.0 if i == j else 0.0
            if abs(matrix[i][j] - expected) > tol:
                return False
    return True


def verify_inverse(original, inverse, label):
    """A x A^-1 이 단위행렬 I가 되는지 검증하여 역행렬이 올바른지 확인한다."""
    if inverse is None:
        return
    product = multiply_matrix(original, inverse)
    print_matrix(product, title=f"검증: A x {label} (단위행렬 I가 나와야 함)")
    if is_identity(product):
        print(f"-> 검증 성공: A x {label} = I 입니다.")
    else:
        print(f"-> 검증 실패: A x {label} != I 입니다.")


# =========================================================
# 메인 함수
# =========================================================
def main():
    print("=" * 50)
    print(" 역행렬 계산 프로그램")
    print(" (행렬식 방법 vs 가우스-조던 소거법)")
    print("=" * 50)

    matrix = input_matrix()
    print_matrix(matrix, title="입력된 행렬 A")

    # 방법 1: 행렬식(여인수 전개)을 이용한 역행렬
    inv_det = inverse_by_determinant(matrix)
    if inv_det is not None:
        print_matrix(inv_det, title="방법 1: 행렬식(여인수 전개)으로 구한 역행렬")

    # 방법 2: 가우스-조던 소거법을 이용한 역행렬
    inv_gj = inverse_by_gauss_jordan(matrix)
    if inv_gj is not None:
        print_matrix(inv_gj, title="방법 2: 가우스-조던 소거법으로 구한 역행렬")

    # 결과 비교
    print("\n[결과 비교]")
    if inv_det is None or inv_gj is None:
        print("-> 역행렬이 존재하지 않아 비교할 수 없습니다.")
    elif compare_matrices(inv_det, inv_gj):
        print("-> 두 방법으로 구한 역행렬이 서로 일치합니다. (프로그램 정상 동작)")
    else:
        print("-> 두 방법으로 구한 역행렬이 서로 다릅니다. (오차 확인 필요)")

    # 추가기능: 검증
    print("\n[추가기능: A x A^-1 = I 검증]")
    verify_inverse(matrix, inv_det, "A^-1(행렬식)")
    verify_inverse(matrix, inv_gj, "A^-1(가우스-조던)")


if __name__ == "__main__":
    main()
