import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 한글 폰트 설정 (환경에 따라 다를 수 있으나, Streamlit Cloud 배포 시 별도 설정 필요)
# 여기서는 기본 차트를 사용합니다.

st.set_page_config(page_title="학생 평가 기록지", page_icon="📝", layout="wide")

# --- 데이터 초기화 (세션 상태) ---
if 'eval_data' not in st.session_state:
    st.session_state.eval_data = pd.DataFrame(columns=[
        "날짜", "학생이름", "과목/영역", "성취도", "수업태도", "종합의견"
    ])

# --- 사이드바: 학생 명부 관리 ---
with st.sidebar:
    st.header("👤 학생 관리")
    student_list = st.text_area("학생 명단 (쉼표로 구분)", "김철수, 이영희, 박지성, 최바다").split(',')
    student_list = [s.strip() for s in student_list]
    
    st.divider()
    st.info("평가 후 아래 '데이터 초기화'를 누르면 모든 기록이 삭제됩니다.")
    if st.button("전체 데이터 초기화"):
        st.session_state.eval_data = pd.DataFrame(columns=["날짜", "학생이름", "과목/영역", "성취도", "수업태도", "종합의견"])
        st.rerun()

# --- 메인 화면 ---
st.title("👨‍🏫 학생 성취도 평가 기록지")
st.write("학습 활동 중 관찰한 학생의 성취도와 태도를 즉시 기록하세요.")

# --- 입력 섹션 ---
with st.expander("➕ 새 평가 기록 작성", expanded=True):
    with st.form("eval_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            eval_date = st.date_input("평가 날짜", datetime.now())
            target_student = st.selectbox("학생 선택", student_list)
        
        with col2:
            subject = st.text_input("과목 또는 활동명", placeholder="예: 국어(토론), 과학(실험)")
            score = st.select_slider("성취도 레벨", options=["매우 미흡", "미흡", "보통", "우수", "매우 우수"], value="보통")
