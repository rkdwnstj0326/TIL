'''
==========================================================================
 NumPy & Pandas 자기주도 학습 - 실행 파일
==========================================================================

 [사용법]
   함께 제공된 numpy_pandas_guide.md 를 읽으며 이 파일을 실행하세요.
   CHAPTER 번호는 마크다운의 장 번호와 1:1 로 대응합니다.

 [실행 방법]
   $ pip install numpy pandas
   $ python numpy_pandas_guide.py

   CHAPTER 가 하나 끝날 때마다 Enter 를 눌러 다음으로 넘어갑니다.
   (한 번에 쭉 보고 싶으면 아래 PAUSE 를 False 로 바꾸세요)
==========================================================================
'''

import numpy as np
import pandas as pd

PAUSE = True  # True: CHAPTER 마다 Enter 대기 / False: 한 번에 전체 실행


def title(no, text):
    '''CHAPTER 제목 출력 (학습 내용과 무관한 보조 함수)'''
    print()
    print('=' * 70)
    print(f' CHAPTER {no}. {text}')
    print('=' * 70)


def pause():
    '''CHAPTER 사이 일시정지 (학습 내용과 무관한 보조 함수)'''
    if not PAUSE:
        return
    try:
        input('\n  ... Enter 를 누르면 다음 CHAPTER 로 넘어갑니다 ...')
    except EOFError:
        pass


# ==========================================================================
# Part A. NumPy
# ==========================================================================

def ch01_what_is_numpy():
    '''리스트의 * 는 이어붙이기, 배열의 * 는 원소별 계산.'''
    title(1, 'NumPy 란 - 리스트와 배열의 결정적 차이')

    py_list = [1, 2, 3]
    print('  리스트 * 2 :', py_list * 2)  # 이어붙이기 (계산 아님)

    np_arr = np.array([1, 2, 3])
    print('  배열   * 2 :', np_arr * 2)  # 원소별 2배 (진짜 계산)

    print()
    print('  [정리] 이 한 줄 차이가 NumPy 를 쓰는 이유의 전부입니다.')


def ch02_ndarray_attributes():
    '''배열을 만나면 ndim -> shape -> size -> dtype 순서로 확인.'''
    title(2, 'ndarray 의 4가지 속성')

    arr = np.array([[1, 2, 3],
                    [4, 5, 6]])

    print('  배열:')
    print(arr)
    print()
    print('  .ndim  (차원 수)     :', arr.ndim)
    print('  .shape (각 차원 크기):', arr.shape)
    print('  .size  (원소 개수)   :', arr.size)
    print('  .dtype (데이터 타입) :', arr.dtype)

    print()
    print('  [주의] 타입을 섞으면 전부 문자열로 통일되어 버립니다:')
    mixed = np.array([1, 'a'])
    print('    np.array([1, "a"]) 의 dtype =>', mixed.dtype, '(더 이상 숫자가 아님)')


def ch03_creation_functions():
    '''zeros / ones / full / arange / linspace.'''
    title(3, '배열을 만드는 함수들')

    print('  np.zeros(3)          :', np.zeros(3))
    print('  np.ones(3)           :', np.ones(3))
    print('  np.full((2, 3), 2)   :')
    print(np.full((2, 3), 2))
    print('  np.arange(10, 30, 5) :', np.arange(10, 30, 5))
    print('  np.linspace(0, 1, 5) :', np.linspace(0, 1, 5))

    print()
    print('  [구분법] 간격을 알면 arange, 개수를 알면 linspace.')
    print('  [철자]   arange 입니다 (array + range). arrange 로 쓰면 에러:')
    try:
        np.arrange(5)  # 일부러 틀린 코드
    except AttributeError as e:
        print('    AttributeError =>', e)


def ch04_indexing_slicing_view():
    '''2차원 [행, 열] 접근, 그리고 View 함정.'''
    title(4, '인덱싱과 슬라이싱 - View 라는 함정')

    arr2d = np.array([[1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 11, 12]])

    print('  arr2d[1, 2]    :', arr2d[1, 2])  # 1행 2열
    print('  arr2d[1, :]    :', arr2d[1, :])  # 1행 전체
    print('  arr2d[:2, 1:3] :')
    print(arr2d[:2, 1:3])

    print()
    print('  --- 오늘의 함정: 슬라이싱은 복사가 아니라 View ---')

    python_list = [10, 20, 30, 40, 50]
    sliced = python_list[1:4]
    sliced[0] = 999
    print('  리스트: 슬라이스 수정 후 원본 =>', python_list, '(무사)')

    numpy_array = np.array([10, 20, 30, 40, 50])
    view = numpy_array[1:4]
    view[0] = 999
    print('  배열  : 슬라이스 수정 후 원본 =>', numpy_array, '(바뀜!)')

    safe = np.array([10, 20, 30, 40, 50])
    copied = safe[1:4].copy()  # 명시적 복사
    copied[0] = 999
    print('  .copy(): 복사본 수정 후 원본 =>', safe, '(무사)')


def ch05_boolean_fancy_indexing():
    '''조건 -> bool 마스크 -> True 만 통과.'''
    title(5, 'Boolean Indexing 과 Fancy Indexing')

    data = np.array([8000, 4500, 15000, 25000, 6000])

    mask = data > 10000
    print('  data           :', data)
    print('  data > 10000   :', mask, '  <= 조건의 정체는 bool 배열')
    print('  data[마스크]   :', data[mask], '            <= True 위치만 통과')

    small = np.array([1, 2, 3, 4, 5, 6])
    print('  짝수만 small[small % 2 == 0] :', small[small % 2 == 0])

    print()
    arr = np.array([10, 20, 30, 40, 50, 60, 70])
    print('  Fancy: arr[[0, 2, 5]] :', arr[[0, 2, 5]], ' (비연속 위치를 한 번에)')


def ch06_reshape():
    '''원소 수를 유지한 채 모양만 변경. -1 은 자동 계산.'''
    title(6, 'reshape - 모양 바꾸기')

    arr = np.arange(12)
    print('  원본 (12개):', arr)
    print()
    print('  reshape(3, 4):')
    print(arr.reshape(3, 4))
    print('  reshape(4, -1) => 열 자동 계산, shape:', arr.reshape(4, -1).shape)
    print('  reshape(-1, 2) => 행 자동 계산, shape:', arr.reshape(-1, 2).shape)

    print()
    print('  원소 수가 안 맞으면 에러가 납니다 (12 != 5 * 3):')
    try:
        arr.reshape(5, 3)  # 일부러 틀린 코드
    except ValueError as e:
        print('    ValueError =>', e)


def ch07_operations_broadcasting():
    '''요소별 연산과 브로드캐스팅.'''
    title(7, '배열 연산과 브로드캐스팅')

    단가 = np.array([4000, 4500, 5000])
    수량 = np.array([2, 1, 3])

    print('  단가 * 0.9 (배열 × 숫자) :', 단가 * 0.9)
    print('  단가 * 수량 (배열 × 배열):', 단가 * 수량)

    print()
    arr = np.array([[1, 2, 3],
                    [4, 5, 6]])
    print('  (2, 3) 배열 + 5 => 5 가 [[5,5,5],[5,5,5]] 처럼 확장되어 계산:')
    print(arr + 5)

    print()
    print('  [정리] 모양이 달라도 작은 쪽이 자동 확장 = 브로드캐스팅.')
    print('         이후 AI 과정의 "bias 더하기" 가 바로 이 연산입니다.')


def ch08_ufunc():
    '''모든 요소에 수학 함수를 한 번에.'''
    title(8, '유니버셜 함수 (ufunc) - 가볍게 훑기')

    arr = np.array([1, 4, 9, 16])
    print('  np.sqrt([1, 4, 9, 16]) :', np.sqrt(arr))

    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    print('  행렬 곱 np.dot(A, B) (= A @ B):')
    print(np.dot(a, b))

    print()
    print('  [정리] 지금은 sqrt 만 손에 익히고 나머지는 이름만 기억해도 충분합니다.')


def ch09_aggregation_axis():
    '''집계 함수, 그리고 axis 방향 감각.'''
    title(9, '집계 함수와 axis')

    매출 = np.array([8000, 4500, 15000, 25000, 6000])
    print('  매출          :', 매출)
    print('  .sum()        :', 매출.sum())
    print('  .mean()       :', 매출.mean())
    print('  .max()        :', 매출.max())
    print('  .argmax()     :', 매출.argmax(), ' <= 최댓값의 "위치"')

    print()
    매출표 = np.array([[8000, 4500, 15000],   # 서울
                      [6000, 5200, 10000]])  # 부산
    print('  매출표 (행=지역, 열=메뉴):')
    print(매출표)
    print('  sum(axis=0) 세로로 눌러 합침 =>', 매출표.sum(axis=0), ' (메뉴별 = 열별)')
    print('  sum(axis=1) 가로로 눌러 합침 =>', 매출표.sum(axis=1), '       (지역별 = 행별)')

    print()
    print('  [암기법] axis 는 "사라지는 방향". 결과 길이가 열 개수면 axis=0.')


# ==========================================================================
# Part B. Pandas
# ==========================================================================

def make_cafe_df():
    '''실습 노트북과 동일한 카페 판매 더미 데이터를 생성합니다. (seed=42)'''
    np.random.seed(42)
    n = 200
    지역 = np.random.choice(['서울', '부산', '대전', '광주'], n)
    메뉴 = np.random.choice(['아메리카노', '카페라떼', '바닐라라떼'], n)
    단가 = np.random.choice([4000, 4500, 5000, 5500, 6000], n)
    수량 = np.random.randint(1, 6, n)

    df = pd.DataFrame({'지역': 지역, '메뉴': 메뉴, '단가': 단가, '수량': 수량})
    df['매출'] = df['단가'] * df['수량']
    return df


def ch10_series_dataframe():
    '''Series = 한 열, DataFrame = 시트 전체.'''
    title(10, 'Pandas 란 - Series 와 DataFrame')

    data = {
        '이름': ['Alice', 'Bob', 'Charlie'],
        '나이': [25, 30, 35],
        '점수': [85.5, 90.3, 78.9],
    }
    df = pd.DataFrame(data)
    print(df)
    print()
    print('  한 열의 타입 type(df["이름"]) :', type(df['이름']).__name__, '(1차원 = 엑셀의 한 열)')
    print('  전체의 타입 type(df)          :', type(df).__name__, '(2차원 = 시트 전체)')
    print('  컬럼마다 자료형이 다름:')
    print(df.dtypes)


def ch11_create_dataframe():
    '''딕셔너리로 생성 + 새 컬럼 만들기.'''
    title(11, 'DataFrame 만들기와 새 컬럼')

    df = pd.DataFrame({
        '이름': ['철수', '영희', '민수'],
        '수학': [95, 80, 60],
        '영어': [88, 92, 70],
    })
    print(df)

    print()
    print('  기존 두 컬럼을 더해 새 컬럼 생성 (열 전체가 한 번에 계산됩니다):')
    df['총점'] = df['수학'] + df['영어']  # NumPy 벡터 연산 그대로
    print(df)

    print()
    print('  [정리] DataFrame 내부 값은 NumPy 배열. Part A 의 문법이 그대로 통합니다.')


def ch12_inspecting():
    '''head -> shape -> info -> describe -> value_counts 순서로 첫인사.'''
    title(12, 'Inspecting - 데이터와의 첫인사')

    df = make_cafe_df()

    print('  1) df.head(3):')
    print(df.head(3))
    print()
    print('  2) df.shape :', df.shape)
    print()
    print('  3) df.info():')
    df.info()
    print()
    print('  4) df.describe():')
    print(df.describe().round(1))
    print()
    print('  5) df["지역"].value_counts():')
    print(df['지역'].value_counts())


def ch13_select_loc_iloc():
    '''열 선택 [], 행 선택 loc / iloc.'''
    title(13, '열 선택과 행 선택 - [], loc, iloc')

    df = make_cafe_df()

    print('  한 열 df["메뉴"] => Series (앞 3개):')
    print(df['메뉴'].head(3))
    print()
    print('  여러 열 df[["지역", "매출"]] => DataFrame (앞 3개):')
    print(df[['지역', '매출']].head(3))

    print()
    print('  loc: 행 조건 + 열 이름 동시 지정 (서울의 매출만, 앞 3개):')
    print(df.loc[df['지역'] == '서울', '매출'].head(3))
    print()
    print('  iloc: 위치(정수) 기반. df.iloc[0, 1] =>', df.iloc[0, 1])

    print()
    print('  --- loc 슬라이싱 끝점 포함 확인 ---')
    small = pd.DataFrame({'값': [10, 20, 30, 40]}, index=['a', 'b', 'c', 'd'])
    print('  loc["a":"c"]  => 행 개수:', len(small.loc['a':'c']), ' (c 포함!)')
    print('  iloc[0:3]     => 행 개수:', len(small.iloc[0:3]), ' (3 미포함, 파이썬과 동일)')


def ch14_filtering():
    '''단일 / 복합 / 특수 조건 필터.'''
    title(14, '조건 필터링 - Pandas 의 심장')

    df = make_cafe_df()

    서울 = df[df['지역'] == '서울']
    print('  단일 조건: 지역 == 서울 =>', len(서울), '행')

    복합 = df[(df['매출'] >= 10000) & (df['메뉴'] == '아메리카노')]
    print('  복합 조건: (매출>=1만) & (아메리카노) =>', len(복합), '행')

    print()
    print('  괄호를 빼면 어떻게 되는지 직접 확인합니다:')
    try:
        df[df['매출'] >= 10000 & df['메뉴'] == '아메리카노']  # 일부러 틀린 코드
    except TypeError as e:
        print('    TypeError =>', str(e)[:60], '...')
    print('    => & 가 비교보다 먼저 계산되어 버립니다.')
    print('    => "복합 조건 = 괄호 + &/|" 를 한 몸으로 기억하세요.')

    print()
    print('  특수 조건 3종 세트:')
    print('    .isin([서울, 부산])       =>', len(df[df['지역'].isin(['서울', '부산'])]), '행')
    print('    .str.contains("라떼")     =>', len(df[df['메뉴'].str.contains('라떼')]), '행')
    print('    .notnull() (결측 아닌 행) =>', len(df[df['매출'].notnull()]), '행')


def ch15_preprocessing():
    '''결측치 처리(dropna/fillna)와 타입 변환(astype).'''
    title(15, '전처리 - 결측치와 타입')

    df = pd.DataFrame({
        '이름': ['철수', '영희', '민수', '지아'],
        '점수': [85.0, 92.5, np.nan, 78.0],   # np.nan = 결측치
    })
    print('  결측치가 섞인 데이터:')
    print(df)

    print()
    print('  방법 1) dropna(): 결측 행 제거 =>', len(df.dropna()), '행 남음 (데이터 손실)')
    print('  방법 2) fillna(0): 0 으로 대체 (일반적으로 선호):')

    df['점수'] = df['점수'].fillna(0)  # 1) 결측치를 먼저 채우고
    df['점수'] = df['점수'].astype(int)  # 2) 정수형으로 변환
    print(df)
    print('  변환 후 dtype:', df['점수'].dtype)

    print()
    print('  [주의] 순서가 반대면 (NaN 인 채 astype) 에러가 납니다. fillna 먼저!')


def ch16_groupby_pivot():
    '''Split-Apply-Combine, agg, pivot_table.'''
    title(16, 'groupby 와 pivot_table - 표를 요약하는 힘')

    df = make_cafe_df()

    print('  지역별 총매출 df.groupby("지역")["매출"].sum():')
    print(df.groupby('지역')['매출'].sum())

    print()
    print('  여러 집계 동시 (agg):')
    요약 = df.groupby('지역').agg(
        매출합=('매출', 'sum'),
        매출평균=('매출', 'mean'),
    )
    print(요약.round(0))

    print()
    print('  pivot_table: 지역(세로) × 메뉴(가로) 교차표:')
    피벗 = df.pivot_table(index='지역', columns='메뉴', values='매출', aggfunc='sum')
    print(피벗)

    print()
    print('  [구분법] 세로로 길게 => groupby, 바둑판 교차표 => pivot_table.')
    print('  [연결]   이 데이터가 실습 노트북 Step 4~8 의 df 와 완전히 같습니다.')


# ==========================================================================
# 실행부
# ==========================================================================

def main():
    print()
    print('#' * 70)
    print('#  NumPy & Pandas 자기주도 학습 - 실행 파일')
    print(f'#  numpy: {np.__version__} | pandas: {pd.__version__}')
    print('#  마크다운 가이드(numpy_pandas_guide.md)와 장 번호가 같습니다.')
    print('#' * 70)

    chapters = [
        ch01_what_is_numpy,
        ch02_ndarray_attributes,
        ch03_creation_functions,
        ch04_indexing_slicing_view,
        ch05_boolean_fancy_indexing,
        ch06_reshape,
        ch07_operations_broadcasting,
        ch08_ufunc,
        ch09_aggregation_axis,
        ch10_series_dataframe,
        ch11_create_dataframe,
        ch12_inspecting,
        ch13_select_loc_iloc,
        ch14_filtering,
        ch15_preprocessing,
        ch16_groupby_pivot,
    ]

    for chapter in chapters:
        chapter()
        pause()

    print()
    print('=' * 70)
    print(' 정리: 오늘 가져갈 5줄')
    print('=' * 70)
    print('  1. 배열 연산은 원소별로 한 번에. 반복문은 잊어라. (벡터화)')
    print('  2. NumPy 슬라이싱은 View. 원본을 지키려면 .copy().')
    print('  3. axis=0 은 세로로 눌러 열별 결과, axis=1 은 가로로 눌러 행별 결과.')
    print('  4. 필터링은 df[(조건1) & (조건2)]. 괄호 + &/|, and/or 금지.')
    print('  5. loc 은 이름 기반(끝점 포함!), iloc 은 위치 기반. i 는 integer.')
    print()
    print(' 다음 단계: 실습 노트북(실습2)의 TODO 1 에 도전하세요.')
    print()


if __name__ == '__main__':
    main()
