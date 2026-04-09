

# 겹침·협로를 반영한 위험장과 강화학습을 통한 도시 밀집환경 UAV 안전 항로 학습

---

## 개요

도심 환경에서 UAV의 안전한 항법을 위한 연구 프로젝트입니다.  
건물 밀집도, 협로(corridor), 사용자 성향(조심/과감)을 반영한 **Risk Field 기반 강화학습**을 목표로 합니다.

## Problem Definition

도심 UAV 운용에서는 다음과 같은 문제가 존재합니다:

- 건물 밀집 → 충돌 위험 증가
- 좁은 통로 → 고위험 구간 발생
- 사용자 성향 반영 필요 (조심 vs 과감)

---

### 1. Risk Field Modeling

건물 마스크로부터 연속적인 위험장을 생성합니다.

- Screened Poisson 기반 필드 생성
- Heavy-tail 확장 (완만한 영향 범위)
- 다중 건물 채널 분리

- FFT 기반 필터링으로 필드 생성 :contentReference[oaicite:1]{index=1}  
- 건물 주변 위험이 부드럽게 퍼짐

---

### 2. Overlap-aware Risk Enhancement

단순 거리 기반이 아니라:

- 겹침 개수 (Multiplicity)
- 겹침 강도 (Strength)
- 겹침 코어 (Core)

를 통해 **“진짜 위험한 구간 (협로)”을 강조**

---

### 3. Corridor-aware Risk

협로 위험을 별도로 모델링:

- 최근접 건물 거리 기반
- 협로 지수 적용

👉 좁은 통로일수록 위험 증가

---

### 4. Safety Parameter (User Intent)

사용자 성향을 직접 반영:

- safety = 0 → 공격적 (짧은 경로)
- safety = 1 → 안전 (우회 경로)

👉 위험장의 형태 자체가 변형됨

---

## 🧠 Reinforcement Learning

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

## 🏗️ Code Structure

```bash
risk_field/
├── poisson.py        # Screened Poisson field
├── combine.py        # strength / multiplicity / core
├── postprocess.py    # safety parameter