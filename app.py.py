import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# --- 설정 및 스타일 ---
st.set_page_config(page_title="AI 대학생 재무 관리 시스템", layout="wide")
st.title("📊 AI 기반 대학생 과소비 위험 감지 시스템")

# --- 데이터 초기화 (세션 상태) ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# --- 사이드바: 입력부 (보고서 설계 반영) ---
with st.sidebar:
    st.header("📌 기본 정보 입력")
    total_budget = st.number_input("이번 달 총 생활비 예산 (원)", min_value=0, value=500000, step=10000)
    
    st.divider()
    st.header("💰 지출 내역 입력")
    exp_date = st.date_input("날짜", value=date.today())
    exp_amount = st.number_input("금액 (원)", min_value=0, value=0, step=1000)
    exp_cat = st.selectbox("카테고리", ["식비", "교통비", "카페/간식", "취미/문화", "기타"])
    
    if st.button("지출 내역 추가"):
        st.session_state.expenses.append({"날짜": exp_date, "금액": exp_amount, "카테고리": exp_cat})
        st.success("내역이 추가되었습니다!")

# --- 데이터 계산 로직 (보고서 5페이지 순서도 반영) ---
today = date.today()
last_day = calendar.monthrange(today.year, today.month)[1]
remaining_days = last_day - today.day + 1

df = pd.DataFrame(st.session_state.expenses)
if not df.empty:
    total_spent = df['금액'].sum()
else:
    total_spent = 0

remaining_budget = total_budget - total_spent
# 하루 평균 사용 가능 금액 계산
avg_daily_limit = remaining_budget / remaining_days if remaining_days > 0 else 0

# 지출 속도 위험도 분석 (보고서 기준: 15,000원 / 7,000원) 
if avg_daily_limit >= 15000:
    risk_status = "안전"
    risk_color = "green"
elif avg_daily_limit >= 7000:
    risk_status = "적정"
    risk_color = "orange"
else:
    risk_status = "위험"
    risk_color = "red"

# --- 메인 화면: 대시보드 출력 ---
col1, col2, col3 = st.columns(3)
col1.metric("이번 달 남은 예산", f"{remaining_budget:,} 원")
col2.metric("남은 기간", f"{remaining_days} 일")
col3.metric("하루 평균 사용 가능액", f"{int(avg_daily_limit):,} 원")

st.divider()

# 지출 속도 상태 표시
st.subheader("⚠️ 현재 소비 속도 분석")
st.markdown(f"### 상태: :{risk_color}[{risk_status}]")

# AI 조언 (보고서 기반 맞춤형 코멘트)
st.subheader("🤖 AI 맞춤형 재무 조언")
if risk_status == "위험":
    st.warning(f"현재 소비 속도가 매우 빠릅니다! 하루에 **{int(avg_daily_limit):,}원** 이하로 지출해야 합니다. 불필요한 배달 음식이나 카페 지출을 줄여보세요.")
    st.info("💡 추천 금융 상품: 단기 자금 관리에 유리한 **'파킹통장'**을 활용해 남은 돈을 관리해보세요.")
elif risk_status == "적정":
    st.info("현재 소비 속도가 적절합니다. 목표 예산을 유지하기 위해 조금만 더 신경 써보세요!")
else:
    st.success("매우 훌륭한 소비 습관입니다! 남은 금액은 저축을 고려해보는 건 어떨까요?")
    st.info("💡 추천 금융 상품: 높은 금리를 제공하는 **'청년 우대형 청약통장'** 또는 **'적금'** 상품을 알아보세요.") [cite: 66-79]

# 지출 내역 차트
if not df.empty:
    st.divider()
    st.subheader("📈 카테고리별 지출 현황")
    cat_chart = df.groupby('카테고리')['금액'].sum()
    st.bar_chart(cat_chart)