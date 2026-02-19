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
            
        with col3:
            attitude = st.radio("수업 태도", ["매우 적극", "참여도 좋음", "집중 필요", "기타"], horizontal=True)
            
        comment = st.text_area("교사의 종합 의견 (관찰 기록)", placeholder="학생의 구체적인 행동이나 변화를 기록하세요.")
        
        submit = st.form_submit_button("평가 저장")

if submit:
    new_eval = {
        "날짜": eval_date.strftime('%Y-%m-%d'),
        "학생이름": target_student,
        "과목/영역": subject,
        "성취도": score,
        "수업태도": attitude,
        "종합의견": comment
    }
    st.session_state.eval_data = pd.concat([st.session_state.eval_data, pd.DataFrame([new_eval])], ignore_index=True)
    st.toast(f"{target_student} 학생의 기록이 저장되었습니다!", icon='✅')

# --- 데이터 시각화 및 조회 ---
st.divider()

tab1, tab2 = st.tabs(["📊 통계 요약", "📋 전체 기록 조회"])

with tab1:
    if not st.session_state.eval_data.empty:
        st.subheader("💡 성취도 분포")
        # 성취도 점수화 (시각화를 위해)
        score_map = {"매우 미흡": 1, "미흡": 2, "보통": 3, "우수": 4, "매우 우수": 5}
        temp_df = st.session_state.eval_data.copy()
        temp_df['score_val'] = temp_df['성취도'].map(score_map)
        
        # 학생별 평균 성취도 차트
        avg_scores = temp_df.groupby('학생이름')['score_val'].mean()
        st.bar_chart(avg_scores)
        st.caption("학생별 성치도 평균 (5점 만점)")
    else:
        st.info("기록된 데이터가 없어 통계를 표시할 수 없습니다.")

with tab2:
    if not st.session_state.eval_data.empty:
        # 필터 기능
        search_name = st.text_input("🔍 학생 이름으로 검색")
        filtered_df = st.session_state.eval_data
        if search_name:
            filtered_df = filtered_df[filtered_df['학생이름'].str.contains(search_name)]
            
        st.dataframe(filtered_df, use_container_width=True)
        
        # CSV 다운로드
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("내보내기 (CSV)", data=csv, file_name="student_eval.csv", mime="text/csv")
    else:
        st.write("작성된 평가 내역이 없습니다.")
