# 26 - Discrete Mathematics - reports.

# Report 1 - 역행렬 계산 프로그램

행렬식(여인수 전개) 방법과 가우스-조던 소거법을 이용하여
n×n 행렬의 역행렬을 계산하는 프로그램입니다.

## 주요 기능

1. n×n 행렬 입력
2. 행렬식(여인수 전개)을 이용한 역행렬 계산
3. 가우스-조던 소거법을 이용한 역행렬 계산
4. 두 방법의 결과 비교
5. A × A⁻¹ = I 검증

## 실행 방법

```bash
python3 matrix_inverse_수정본.py
```


# Report 2 - 동치 관계 판별 프로그램

# 집합 A = {1, 2, 3, 4, 5} 에 관한 5×5 관계행렬을 입력받아
반사·대칭·추이 관계를 판별하고, 동치 관계이면 동치류를 출력하는 Python 프로그램입니다.
동치 관계가 아니면 성립하지 않는 성질마다 폐포로 변환한 뒤 다시 판별합니다.

## 실행 방법

```bash
python equivalence_relation.py
```

Python 3.8 이상, 외부 라이브러리는 필요 없습니다.
메뉴에서 `0`을 고르면 행렬을 직접 입력하고, `1`~`5`를 고르면 예제 행렬로 바로 실행합니다.

## 구성 조건과 함수

| 조건 | 내용 | 함수 |
|---|---|---|
| 1 | 5×5 관계행렬을 행 단위로 입력, 2차원 리스트로 저장 | `input_matrix()`, `print_matrix()` |
| 2 | 반사·대칭·추이 판별, 동치 관계 여부 메시지 출력 | `is_reflexive()`, `is_symmetric()`, `is_transitive()`, `check_equivalence()` |
| 3 | 각 원소의 동치류 판별·출력 | `equivalence_class()`, `print_equivalence_classes()` |
| 4 | 반사·대칭·추이 폐포 변환, 전·후 출력, 재판별 | `reflexive_closure()`, `symmetric_closure()`, `transitive_closure()`(와샬), `apply_closure()` |

## 추가 기능

- 입력 검증: 값 개수나 0/1 이외의 값이 틀리면 그 행을 다시 입력
- 예제 행렬 메뉴 (5가지 경우)
- 성질이 성립하지 않는 근거(빠진 순서쌍) 출력
- 폐포 변환으로 추가된 순서쌍 표시
- 동치 폐포(반사 → 대칭 → 추이)와 그 분할 출력
- 반복 실행 (y/n)

## 검증

```bash
python test_equivalence.py
```
