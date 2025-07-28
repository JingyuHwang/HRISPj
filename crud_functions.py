from db_client import supabase

# --- Employee CRUD ---

def add_employee(name, department, position, hire_date):
    """새로운 직원을 'employees' 테이블에 추가합니다."""
    try:
        data, count = supabase.table('employees').insert({
            "name": name,
            "department": department,
            "position": position,
            "hire_date": str(hire_date)
        }).execute()
        return data
    except Exception as e:
        print(f"직원 추가 오류: {e}")
        return None

from db_client import supabase

def get_all_employees():
    """모든 직원 정보를 조회합니다."""
    try:
        # 'order('name')' can be added to sort by name
        response = supabase.table('employees').select('*').execute()
        return response.data
    except Exception as e:
        print(f"직원 조회 오류: {e}")
        return []

def update_employee_position(name, new_position):
    """직원의 직책을 업데이트합니다."""
    try:
        data, count = supabase.table('employees').update({'position': new_position}).eq('name', name).execute()
        return data
    except Exception as e:
        print(f"직책 변경 오류: {e}")
        return None

def delete_employee(name):
    """이름으로 특정 직원을 삭제합니다."""
    try:
        data, count = supabase.table('employees').delete().eq('name', name).execute()
        return data
    except Exception as e:
        print(f"직원 삭제 오류: {e}")
        return None

# --- Attendance CRUD ---

def add_attendance(employee_id, date, attendance_type):
    """직원의 근태 기록을 추가합니다."""
    try:
        record = {
            "employee_id": employee_id,
            "date": str(date),
            "attendance_type": attendance_type,
        }
        data, count = supabase.table('attendance').insert(record).execute()
        return data
    except Exception as e:
        print(f"근태 기록 추가 오류: {e}")
        return None

def get_attendance_by_employee(employee_id, year, month):
    """특정 직원의 월별 근태 기록을 조회합니다."""
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-31" # 월의 마지막 날을 계산하는 로직으로 개선 가능
    try:
        response = supabase.table('attendance').select('*') \
            .eq('employee_id', employee_id) \
            .gte('date', start_date) \
            .lte('date', end_date) \
            .order('date') \
            .execute()
        return response.data
    except Exception as e:
        print(f"근태 기록 조회 오류: {e}")
        return []

# --- Salary CRUD (Placeholder) ---
# 실제 구현 시에는 이 함수들을 구체화해야 합니다.
def get_salary_info(employee_id):
    # 예시: 모든 직원의 기본급을 3,000,000원으로 가정
    return {'base_salary': 3000000}

def get_overtime_hours(employee_id, month):
     # 예시: 초과 근무 시간을 10시간으로 가정
    return 10