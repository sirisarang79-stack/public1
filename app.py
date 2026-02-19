import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def draw_house():
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # 하우스 그리기 (원형 표적)
    circles = [
        {'radius': 6, 'color': 'white', 'edge': 'black'}, # 12피트
        {'radius': 4, 'color': '#3498db', 'edge': 'black'}, # 8피트 (블루)
        {'radius': 2, 'color': 'white', 'edge': 'black'}, # 4피트
        {'radius': 0.5, 'color': '#e74c3c', 'edge': 'black'} # 버튼 (레드)
    ]
    
    for circle in circles:
        c = plt.Circle((0, 0), circle['radius'], color=circle['color'], ec=circle['edge'], zorder=1)
        ax.add_artist(c)
        
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def calculate_score(red_stones, yellow_stones):
    # 하우스 안에 있는 스톤만 필터링 (반지름 6 이내)
    red_in = [s for s in red_stones if s['dist'] <= 6]
    yellow_in = [s for s in yellow_stones if s['dist'] <= 6]
    
    if not red_in and not yellow_in:
        return "0 : 0 (무득점)", None

    # 가장 가까운 스톤 찾기
    min_red = min([s['dist'] for s in red_in]) if red_in else 999
    min_yellow = min([s['dist'] for s in yellow_in]) if yellow_in else 999
    
    score = 0
    winner = ""
    
    if min_red < min_yellow:
        winner = "Red"
        # 상대편의 가장 가까운 스톤보다 더 안쪽에 있는 우리 스톤 개수 카운트
        for s in sorted([s['dist'] for s in red_in]):
            if s < min_yellow:
                score += 1
            else:
                break
    else:
        winner = "Yellow"
        for s in sorted([s['dist'] for s in yellow_in]):
            if s < min_red:
                score += 1
            else:
                break
                
    return f"{winner}팀 {score}점 획득!", winner

# --- Streamlit UI ---
st.title("🥌 컬링 점수 계산 시뮬레이터")
st.markdown("""
하우스 중심(버튼)에서 각 스톤까지의 거리를 입력해보세요. 
**상대방의 가장 가까운 스톤보다 더 안쪽에 있는 스톤들만** 점수로 인정됩니다!
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Red Team")
    red_count = st.number_input("레드 스톤 개수", 0, 8, 2)
    red_dists = [st.slider(f"레드 {i+1}번 거리", 0.0, 8.0, 1.0 + i) for i in range(red_count)]

with col2:
    st.subheader("🟡 Yellow Team")
    yellow_count = st.number_input("옐로우 스톤 개수", 0, 8, 2)
    yellow_dists = [st.slider(f"옐로우 {i+1}번 거리", 0.0, 8.0, 1.5 + i) for i in range(yellow_count)]

# 데이터 정리
red_stones = [{'dist': d, 'color': 'red'} for d in red_dists]
yellow_stones = [{'dist': d, 'color': 'yellow'} for d in yellow_dists]

# 점수 계산 및 결과 출력
result_text, winner = calculate_score(red_stones, yellow_stones)

st.divider()
st.header(result_text)

# 시각화
fig, ax = draw_house()
# 간단한 시각화를 위해 모든 스톤을 x축 상에 배치 (거리 표현용)
for s in red_stones:
    ax.scatter(s['dist'], 0, color='red', s=200, edgecolors='black', zorder=5)
for s in yellow_stones:
    ax.scatter(-s['dist'], 0, color='yellow', s=200, edgecolors='black', zorder=5)

st.pyplot(fig)

st.info("""
💡 **점수 규칙 가이드:**
1. 엔드 종료 시 하우스(원 안)에 스톤이 있어야 점수 기회가 생깁니다.
2. 중심에 가장 가까운 스톤을 가진 팀이 해당 엔드를 이깁니다.
3. 이긴 팀은 상대방의 '가장 중심에 가까운 스톤'보다 더 안쪽에 넣은 스톤 개수만큼 점수를 얻습니다.
""")
