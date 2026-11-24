"""
Report 2 : 동치 관계 판별 프로그램
----------------------------------------------------
집합 A = {1, 2, 3, 4, 5} 에 관한 관계행렬을 입력받아
동치 관계인지 판별하고, 동치 관계이면 동치류를 출력한다.

구성 조건
 1. 관계 행렬 입력 기능        : input_matrix()
 2. 동치 관계 판별 기능        : is_reflexive(), is_symmetric(),
                                 is_transitive(), check_equivalence()
 3. 동치류 출력 기능           : equivalence_class(), print_equivalence_classes()
 4. 폐포 구현 기능             : reflexive_closure(), symmetric_closure(),
                                 transitive_closure(), apply_closure()

추가 기능
 - 입력 검증 : 0/1 이외의 값, 개수 오류를 다시 입력받음
 - 예제 행렬 메뉴 : 미리 준비한 관계를 골라 바로 실행
 - 위반 근거 출력 : 성질이 성립하지 않는 이유(빠진 순서쌍)를 구체적으로 출력
 - 추가된 순서쌍 출력 : 폐포로 변환할 때 새로 추가된 순서쌍을 표시
 - 동치 폐포 : 반사 → 대칭 → 추이 폐포를 차례로 적용해
               R 을 포함하는 가장 작은 동치 관계와 그 분할(partition)을 출력
 - 반복 실행 : 프로그램을 종료하지 않고 다른 관계를 계속 검사
"""

A = [1, 2, 3, 4, 5]   # 집합 A
N = len(A)            # 행렬 크기 (5)

# 추가 기능 : 예제 관계행렬
SAMPLES = {
    "1": ("동치 관계 (동치류 {1,2}, {3}, {4,5})",
          [[1, 1, 0, 0, 0],
           [1, 1, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 1, 1],
           [0, 0, 0, 1, 1]]),
    "2": ("반사 관계만 아님 ((3,3) 없음)",
          [[1, 1, 0, 0, 0],
           [1, 1, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 1, 1],
           [0, 0, 0, 1, 1]]),
    "3": ("대칭 관계만 아님 ((1,2)만 있고 (2,1) 없음)",
          [[1, 1, 0, 0, 0],
           [0, 1, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 1, 0],
           [0, 0, 0, 0, 1]]),
    "4": ("추이 관계만 아님 (1~2, 2~3 이지만 1~3 없음)",
          [[1, 1, 0, 0, 0],
           [1, 1, 1, 0, 0],
           [0, 1, 1, 0, 0],
           [0, 0, 0, 1, 0],
           [0, 0, 0, 0, 1]]),
    "5": ("세 성질 모두 아님",
          [[0, 1, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0]]),
}


# =========================================================
# 1. 관계 행렬 입력 기능
# =========================================================
def input_matrix():
    """5 x 5 관계행렬을 행 단위로 입력받아 2차원 리스트로 반환한다.
    각 행은 0 또는 1 다섯 개를 공백으로 구분해 입력한다."""
    print(f"\n{N} x {N} 관계행렬을 한 행씩 입력하세요. (0 또는 1, 공백으로 구분)")
    print("  M[i][j] = 1 이면 (i, j) ∈ R 입니다.")
    matrix = []
    for i in range(N):
        while True:
            values = input(f" {A[i]}행 입력: ").split()
            if len(values) != N:                       # 개수 검사
                print(f"  -> {N}개의 값을 입력해야 합니다. 다시 입력하세요.")
                continue
            if any(v not in ("0", "1") for v in values):  # 0/1 검사
                print("  -> 0 또는 1만 입력할 수 있습니다. 다시 입력하세요.")
                continue
            matrix.append([int(v) for v in values])
            break
    return matrix


def choose_matrix():
    """추가 기능 : 직접 입력할지, 예제 행렬을 쓸지 고른다."""
    print("\n[관계행렬 선택]")
    print(" 0. 직접 입력")
    for key, (desc, _) in SAMPLES.items():
        print(f" {key}. 예제 - {desc}")
    while True:
        choice = input("번호를 선택하세요: ").strip()
        if choice == "0":
            return input_matrix()
        if choice in SAMPLES:
            return [row[:] for row in SAMPLES[choice][1]]
        print("  -> 목록에 있는 번호를 입력하세요.")


def print_matrix(matrix, title=""):
    """관계행렬을 행/열 번호와 함께 출력한다."""
    if title:
        print(f"\n[{title}]")
    print("     " + " ".join(str(a) for a in A))
    print("    " + "-" * (2 * N))
    for i in range(N):
        print(f" {A[i]} | " + " ".join(str(v) for v in matrix[i]))


def to_pairs(matrix):
    """관계행렬을 순서쌍 리스트로 바꾼다."""
    return [(A[i], A[j]) for i in range(N) for j in range(N) if matrix[i][j] == 1]


def print_pairs(matrix, label="R"):
    pairs = to_pairs(matrix)
    text = ", ".join(f"({a},{b})" for a, b in pairs)
    print(f" {label} = {{{text}}}  (순서쌍 {len(pairs)}개)")


# =========================================================
# 2. 동치 관계 판별 기능
# =========================================================
def is_reflexive(matrix):
    """반사 관계 : 모든 a 에 대해 (a, a) ∈ R  (주대각선이 모두 1)
    반환값 : (성립 여부, 빠진 순서쌍 리스트)"""
    missing = [(A[i], A[i]) for i in range(N) if matrix[i][i] != 1]
    return len(missing) == 0, missing


def is_symmetric(matrix):
    """대칭 관계 : (a, b) ∈ R 이면 (b, a) ∈ R  (M = M의 전치)
    반환값 : (성립 여부, [(있는 순서쌍, 빠진 순서쌍), ...])"""
    violations = []
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1 and matrix[j][i] != 1:
                violations.append(((A[i], A[j]), (A[j], A[i])))
    return len(violations) == 0, violations


def is_transitive(matrix):
    """추이 관계 : (a, b) ∈ R 이고 (b, c) ∈ R 이면 (a, c) ∈ R
    반환값 : (성립 여부, [(a, b, c), ...])  -> (a, c) 가 빠진 경우"""
    violations = []
    for i in range(N):
        for j in range(N):
            if matrix[i][j] != 1:
                continue
            for k in range(N):
                if matrix[j][k] == 1 and matrix[i][k] != 1:
                    violations.append((A[i], A[j], A[k]))
    return len(violations) == 0, violations


def check_equivalence(matrix, show_detail=True):
    """반사·대칭·추이 성질을 판별해 출력하고, 동치 관계 여부를 반환한다."""
    ref, ref_missing = is_reflexive(matrix)
    sym, sym_viol = is_symmetric(matrix)
    tra, tra_viol = is_transitive(matrix)

    mark = lambda ok: "O (성립)" if ok else "X (성립하지 않음)"
    print(f"  반사 관계 : {mark(ref)}")
    if not ref and show_detail:   # 추가 기능 : 위반 근거
        print("     - 빠진 순서쌍:", ", ".join(f"({a},{b})" for a, b in ref_missing))
    print(f"  대칭 관계 : {mark(sym)}")
    if not sym and show_detail:
        for have, need in sym_viol[:3]:
            print(f"     - ({have[0]},{have[1]}) ∈ R 이지만 ({need[0]},{need[1]}) ∉ R")
        if len(sym_viol) > 3:
            print(f"     - ... 외 {len(sym_viol) - 3}개")
    print(f"  추이 관계 : {mark(tra)}")
    if not tra and show_detail:
        for a, b, c in tra_viol[:3]:
            print(f"     - ({a},{b}), ({b},{c}) ∈ R 이지만 ({a},{c}) ∉ R")
        if len(tra_viol) > 3:
            print(f"     - ... 외 {len(tra_viol) - 3}개")

    equivalent = ref and sym and tra
    if equivalent:
        print("  => 반사·대칭·추이 관계를 모두 만족하므로 동치 관계입니다.")
    else:
        failed = [name for name, ok in (("반사", ref), ("대칭", sym), ("추이", tra)) if not ok]
        print(f"  => {', '.join(failed)} 관계를 만족하지 않으므로 동치 관계가 아닙니다.")
    return equivalent


# =========================================================
# 3. 동치 관계일 경우 동치류 출력 기능
# =========================================================
def equivalence_class(matrix, x):
    """원소 x 의 동치류 [x] = { y ∈ A | (x, y) ∈ R } 를 구한다."""
    i = A.index(x)
    return [A[j] for j in range(N) if matrix[i][j] == 1]


def print_equivalence_classes(matrix):
    """집합의 각 원소에 대한 동치류를 출력하고, 서로 다른 동치류(분할)도 출력한다."""
    print("  [동치류]")
    classes = []
    for x in A:
        cls = equivalence_class(matrix, x)
        print(f"   [{x}] = {{{', '.join(map(str, cls))}}}")
        if cls not in classes:
            classes.append(cls)
    # 추가 기능 : 서로 다른 동치류 = A 의 분할
    parts = ", ".join("{" + ", ".join(map(str, c)) + "}" for c in classes)
    print(f"  서로 다른 동치류 {len(classes)}개 → A 의 분할: {{{parts}}}")


# =========================================================
# 4. 폐포 구현 기능
# =========================================================
def reflexive_closure(matrix):
    """반사 폐포 : 주대각선 성분을 모두 1로 만든다.  R ∪ {(a,a) | a ∈ A}"""
    result = [row[:] for row in matrix]
    for i in range(N):
        result[i][i] = 1
    return result


def symmetric_closure(matrix):
    """대칭 폐포 : (a,b) 가 있으면 (b,a) 도 추가한다.  R ∪ R^-1"""
    result = [row[:] for row in matrix]
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                result[j][i] = 1
    return result


def transitive_closure(matrix):
    """추이 폐포 : 와샬(Warshall) 알고리즘
    k 를 경유점으로 하여 i→k, k→j 가 있으면 i→j 를 추가한다."""
    result = [row[:] for row in matrix]
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if result[i][k] == 1 and result[k][j] == 1:
                    result[i][j] = 1
    return result


def added_pairs(before, after):
    """추가 기능 : 폐포 변환으로 새로 추가된 순서쌍"""
    return [(A[i], A[j]) for i in range(N) for j in range(N)
            if before[i][j] == 0 and after[i][j] == 1]


def apply_closure(matrix, name, closure_func, already_ok):
    """폐포 변환 전/후를 출력하고, 변환 후 동치 관계를 다시 판별한다."""
    print("\n" + "=" * 50)
    print(f" {name} 폐포")
    print("=" * 50)
    if already_ok:
        print(f"  입력 관계가 이미 {name} 관계이므로 {name} 폐포는 R 자신과 같습니다.")
        return matrix

    closed = closure_func(matrix)
    print_matrix(matrix, f"{name} 폐포 변환 전")
    print_matrix(closed, f"{name} 폐포 변환 후")
    new = added_pairs(matrix, closed)
    print(f"  추가된 순서쌍 {len(new)}개: " + ", ".join(f"({a},{b})" for a, b in new))

    print(f"\n  [{name} 폐포에 대한 동치 관계 재판별]")
    if check_equivalence(closed, show_detail=False):
        print_equivalence_classes(closed)
    return closed


def equivalence_closure(matrix):
    """추가 기능 : 동치 폐포 = 추이( 대칭( 반사(R) ) )
    R 을 포함하는 가장 작은 동치 관계"""
    return transitive_closure(symmetric_closure(reflexive_closure(matrix)))


# =========================================================
# 메인 함수
# =========================================================
def run_once():
    matrix = choose_matrix()              # 1. 입력
    print_matrix(matrix, "입력된 관계행렬 M_R")
    print_pairs(matrix)

    print("\n" + "=" * 50)
    print(" 동치 관계 판별")
    print("=" * 50)
    equivalent = check_equivalence(matrix)  # 2. 판별

    if equivalent:                          # 3. 동치류
        print_equivalence_classes(matrix)
        return

    # 4. 성립하지 않는 성질마다 각각의 폐포로 변환
    ref, _ = is_reflexive(matrix)
    sym, _ = is_symmetric(matrix)
    tra, _ = is_transitive(matrix)
    apply_closure(matrix, "반사", reflexive_closure, ref)
    apply_closure(matrix, "대칭", symmetric_closure, sym)
    apply_closure(matrix, "추이", transitive_closure, tra)

    # 추가 기능 : 동치 폐포
    print("\n" + "=" * 50)
    print(" [추가 기능] 동치 폐포 (반사 → 대칭 → 추이)")
    print("=" * 50)
    eq = equivalence_closure(matrix)
    print_matrix(eq, "동치 폐포")
    new = added_pairs(matrix, eq)
    print(f"  추가된 순서쌍 {len(new)}개: " + ", ".join(f"({a},{b})" for a, b in new))
    if check_equivalence(eq, show_detail=False):
        print_equivalence_classes(eq)


def main():
    print("=" * 50)
    print(" 동치 관계 판별 프로그램  (A = {1, 2, 3, 4, 5})")
    print("=" * 50)
    while True:
        run_once()
        again = input("\n다른 관계를 검사하시겠습니까? (y/n): ").strip().lower()
        if again != "y":
            print("프로그램을 종료합니다.")
            break


if __name__ == "__main__":
    main()
