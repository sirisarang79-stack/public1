import streamlit as st
import pandas as pd
from datetime import datetime

# --- 페이지 설정 ---
st.set_page_config(page_title="우리반 학급일지", page_icon="📅", layout="centered")

# --- 데이터 저장소 초기화 ---
# 세션 상태(Session State)를 사용하여 앱이 새로고침되어도 데이터가 유지되게 합니다.
if 'logs' not in st.session_state:
    st.session_state.logs = pd.DataFrame(columns=["날짜", "날씨", "출석현황", "주요학습내용", "특이사항"])

# --- 헤더 ---
st.title("🍎 오늘의 학급일지")
st.write(f"오늘은 **{datetime.now().strftime('%Y년 %m월 %d일')}** 입니다.")
st.divider()

# --- 입력 섹션 ---
with st.form("log_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        date = st.date_input("날짜 선택", datetime.now())
        weather = st.selectbox("오늘의 날씨", ["맑음", "흐림", "비", "눈", "미세먼지 나쁨"])
        
    with col2:
        attendance = st.text_input("출석 현황 (예: 전원 출석 / 결석 1명)", placeholder="출석 정보를 입력하세요")

    subject_content = st.text_area("주요 학습 내용", placeholder="교시별 핵심 내용을 간단히 적어주세요.")
    special_note = st.text_area("학급 특이사항 및 전달사항", placeholder="학생 상담, 사고, 공지사항 등")

    submit_button = st.form_submit_button("일지 저장하기")

# --- 데이터 저장 로직 ---
if submit_button:
    new_data = {
        "날짜": date.strftime('%Y-%m-%d'),
        "날씨": weather,
        "출석현황": attendance,
        "주요학습내용": subject_content,
        "특이사항": special_note
    }
    # 새로운 데이터를 기존 데이터프레임에 추가
    st.session_state.logs = pd.concat([st.session_state.logs, pd.DataFrame([new_data])], ignore_index=True)
    st.success("오늘의 기록이 성공적으로 저장되었습니다!")

# --- 조회 섹션 ---
st.divider()
st.subheader("📚 누적 학급 기록")

if not st.session_state.logs.empty:
    # 최신순으로 정렬하여 보여주기
    display_df = st.session_state.logs.sort_values(by="날짜", ascending=False)
    st.dataframe(display_df, use_container_width=True)
    
    # CSV 다운로드 기능
    csv = display_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 전체 일지 다운로드 (CSV)",
        data=csv,
        file_name=f"class_log_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
else:
    st.info("아직 작성된 일지가 없습니다. 첫 번째 일지를 작성해 보세요!")

# --- 오늘의 한마디 (위트) ---
st.sidebar.title("💡 선생님의 한마디")
quote = st.sidebar.text_input("오늘의 응원 메시지", "얘들아, 오늘도 수고했어!")
st.sidebar.info(f"✨ {quote}")
