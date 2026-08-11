[toc]

# MLP 모델링 실습: PyTorch로 나만의 신경망 만들기

> 딥러닝 라이브러리 **PyTorch**로 가장 기본 모델인 **MLP(Multi-Layer Perceptron)** 를 직접 만들고 학습시키는 과정을 단계별로 진행합니다.
> 교재 `1-2. MLP` 의 개념을 **코드로 옮기는 다리** 역할을 하는 자료입니다.

---

## 이 문서를 읽는 법

교재에서 배운 학습 4단계가 이 문서의 어디에 있는지 먼저 확인하고 시작하세요.

| 교재 개념 | 이 문서 | 핵심 코드 |
|---|---|---|
| 모델 구조 (입력층·은닉층·출력층) | Part 2 | `nn.Sequential(...)` |
| ① 순전파 | Part 3-1 | `logits = model(x)` |
| ② 손실 계산 | Part 3-2 | `loss = criterion(logits, y)` |
| ③ 역전파 | Part 3-2 | `loss.backward()` |
| ④ 가중치 업데이트 | **Part 4** | `optimizer.step()` |
| 과적합 방지 (Dropout) | Part 4-3 | `model.train()` / `model.eval()` |

---

## 실습 환경 준비

```bash
# 가상환경 생성 및 활성화
# 패키지 설치
pip install torch numpy
```

```python
# 이 문서의 모든 코드는 아래 import를 전제로 합니다.
import torch
import torch.nn as nn
```

---



# Part 1. PyTorch 기초

## 1-1. 왜 PyTorch를 사용할까요?

PyTorch는 딥러닝 모델을 쉽고 유연하게 만들 수 있도록 도와주는 파이썬 라이브러리입니다.
과학 계산에 널리 쓰이는 NumPy와 사용법이 매우 유사하지만, 딥러닝에 최적화된 두 가지 기능을 추가로 제공합니다.

- **GPU를 활용한 연산 가속**: CPU 대신 GPU의 병렬 처리 능력으로 텐서(행렬) 연산을 매우 빠르게 처리합니다.
- **자동 미분 (AutoGrad)**: 모델 학습에 필수인 '미분'을 자동으로 계산해 줍니다.

### 연산 장치(device) 지정하기

GPU를 쓰려면 **모델과 데이터를 같은 장치로 보내야** 합니다. 이 두 줄을 습관처럼 쓰세요.

```python
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'사용 중인 장치: {DEVICE}')
```

```text
[예상 출력]
사용 중인 장치: cpu        # GPU가 있으면 cuda
```

> **자주 만나는 에러**
> `RuntimeError: Expected all tensors to be on the same device`
> => 모델은 GPU에 있는데 데이터는 CPU에 있을 때 납니다. 데이터에도 `.to(DEVICE)` 를 붙여 주세요.



## 1-2. 기본 단위: 텐서(Tensor) 다루기

**텐서(Tensor)** 는 PyTorch의 가장 기본이 되는 데이터 구조로, 쉽게 말해 **다차원 배열**입니다.

| 차원 | 이름 | 예시 |
|---|---|---|
| 0차원 | 스칼라 | `3.14` |
| 1차원 | 벡터 | `[1, 2, 3]` |
| 2차원 | 행렬 | `[[1, 2], [3, 4]]` |
| 3차원 이상 | 텐서 | 이미지 배치 등 |

NumPy의 `ndarray`와 거의 같지만, **GPU 가속과 자동 미분을 탑재한 NumPy의 파워 버전**이라고 생각하면 쉽습니다.

```python
# (2, 3) 행렬과 (4, 3) 행렬을 만듭니다.
x = torch.rand(2, 3)
y = torch.ones(4, 3)

print('x의 shape:', x.shape)
print('y의 shape:', y.shape)

# 행렬 곱셈(@)은 '앞 행렬의 열 수 == 뒤 행렬의 행 수'여야 성립합니다.
# x는 (2, 3), y.T는 (3, 4) 이므로 결과는 (2, 4)가 됩니다.
result = x @ y.T
print('x @ y.T 의 shape:', result.shape)

# 검증: shape이 예상과 일치하는지 확인
assert result.shape == (2, 4), 'shape 계산이 잘못되었습니다'
print('✅ shape 검증 통과')
```

```text
[예상 출력]
x의 shape: torch.Size([2, 3])
y의 shape: torch.Size([4, 3])
x @ y.T 의 shape: torch.Size([2, 4])
✅ shape 검증 통과
```

>  **딥러닝 디버깅의 90%는 shape 싸움입니다.**
> 에러가 나면 가장 먼저 `print(텐서.shape)` 를 찍어 보세요. `mat1 and mat2 shapes cannot be multiplied` 에러는 거의 항상 이 규칙을 어긴 경우입니다.



## 1-3. PyTorch의 핵심: 자동 미분(AutoGrad)

모델이 '학습'을 하려면, 예측이 틀렸을 때 각 파라미터를 **어느 방향으로 얼마나** 조절할지 알아야 합니다.
이 '조절 방향과 양'을 **기울기(Gradient)** 라고 하며, 기울기를 구하는 과정이 **미분**입니다.

**경사 하강법(Gradient Descent)** 은 이 기울기를 이용해 손실(Loss)을 점진적으로 줄여나가는 최적화 알고리즘입니다.

> **경사 하강법 업데이트 공식**
>
> ```
> 새 파라미터 = 기존 파라미터 - (학습률 × 기울기)
>
> θ_new = θ_old - η · ∇L
> ```
>
> - **θ (세타)**: 모델의 파라미터 (가중치 w, 편향 b)
> - **η (에타)**: 학습률(Learning Rate). 기울기 방향으로 얼마나 크게 이동할지 정하는 **보폭**
> - **L**: 손실 함수. 예측이 얼마나 틀렸는지를 나타내는 지표
> - **∇L**: 손실 L을 파라미터로 편미분한 기울기. 손실이 가장 가파르게 **증가**하는 방향입니다.
>   우리는 손실을 **줄이고** 싶으므로 마이너스를 붙여 빼 주는 것입니다.

PyTorch의 **AutoGrad** 는 이 복잡한 기울기 계산을 자동으로 처리합니다.
텐서에 `requires_grad=True` 를 주면 해당 텐서에 가해지는 모든 연산을 추적하고, `backward()` 호출 한 번으로 모든 기울기를 계산해 냅니다.

```python
# requires_grad=True로 설정하면 이 텐서에 대한 모든 연산이 추적됩니다.
x = torch.tensor([2.0, 3.0], requires_grad=True)

# y = x^2 + 3x + 1
y = x**2 + 3 * x + 1

# backward()는 스칼라(숫자 하나)에 대해서만 호출할 수 있으므로 합을 구합니다.
z = y.sum()

# 역전파 실행: z를 x에 대해 미분합니다.
z.backward()

# 계산된 기울기는 x.grad에 저장됩니다.
print('x의 기울기:', x.grad)
```

```text
[예상 출력]
x의 기울기: tensor([7., 9.])
```



### 손으로 검증해 보기

이 예제는 **직접 검산이 가능**합니다. 반드시 한 번 해 보세요.

```
y = x² + 3x + 1  을 x로 미분하면  =>  dy/dx = 2x + 3

x = 2.0 일 때  ->  2(2) + 3 = 7
x = 3.0 일 때  ->  2(3) + 3 = 9

=> tensor([7., 9.])  ✅ 코드 출력과 일치
```

```python
# 코드로도 검증해 봅시다.
expected = torch.tensor([7.0, 9.0])
assert torch.allclose(x.grad, expected), '기울기 계산 결과가 다릅니다'
print('✅ 미분 결과 검증 통과')
```

>  **여기서 꼭 알아야 할 성질: 기울기는 덮어쓰이지 않고 '누적'됩니다.**
> 위 셀을 **두 번 실행하면** `x.grad` 가 `[14., 18.]` 로 두 배가 됩니다.
> 이것이 뒤에서 배울 `optimizer.zero_grad()` 가 필요한 이유입니다. (Part 4-2)



---



# Part 2. 신경망의 설계도: MLP 이해하기

MLP는 여러 개의 **선형 계층(Linear Layer)** 사이에 **비선형 활성화 함수** 를 끼워 층층이 쌓아 올린 모델입니다.

> - **입력층 (Input Layer)**: 데이터가 처음 들어오는 입구
> - **은닉층 (Hidden Layer)**: 데이터의 특징을 추출·변환하는 중간 처리 과정. 깊어질수록 복잡한 패턴을 학습
> - **출력층 (Output Layer)**: 최종 예측 결과를 내보내는 출구

이 문서에서는 **실습 파일과 동일한 규격**으로 모델을 만듭니다.

```
입력 64 (8x8 손글씨 이미지를 펼친 값)
   -> 은닉 128 -> 은닉 64
   -> 출력 10 (숫자 0~9)
```



## 2-1. 신경망 모듈 `nn.Module`

PyTorch의 모든 신경망 모델은 `nn.Module` 을 상속받아 만듭니다.
`nn.Module` 은 여러 층과 학습 가능한 파라미터(가중치·편향)를 체계적으로 관리해 주는 **설계도**입니다.

- `__init__()`: 모델에 필요한 **부품 목록** (레이어, 활성화 함수 등)을 정의
- `forward()`: 데이터가 그 부품들을 **어떤 순서로 통과할지**, 즉 순전파를 정의

>  `__init__` 이 부품 목록, `forward` 가 조립 설명서라고 생각하세요.



## 2-2. 방법 1: 기본에 충실하게 (`nn.Module`)

가장 기본적인 방법은 `__init__` 에서 레이어를 하나씩 정의하고, `forward` 에서 흐름을 직접 작성하는 것입니다.

```python
class SimpleMLP(nn.Module):
    """가장 기본적인 형태의 MLP 모델입니다.

    레이어를 하나씩 정의하고 forward에서 흐름을 직접 작성하는 방식으로,
    데이터가 어떤 순서로 흐르는지 눈으로 확인하기 좋습니다.

    Args:
        input_dim (int): 입력 특성의 개수 (예: 8x8 이미지 -> 64)
        hidden_dim (int): 은닉층 뉴런 개수
        output_dim (int): 출력 클래스 개수 (예: 숫자 0~9 -> 10)
    """

    def __init__(self, input_dim, hidden_dim, output_dim):
        # nn.Module의 생성자를 반드시 먼저 호출해야 합니다.
        super().__init__()

        # nn.Linear: y = xW^T + b 형태의 선형 변환 레이어.
        # 내부적으로 가중치(W)와 편향(b)을 자동 생성하고 무작위로 초기화합니다.
        self.fc1 = nn.Linear(input_dim, hidden_dim)

        # nn.ReLU: 대표적인 비선형 활성화 함수. ReLU(x) = max(0, x)
        # 음수는 0으로, 양수는 그대로 통과시켜 모델에 '비선형성'을 부여합니다.
        self.relu = nn.ReLU()

        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        """순전파를 정의합니다.

        Args:
            x (torch.Tensor): (배치 크기, input_dim) 형태의 입력 텐서

        Returns:
            torch.Tensor: (배치 크기, output_dim) 형태의 예측 점수(logits)
        """
        x = self.fc1(x)   # 선형 변환
        x = self.relu(x)  # 비선형 활성화
        x = self.fc2(x)   # 출력층
        return x
```

>  **출력층 뒤에 활성화 함수가 없는 것은 실수가 아닙니다.** 이유는 Part 3-2에서 설명합니다.



## 2-3. 방법 2: 똑똑하고 간결하게 (`nn.Sequential`)

데이터가 순차적으로 흐르는 대부분의 경우, `nn.Sequential` 을 쓰면 훨씬 간결합니다.
여러 레이어를 컨테이너에 묶어 **순서대로 실행**해 주는 도구입니다.

```python
class SequentialMLP(nn.Module):
    """nn.Sequential을 사용해 간결하게 정의한 MLP 모델입니다.

    Linear -> ReLU -> Dropout 세트를 두 번 반복한 뒤 출력층으로 연결합니다.
    실습 파일에서 사용하는 것과 동일한 구조입니다.

    Args:
        input_dim (int): 입력 특성의 개수. 기본값 64
        hidden_dims (tuple): 은닉층 뉴런 개수 두 개. 기본값 (128, 64)
        output_dim (int): 출력 클래스 개수. 기본값 10
        dropout (float): 드롭아웃 확률. 기본값 0.2
    """

    def __init__(self, input_dim=64, hidden_dims=(128, 64), output_dim=10, dropout=0.2):
        super().__init__()
        h1, h2 = hidden_dims

        self.net = nn.Sequential(
            # 입력층 -> 첫 번째 은닉층
            nn.Linear(input_dim, h1),
            nn.ReLU(),
            # nn.Dropout: 과적합 방지용 규제 기법.
            # 학습 중 p의 확률로 뉴런을 랜덤하게 꺼서
            # 특정 뉴런에 과도하게 의존하는 것을 막습니다.
            nn.Dropout(p=dropout),
            # 첫 번째 은닉층 -> 두 번째 은닉층
            nn.Linear(h1, h2),
            nn.ReLU(),
            nn.Dropout(p=dropout),
            # 두 번째 은닉층 -> 출력층
            nn.Linear(h2, output_dim),
        )

    def forward(self, x):
        """순전파를 정의합니다.

        Args:
            x (torch.Tensor): (배치 크기, input_dim) 형태의 입력 텐서

        Returns:
            torch.Tensor: (배치 크기, output_dim) 형태의 예측 점수(logits)
        """
        return self.net(x)
```



### 두 방식 비교

| 항목 | `SimpleMLP` (방법 1) | `SequentialMLP` (방법 2) |
|---|---|---|
| 코드 길이 | 길다 | 짧다 |
| 흐름 파악 | `forward`에 명시적으로 보임 | 컨테이너 안에 압축됨 |
| 분기·조건 처리 | 자유롭게 가능 | 어려움 (순차 실행만) |
| 실무 사용 빈도 | 복잡한 모델에서 사용 | 단순한 모델에서 주로 사용 |

>  둘은 우열 관계가 아닙니다. 데이터가 **한 줄로 흐르면 Sequential**, 중간에 갈라지거나 합쳐지면 **직접 `forward` 작성** 이라고 기억하세요.



---



# Part 3. 순전파와 역전파 실행해 보기

## 3-1. 모델 생성 및 순전파 실행

```python
# 재현성 확보: 시드를 고정하면 매번 같은 초기 가중치가 만들어집니다.
# (가중치는 무작위로 초기화되므로, 고정하지 않으면 실행할 때마다 결과가 달라집니다)
torch.manual_seed(42)

model = SequentialMLP(input_dim=64, hidden_dims=(128, 64), output_dim=10).to(DEVICE)
print(model)

# 임의의 더미 데이터 (배치 크기 4, 입력 특성 64)
dummy_input = torch.rand(4, 64).to(DEVICE)

# 순전파 실행. model(x)는 내부적으로 model.forward(x)를 호출합니다.
logits = model(dummy_input)

print('\n입력 shape :', dummy_input.shape)
print('출력 shape :', logits.shape)

# 검증
assert logits.shape == (4, 10), '출력 shape이 (배치 크기, 클래스 수)가 아닙니다'
print('✅ 순전파 검증 통과')
```

```text
[예상 출력]
SequentialMLP(
  (net): Sequential(
    (0): Linear(in_features=64, out_features=128, bias=True)
    (1): ReLU()
    (2): Dropout(p=0.2, inplace=False)
    (3): Linear(in_features=128, out_features=64, bias=True)
    (4): ReLU()
    (5): Dropout(p=0.2, inplace=False)
    (6): Linear(in_features=64, out_features=10, bias=True)
  )
)

입력 shape : torch.Size([4, 64])
출력 shape : torch.Size([4, 10])
✅ 순전파 검증 통과
```

>  **모델을 출력하면 층에 번호가 붙습니다.** `(0)`이 첫 번째 `Linear`, `(6)`이 출력층입니다.
> 나중에 특정 층에 접근할 때 `model.net[0]` 처럼 이 번호를 씁니다.



### 파라미터 개수 세어 보기

```python
total_params = sum(p.numel() for p in model.parameters())
print(f'전체 학습 파라미터 개수: {total_params:,}개')
```

```text
[예상 출력]
전체 학습 파라미터 개수: 17,034개
```

```
검산)
(64 x 128 + 128) + (128 x 64 + 64) + (64 x 10 + 10)
= 8,320 + 8,256 + 650
= 17,034  ✅

각 항의 뒷부분(+128, +64, +10)이 편향(bias)입니다.
```



## 3-2. 손실 계산과 역전파 실행

순전파로 얻은 예측값을 정답과 비교해 **손실(Loss)** 을 계산하고, **역전파** 로 각 파라미터의 기울기를 구합니다.

```python
# 1. 입력과 정답 레이블 준비 (배치 크기 2)
torch.manual_seed(0)
dummy_input = torch.rand(2, 64).to(DEVICE)

# CrossEntropyLoss는 정수형(long) 레이블을 기대합니다.
# 값은 '몇 번째 클래스가 정답인가'를 뜻하는 인덱스입니다.
dummy_labels = torch.tensor([3, 7]).to(DEVICE)

# 2. 순전파
logits = model(dummy_input)

# 3. 손실 계산 (다중 클래스 분류의 표준)
criterion = nn.CrossEntropyLoss()
loss = criterion(logits, dummy_labels)
print(f'계산된 손실(Loss): {loss.item():.4f}')

# 4. 역전파 실행 전: 기울기는 아직 None입니다.
print('역전파 전, 첫 번째 Linear 층의 기울기:', model.net[0].weight.grad)

# 5. 역전파 실행! 이 한 줄이 모든 파라미터의 기울기를 자동 계산합니다.
loss.backward()

# 6. 역전파 실행 후: .grad에 값이 채워집니다.
print('역전파 후, 기울기 shape:', model.net[0].weight.grad.shape)

# 검증
assert model.net[0].weight.grad is not None, '기울기가 계산되지 않았습니다'
assert model.net[0].weight.grad.shape == (128, 64), '기울기 shape이 가중치와 달라야 합니다'
print('✅ 역전파 검증 통과')
```

```text
[예상 출력]
계산된 손실(Loss): 2.3xxx        # 아래 설명 참고
역전파 전, 첫 번째 Linear 층의 기울기: None
역전파 후, 기울기 shape: torch.Size([128, 64])
✅ 역전파 검증 통과
```



### 손실값이 왜 2.3 근처인가?

이 숫자는 **우연이 아니라 예측 가능한 값**입니다. 학습 전 모델은 아무것도 모르므로 10개 클래스에 거의 균등한 확률(각 0.1)을 줍니다.

```
교차 엔트로피 = -ln(정답 클래스에 준 확률)
             = -ln(1/10)
             = ln(10)
             ≈ 2.303
```

> 학습을 시작했는데 초기 loss가 `ln(클래스 수)` 근처가 아니라면, 데이터나 레이블 설정이 잘못됐을 가능성이 높습니다. 10클래스면 2.3, 2클래스면 0.69(= ln 2). 이 숫자를 외워두면 디버깅이 빨라집니다.



### 출력층에 Softmax를 넣지 않는 이유

가장 많이 틀리는 부분입니다.

```python
# 틀린 코드
nn.Linear(64, 10),
nn.Softmax(dim=1)      # CrossEntropyLoss와 함께 쓰면 Softmax가 두 번 적용됨

# 맞는 코드
nn.Linear(64, 10)      # 여기서 끝. 이 출력을 'logits'라고 부릅니다
```

`nn.CrossEntropyLoss` 내부에는 **이미 Softmax(정확히는 LogSoftmax)가 포함**되어 있습니다.
모델 끝에 또 넣으면 이중 적용되어 기울기가 뭉개지고 학습이 제대로 되지 않습니다.

| 용어 | 뜻 |
|---|---|
| **logits** | Softmax를 통과하기 **전**의 날것 점수. 범위 제한 없음 |
| **확률** | Softmax를 통과한 뒤의 값. 전부 더하면 1 |

> 실제로 예측 결과를 확인할 때는 `logits.argmax(dim=1)` 을 쓰면 됩니다.
> Softmax는 순서를 바꾸지 않으므로, **가장 큰 logit이 곧 가장 확률이 높은 클래스**입니다.



---



# Part 4. 학습 루프 완성하기

> 여기까지가 교재의 ①②③단계입니다. **④단계인 '실제 가중치 업데이트'가 아직 남았습니다.**



## 4-1. 옵티마이저 붙이기

역전파는 "각 가중치를 어느 방향으로 얼마나 고쳐야 하는지"를 **계산만** 합니다.
그 지침대로 **실제로 값을 바꾸는 것**이 옵티마이저입니다.

```python
# Adam: 현재 사실상 표준 옵티마이저
#   lr           = 학습률(보폭). 1e-3(=0.001)이 Adam의 관례적 기본값
#   weight_decay = L2 규제. 가중치가 지나치게 커지는 것을 억제 (과적합 방지)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
```

>  `model.parameters()` 를 넘겨주는 순간, 옵티마이저는 이 모델의 모든 가중치와 편향을 관리 대상으로 잡습니다.



## 4-2. 학습 4단계를 코드 5줄로

```python
# 교재의 학습 4단계 = 이 5줄이 전부입니다.

logits = model(inputs)              # 1. 순전파   : 일단 예측해 본다
loss = criterion(logits, labels)    # 2. 손실 계산 : 얼마나 틀렸나 재본다

optimizer.zero_grad()               #    칠판 지우기 (아래 설명)
loss.backward()                     # 3. 역전파   : 누구 책임인지 계산
optimizer.step()                    # 4. 업데이트 : 실제로 가중치를 고친다
```



### `zero_grad()` 는 왜 필요한가

Part 1-3에서 확인했듯 **PyTorch의 기울기는 덮어쓰이지 않고 누적**됩니다.
지우지 않으면 1번째 반성 + 2번째 반성 + 3번째 반성이 뒤엉켜 엉뚱한 방향으로 학습됩니다.

```python
# 누적되는 성질을 직접 확인해 봅시다.
model.zero_grad()

loss = criterion(model(dummy_input), dummy_labels)
loss.backward()
first = model.net[0].weight.grad.clone()

# zero_grad() 없이 한 번 더 backward
loss = criterion(model(dummy_input), dummy_labels)
loss.backward()
second = model.net[0].weight.grad.clone()

print('한 번 backward 후 기울기 합계 :', first.abs().sum().item())
print('두 번 backward 후 기울기 합계 :', second.abs().sum().item())
print('=> 값이 커졌다면 누적되고 있다는 뜻입니다')
```

> **순서 암기법: "지우고 → 계산하고 → 적용한다"** (`zero_grad` -> `backward` -> `step`)



## 4-3. `train()` / `eval()` / `no_grad()` 3종 세트

우리 모델에는 **Dropout** 이 들어 있습니다. Dropout은 학습할 때와 평가할 때 동작이 달라야 합니다.

| 코드 | 언제 | 하는 일 |
|---|---|---|
| `model.train()` | 학습할 때 | Dropout **ON** (뉴런을 랜덤하게 끔) |
| `model.eval()` | 평가·추론할 때 | Dropout **OFF** (전부 켬) |
| `with torch.no_grad():` | 평가·추론할 때 | 기울기 계산 생략 -> 메모리 절약 + 속도 향상 |

```python
# 모드에 따라 결과가 달라지는 것을 직접 확인해 봅시다.
torch.manual_seed(1)
sample = torch.rand(1, 64).to(DEVICE)

model.train()
out1 = model(sample)
out2 = model(sample)
print('train 모드 - 같은 입력, 두 번 실행이 동일한가?:', torch.allclose(out1, out2))

model.eval()
with torch.no_grad():
    out3 = model(sample)
    out4 = model(sample)
print('eval  모드 - 같은 입력, 두 번 실행이 동일한가?:', torch.allclose(out3, out4))
```

```text
[예상 출력]
train 모드 - 같은 입력, 두 번 실행이 동일한가?: False
eval  모드 - 같은 입력, 두 번 실행이 동일한가?: True
```

>  **`model.eval()` 을 빠뜨리면** 평가할 때도 뉴런이 랜덤하게 꺼져서
> **"실행할 때마다 정확도가 달라져요"** 라는 증상이 나타납니다.



## 4-4. 전체 학습 루프 (완성본)

지금까지 배운 것을 하나로 합치면 아래가 됩니다. **이 형태가 모든 딥러닝 코드의 표준 골격**입니다.

```python
def train_one_epoch(model, loader, optimizer, criterion, device):
    """한 에포크 동안 모델을 학습시킵니다.

    Args:
        model (nn.Module): 학습시킬 모델
        loader (DataLoader): 학습 데이터를 배치 단위로 공급하는 로더
        optimizer (torch.optim.Optimizer): 가중치를 업데이트할 옵티마이저
        criterion (nn.Module): 손실 함수
        device (str): 연산 장치 ('cuda' 또는 'cpu')

    Returns:
        tuple[float, float]: (평균 손실, 정확도)
    """
    model.train()  # 학습 모드: Dropout ON

    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in loader:
        inputs, labels = inputs.to(device), labels.to(device)

        logits = model(inputs)              # 1. 순전파
        loss = criterion(logits, labels)    # 2. 손실 계산

        optimizer.zero_grad()               #    기울기 초기화
        loss.backward()                     # 3. 역전파
        optimizer.step()                    # 4. 가중치 업데이트

        running_loss += loss.item() * labels.size(0)
        correct += (logits.argmax(dim=1) == labels).sum().item()
        total += labels.size(0)

    return running_loss / total, correct / total


def evaluate(model, loader, criterion, device):
    """모델을 평가합니다. 가중치를 업데이트하지 않습니다.

    Args:
        model (nn.Module): 평가할 모델
        loader (DataLoader): 검증 또는 테스트 데이터 로더
        criterion (nn.Module): 손실 함수
        device (str): 연산 장치 ('cuda' 또는 'cpu')

    Returns:
        tuple[float, float]: (평균 손실, 정확도)
    """
    model.eval()  # 평가 모드: Dropout OFF

    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():  # 기울기 계산 생략
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)

            logits = model(inputs)
            loss = criterion(logits, labels)

            running_loss += loss.item() * labels.size(0)
            correct += (logits.argmax(dim=1) == labels).sum().item()
            total += labels.size(0)

    return running_loss / total, correct / total
```

> **두 함수의 차이는 딱 세 군데입니다.**
> `train()` vs `eval()` / `no_grad()` 유무 / `zero_grad`-`backward`-`step` 3줄 유무.
> 나머지는 완전히 동일합니다. 이 대칭 구조를 눈에 익혀 두세요.



---



# Part 5. 자주 만나는 에러 정리

| 증상 / 에러 메시지 | 원인 | 해결 |
|---|---|---|
| `mat1 and mat2 shapes cannot be multiplied` | 층 사이 차원이 안 맞음 | `nn.Linear(a, b)` 의 `b` 와 다음 층의 `a` 를 일치시킬 것 |
| `Expected all tensors to be on the same device` | 모델과 데이터의 장치가 다름 | 데이터에도 `.to(DEVICE)` 적용 |
| `loss` 가 줄지 않음 | 학습률이 너무 작음 | `lr` 을 1e-4 -> 1e-3 으로 올려 보기 |
| `loss` 가 `nan` | 학습률이 너무 큼 (오버슈팅) | `lr` 을 1e-3 -> 1e-4 로 낮추기 |
| 정확도가 실행할 때마다 달라짐 | 평가 시 `model.eval()` 누락 | 평가 함수 첫 줄에 `model.eval()` 추가 |
| 초기 loss가 `ln(클래스 수)` 와 크게 다름 | 레이블 설정 오류 가능성 | 레이블이 0부터 시작하는 정수인지 확인 |
| 학습이 전혀 안 되고 loss가 요동침 | 출력층에 Softmax 중복 적용 | 마지막 층은 `nn.Linear` 로 끝낼 것 |
| `element 0 of tensors does not require grad` | `no_grad()` 안에서 `backward()` 호출 | 학습 코드는 `no_grad()` 블록 밖으로 |

---

