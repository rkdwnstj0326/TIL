################ 문자 유형 판별 메서드 ################
# =============================================================
# 숫자 판별 3형제: isdecimal / isdigit / isnumeric
# - 셋 다 "문자열이 숫자인가?"를 판별하지만 '인정 범위'가 다름
# - 좁음 --------------------------------> 넓음
#   isdecimal  <  isdigit  <  isnumeric
# - 공통점: 소수점(.)과 부호(-)는 셋 다 숫자로 보지 않음 (문자가 섞인 것)
#   => '123.45', '-123'은 세 메서드 모두 False
# =============================================================

# =============================================================
# isdecimal - 가장 엄격: 오직 0~9 십진수만 True
# - 로마 숫자(Ⅳ), 분수(½), 지수(²)는 모두 False
# =============================================================

# isdecimal() : 가장 엄격한 기준을 적용, 오직 일반적인 십진수 숫자(0-9)만 True로 인식
print('isdecimal() 메서드 예시:')
print('"12345".isdecimal():', '12345'.isdecimal())
print('"123.45".isdecimal():', '123.45'.isdecimal())
print('"-123".isdecimal():', '-123'.isdecimal())
print('"Ⅳ".isdecimal():', 'Ⅳ'.isdecimal())
print('"½".isdecimal():', '½'.isdecimal())
print('"²".isdecimal():', '²'.isdecimal())
print()

# =============================================================
# isdigit - 중간: 십진수 + 지수 표현(², ³)까지 True
# - 여전히 로마 숫자(Ⅳ), 분수(½)는 False
#   => isdecimal과의 차이가 '²'에서 드러남 (decimal은 False, digit은 True)
# =============================================================

# isdigit() : 일반 숫자뿐만 아니라 지수 표현(²)도 True로 인식
print('isdigit() 메서드 예시:')
print('"12345".isdigit():', '12345'.isdigit())
print('"123.45".isdigit():', '123.45'.isdigit())
print('"-123".isdigit():', '-123'.isdigit())
print('"Ⅳ".isdigit():', 'Ⅳ'.isdigit())
print('"½".isdigit():', '½'.isdigit())
print('"²".isdigit():', '²'.isdigit())
print()

# =============================================================
# isnumeric - 가장 넓음: 로마 숫자(Ⅳ), 분수(½), 지수(²)까지 모두 True
# - '숫자의 의미를 가진' 유니코드 문자를 폭넓게 인정
#   => Ⅳ, ½ 에서 isdigit과의 차이가 드러남
# - 정리: 실무에서 "정수 입력인지" 검증할 때는 가장 엄격한
#         isdecimal이 안전 (½, Ⅳ 같은 값을 걸러내야 하므로)
# =============================================================

# isnumeric() : 일반 숫자, 로마 숫자, 분수, 지수 등 다양한 형태의 숫자 표현을 True로 인식
print('isnumeric() 메서드 예시:')
print('"12345".isnumeric():', '12345'.isnumeric())
print('"123.45".isnumeric():', '123.45'.isnumeric())
print('"-123".isnumeric():', '-123'.isnumeric())
print('"Ⅳ".isnumeric():', 'Ⅳ'.isnumeric())
print('"½".isnumeric():', '½'.isnumeric())
print('"²".isnumeric():', '²'.isnumeric())
