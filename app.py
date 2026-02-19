import streamlit as st
import pandas as pd
import numpy as np

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="기후변화 생물영향 모니터",
    page_icon="🍊",
    layout="wide"
)

# --- 제목 및 헤더 ---
st.title("🌏 기후변화와 생태계의 변화")
st.markdown("""
이 대시보드는 기후 변화가 **생물 다양성**과 **서식지**에 미치는 영향을 시각화합니다.
데이터를 통해 과거를 돌아보고, 시뮬레이션을 통해 미래를 예측해 봅시다.
""")
st.divider()

# --- 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 설정 및 메뉴")
    menu = st.radio("메뉴 선택", ["대시보드 (Global Data)", "생태계 시뮬레이터", "한국의 사례"])
    st.info("💡 **Update:** 감귤 재배지 북상 데이터가 추가되었습니다.")

# --- 데이터 생성 함수 ---
@st.cache_data
def load_temp_data():
    years = np.arange(1850, 2101)
    anomaly = [0.05 * np.exp(0.025 * (y - 1900)) if y > 1900 else np.random.normal(0, 0.1) for y in years]
    data = pd.DataFrame({'Year': years, 'Temperature Anomaly (°C)': anomaly})
    return data

df = load_temp_data()

# --- 1. 대시보드 탭 ---
if menu == "대시보드 (Global Data)":
    st.subheader("📈 지구 평균 기온 상승 추이")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.line_chart(df.set_index('Year'), color="#FF4B4B")
    with col2:
        current_anomaly = df[df['Year'] == 2024]['Temperature Anomaly (°C)'].values[0]
        st.metric(label="2024년 기준", value=f"+{current_anomaly:.2f}°C", delta="산업화 이전 대비")
        st.warning("상승 추세가 지속되고 있습니다.")

    st.markdown("### 🔍 주요 멸종 위기종 데이터")
    species_data = {
        "이름": ["북극곰", "산호초", "바다거북", "황제펭귄"],
        "위험 요인": ["해빙 감소", "해
