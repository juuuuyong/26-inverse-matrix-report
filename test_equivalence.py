"""
equivalence_relation.py 검증 테스트
무작위 5x5 관계행렬을 만들어, 프로그램의 판별 함수와 폐포 함수 결과를
집합 정의대로 직접 계산한 값과 비교한다.

실행 : python test_equivalence.py
"""
import random
import equivalence_relation as eq

R5 = range(5)


def to_set(m):
    return {(i, j) for i in R5 for j in R5 if m[i][j]}


def transitive_closure_by_definition(s):
    """(a,b), (b,c) 가 있으면 (a,c) 를 더하는 일을 더 이상 바뀌지 않을 때까지 반복"""
    t = set(s)
    while True:
        new = {(a, d) for a, b in t for c, d in t if b == c} - t
        if not new:
            return t
        t |= new


def test(trials=20000, seed=2026):
    random.seed(seed)
    for _ in range(trials):
        m = [[1 if random.random() < 0.3 else 0 for _ in R5] for _ in R5]
        s = to_set(m)
        # 판별 함수
        assert eq.is_reflexive(m)[0] == all((i, i) in s for i in R5)
        assert eq.is_symmetric(m)[0] == all((b, a) in s for a, b in s)
        assert eq.is_transitive(m)[0] == all((a, d) in s for a, b in s for c, d in s if b == c)
        # 폐포 함수
        assert to_set(eq.reflexive_closure(m)) == s | {(i, i) for i in R5}
        assert to_set(eq.symmetric_closure(m)) == s | {(b, a) for a, b in s}
        assert to_set(eq.transitive_closure(m)) == transitive_closure_by_definition(s)
        # 동치 폐포는 항상 동치 관계
        e = eq.equivalence_closure(m)
        assert eq.is_reflexive(e)[0] and eq.is_symmetric(e)[0] and eq.is_transitive(e)[0]
    print(f"무작위 관계행렬 {trials}개 검증 통과")


if __name__ == "__main__":
    test()
