from db_client import supabase
import streamlit as st

def sign_up(email, password):
    """새로운 사용자를 등록합니다."""
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        st.success("회원가입 성공! 이메일을 확인하여 인증해주세요.")
        return res
    except Exception as e:
        st.error(f"회원가입 오류: {e}")
        return None

def sign_in(email, password):
    """이메일과 비밀번호로 로그인합니다."""
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        # 세션 정보 저장
        st.session_state['user_session'] = res
        st.session_state['logged_in'] = True
        st.success("로그인 성공!")
        return res
    except Exception as e:
        st.error(f"로그인 오류: {e}")
        st.session_state['logged_in'] = False
        return None

def sign_out():
    """사용자를 로그아웃시킵니다."""
    try:
        supabase.auth.sign_out()
        # 세션 정보 초기화
        for key in st.session_state.keys():
            del st.session_state[key]
        st.info("로그아웃되었습니다.")
    except Exception as e:
        st.error(f"로그아웃 오류: {e}")