import streamlit as st
import pandas as pd
# CRUD 및 로직 함수 임포트
from crud_functions import (
    get_all_employees, add_employee, update_employee_position, delete_employee,
    add_attendance, get_attendance_by_employee
)
from logic_functions import calculate_payroll, create_payslip_pdf
# 인증 함수 임포트
from auth_functions import sign_up, sign_in, sign_out

st.set_page_config(page_title="인사 관리 시스템", layout="wide")

# --- 1. 로그인 상태 확인 및 UI 분기 ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 로그인 화면
if not st.session_state['logged_in']:
    st.title("로그인 및 회원가입")
    
    choice = st.selectbox("선택", ["로그인", "회원가입"])

    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")

    if choice == "회원가입":
        if st.button("회원가입"):
            sign_up(email, password)
    else:
        if st.button("로그인"):
            sign_in(email, password)
            st.rerun()

# 메인 애플리케이션 화면 (로그인 성공 시)
else:
    st.sidebar.title("메뉴")
    
    # 로그아웃 버튼
    if st.sidebar.button("로그아웃"):
        sign_out()
        st.rerun()

    # --- 공통 데이터 로딩 ---
    employees = get_all_employees()
    employee_map = {emp['name']: emp['id'] for emp in employees} if employees else {}
    
    page = st.sidebar.radio("페이지 선택", ["직원 관리", "근태 관리", "급여 관리", "인사 통계"])
    
    st.title("👔 급여 및 인사 관리 시스템")
    st.header(f"{page} 페이지")
    st.divider()

    # --- 페이지별 UI 구현 (기존 코드와 거의 동일) ---
    if page == "직원 관리":
        # (기존 직원 관리 페이지 코드 붙여넣기)
        st.header("직원 목록")
        if employees:
            st.dataframe(employees, use_container_width=True)
        else:
            st.info("등록된 직원이 없습니다.")
        st.divider()

        with st.form("new_employee_form", clear_on_submit=True):
            st.subheader("신규 직원 추가")
            name = st.text_input("이름")
            department = st.text_input("부서")
            position = st.text_input("직책")
            hire_date = st.date_input("입사일")
            if st.form_submit_button("추가하기"):
                add_employee(name, department, position, hire_date)
                st.success(f"{name} 님을 추가했습니다.")
                # st.experimental_rerun() # Streamlit 버전 < 1.18.0
                st.rerun()

        st.divider()
        st.subheader("직원 정보 수정 및 삭제")
        if employee_map:
            target_name = st.selectbox("대상 직원 선택", list(employee_map.keys()))
            new_position = st.text_input("변경할 직책", key="update_pos")
            if st.button("직책 변경"):
                update_employee_position(target_name, new_position)
                st.success(f"{target_name} 님의 직책을 변경했습니다.")
                st.rerun()

            if st.button("직원 삭제", type="primary"):
                delete_employee(target_name)
                st.warning(f"{target_name} 님의 정보를 삭제했습니다.")
                st.rerun()
        # ... 이하 생략 ...

    elif page == "근태 관리":
        st.header("근태 기록")
        if employee_map:
            selected_name = st.selectbox("직원 선택", list(employee_map.keys()), key="att_emp")
            selected_employee_id = employee_map[selected_name]

            att_date = st.date_input("날짜")
            att_type = st.selectbox("근무 유형", ["정상", "지각", "조퇴", "휴가"])
            if st.button("근태 기록 저장"):
                add_attendance(selected_employee_id, att_date, att_type)
                st.success(f"{selected_name} 님의 {att_date} 근태 기록을 저장했습니다.")
            
            st.divider()
            st.subheader(f"{selected_name} 님 근태 기록 조회")
            year, month = att_date.year, att_date.month
            attendance_records = get_attendance_by_employee(selected_employee_id, year, month)
            st.dataframe(attendance_records, use_container_width=True)
        else:
            st.info("먼저 직원을 등록해주세요.")

    elif page == "급여 관리":
        # (기존 급여 관리 페이지 코드 붙여넣기)
        st.header("급여 계산 및 명세서 생성")
        if employee_map:
            selected_name = st.selectbox("급여 계산 대상 직원 선택", list(employee_map.keys()), key="sal_emp")
            selected_employee_id = employee_map[selected_name]
            
            year = st.number_input("연도", value=2025, key="sal_year")
            month = st.number_input("월", min_value=1, max_value=12, value=7, key="sal_month")

            if st.button("급여 계산 및 명세서 생성"):
                with st.spinner("처리 중..."):
                    payroll_data = calculate_payroll(selected_employee_id, month)
                    st.subheader(f"{year}년 {month}월 급여 계산 결과")
                    st.write(f"총 지급액: {payroll_data['gross_pay']:,} 원")
                    st.write(f"공제액: {payroll_data['deductions']:,} 원")
                    st.success(f"실 지급액: {payroll_data['net_pay']:,} 원")
                    
                    pdf_file = create_payslip_pdf(payroll_data, selected_name, year, month)
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="급여 명세서 다운로드",
                            data=f,
                            file_name=pdf_file,
                            mime="application/pdf"
                        )
        else:
            st.info("먼저 직원을 등록해주세요.")

    elif page == "인사 통계":
        st.header("인사 통계 대시보드")
        if employees:
            df = pd.DataFrame(employees)
            st.subheader("부서별 인원")
            dept_counts = df['department'].value_counts()
            st.bar_chart(dept_counts)

            st.subheader("직책별 분포")
            pos_counts = df['position'].value_counts()
            st.bar_chart(pos_counts)
        else:
            st.info("통계를 표시할 데이터가 없습니다.")
