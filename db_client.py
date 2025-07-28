from supabase import create_client, Client
import os

# Supabase 프로젝트 URL과 anon key
SUPABASE_URL = "https://mgbuemveocgoajoxdkqh.supabase.co"
SUPABASE_KEY = "sb_publishable_cqz893vXVD1aINyhtTWTeA_jyKOUYTP"

# 이 라인이 supabase 변수를 생성합니다. 이 코드가 누락되었을 가능성이 높습니다.
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)