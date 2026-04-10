

# 겹침·협로를 반영한 위험장과 강화학습을 통한 도시 밀집환경 UAV 안전 항로 학습

![title](docs/figures/title.png)
---

## 1. 개요

도심 환경에서 UAV의 안전한 항법을 위한 연구 프로젝트입니다.  
건물 밀집도, 협로(corridor), 사용자 성향(조심/과감)을 반영한 **Risk Field 기반 강화학습**을 목표로 합니다.

---

## 2. 문제 정의

도심 UAV 운용에서는 다음과 같은 문제가 존재합니다:

- 건물 밀집 → 충돌 위험 증가
- 좁은 통로 → 고위험 구간 발생
- 사용자 성향 반영 필요 (조심 vs 과감)

---

## 3. 관련 연구

### 3.1. APF(Artificial Potential Field) 

로봇이나 드론의 경로 계획 방법 중 하나로, **목표를 잡아당기는 힘(인력), 장애물은 밀어내는 가상의 힘(척력)** 을 만들어서 이동시키는 방법
최근 다양한 UAV 경로 계획, 장애물 회피 연구에서 활용되고 있음[1][2].


<div align="center">
  <img src=".\docs\figures\apf.webp" width="800"/>
</div>

#### 3.1.1. APF(Artificial Potential Field) 종류

##### 인력

**Parabolic function**

<div align="center">
  <img src=".\docs\figures\parabolic.png" width="400"/>
</div>

$$
U^{a_p}(Q) = \frac{1}{2}k^a(d(Q))^2
$$

**Conical function**

<div align="center">
  <img src=".\docs\figures\conical.png" width="400"/>
</div>

$$
\begin{cases}
U^{a}(Q) = \frac{1}{2} k^{a} d^{2}(Q) \\
f^{a}(Q) = -\nabla U^{a}(Q) = k^{a} (Q_g - Q)
\end{cases}
$$

##### 척력

**FIRAS function**

<div align="center">
  <img src=".\docs\figures\repulsive.png" width="400"/>
</div>

$$
U_i^{r}(Q) =
\begin{cases}
\frac{1}{2} k_i^{r} \left( \frac{1}{d_i(Q)} - \frac{1}{d_i^{0}} \right)^2 & \text{if } d_i(Q) \le d_i^{0} \\
0 & \text{otherwise}
\end{cases}
$$

---

### 3.2 하모닉 필드(Harmonic field)

라플라스 방정식을 만족하는 필드로, 균형 잡힌 장(field)를 만들 수 있음. 기존 연구 로봇 경로 계획에 하모닉 필드를 응용한 연구가 있음[3].

<div align="center">
  <img src=".\docs\figures\poisson.png" width="400"/>
</div>

$$
\nabla^2 u = 0
$$


---

### 3.3. 심층 강화학습 (Deep reinforcement learning)

강화학습과 딥러닝을 결합한 방법으로 경험을 통해 스스로 최적의 행동을 배우는 **신경망 기반 의사결정 방법**

<div align="center">
  <img src=".\docs\figures\drl.png" width="600"/>
</div>

#### 3.3.1. On policy 방식

**현재 정책으로 행동**하고, 그 데이터로 바로 학습; **rollout 개념**
예시) PPO(Proximal Policy Optimization) [4]

<div align="center">
  <img src=".\docs\figures\orl.png" width="400"/>
</div>


#### 3.3.2. Off policy 방식

**이전(다른) 정책 포함** 모은 데이터로 학습, **Replay buffer 개념**
예시) Deep Q-Network(DQN) [5]

<div align="center">
  <img src=".\docs\figures\offrl.png" width="400"/>
</div>


---

## 4. 제안 방법

<div align="center">
  <img src=".\docs\figures\mission.png" width="500"/>
</div>


### 4.1. 위험장 생성

<div align="center">
  <img src=".\docs\figures\structure.png" width="700"/>
</div>


건물 마스크로부터 연속적인 위험장을 생성합니다.

#### 4.1.1. 하모닉 필드 기반 필드 생성

건물 6개를 채널 별로 나눠 필드 생성

<div align="center">
  <img src=".\docs\figures\harmony.png" width="500"/>
</div>

$$
\Phi = \mathcal{F}^{-1} \left( \frac{\mathcal{F}(B)}{(1 + \lambda k^2)^q} \right)
$$

---

#### 4.1.2. 중첩 위험장 강화

단순 거리 기반 → 위험장이 겹치는 부분은 크게 강화

##### (1) 겹침 개수 (Multiplicity)

<div align="center">
  <img src=".\docs\figures\m.png" width="400"/>
</div>

여러 채널이 동시에 활성화되는 정도를 측정

$$
M(x) = \sum_{i=1}^{N} \sigma\left(\frac{\phi_i(x) - \tau}{\beta}\right)
$$

##### (2) 겹침 강도 (Strength)

<div align="center">
  <img src=".\docs\figures\s.png" width="400"/>
</div>


몇 개의 건물이 동시에 영향을 주는지 측정

$$
M(x) = \frac{1}{\alpha} \log \left( \sum_{i=1}^{N} e^{\alpha \phi_i(x)} \right)
$$


##### (3) 겹침 코어 (Core)

<div align="center">
  <img src=".\docs\figures\c.png" width="400"/>
</div>


단일 위험보다 **진짜 위험한 중심 영역** 추출

$$
C(x) = \sum_{i \lt j} \phi_i(x)\phi_j(x)
$$

---

### 4.2. 지역 위험 지도 | 전역 위험 지도

**전역 위험 지도**는 위성사진에서 장애물의 영향을 반영하여 넓은 범위의 경로 흐름을 형성하는데 사용된다.
**지역 위험 지도**는 센서 기반 위험 정보를 통해 국소적인 의사결정을 위해 사용된다.

<div align="center">
  <img src=".\docs\figures\global_local.png" width="600"/>
</div>

#### 4.2.1. 샘플링 기반 후보 경로 생성

RRT(Rapidly-exploring Random Trees Star)을 이용해 여러 경로를 생성한다.

<div align="center">
  <img src=".\docs\figures\rrt.png" width="300"/>
</div>

---

## 5. Safety Parameter (User Intent)

<div align="center">
  <img src=".\docs\figures\safety_level.png" width="700"/>
</div>


사용자 성향을 직접 반영:

- safety = 0 → 공격적 (짧은 경로)
- safety = 1 → 안전 (우회 경로)

**위험장의 형태 자체가 변형됨**

---

##  Reinforcement Learning

**본 구조는 이미지 기반 위험 정보와 상태 벡터를 함께 사용하는 강화학습 네트워크이다.**
입력으로 다중 비트맵 형태의 환경 정보(장애물, 위험장)을 CNN을 통해 특징(feature)으로 추출하고, 이를 벡터로 변환한다.
이후 위치 등 상태 정보와 결합하여 FC(Fully Connected Network)에 입력되며, **최종적으로 정책을 출력**한다.

<div align="center">
  <img src=".\docs\figures\rf.png" width="900"/>
</div>


### State

- UAV position
- goal direction
- risk field (potential)
- obstacle mask

### Action

- 방향 + 이동 크기 (continuous)

### Reward

- 목표 접근
- 시간 패널티
- 충돌 패널티
- 위험도 감소 보상

---

참고 문헌 <br/>
[1] Z. Pan, C. Zhang, Y. Xia, H. Xiong and X. Shao, "An Improved Artificial Potential Field Method for Path Planning and Formation Control of the Multi-UAV Systems," in IEEE Transactions on Circuits and Systems II: Express Briefs, vol. 69, no. 3, pp. 1129-1133, March 2022, doi: 10.1109/TCSII.2021.3112787. <br/>
[2] Z. Pan, C. Zhang, Y. Xia, H. Xiong and X. Shao, "An Improved Artificial Potential Field Method for Path Planning and Formation Control of the Multi-UAV Systems," in IEEE Transactions on Circuits and Systems II: Express Briefs, vol. 69, no. 3, pp. 1129-1133, March 2022, doi: 10.1109/TCSII.2021.3112787. <br/>
[3] Connolly, Christopher I., and Roderic A. Grupen. "The applications of harmonic functions to robotics." Journal of robotic Systems 10.7 (1993): 931-946. <br/>
[4] Schulman, J., Wolski, F., Dhariwal, P., Radford, A., & Klimov, O. (2017). Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347. <br/>
[5] Mnih, V., Kavukcuoglu, K., Silver, D., Graves, A., Antonoglou, I., Wierstra, D., & Riedmiller, M. (2013). Playing atari with deep reinforcement learning. arXiv preprint arXiv:1312.5602.