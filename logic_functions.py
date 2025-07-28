
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from crud_functions import get_salary_info, get_overtime_hours

# --- Payroll Logic ---
BASE_DEDUCTION_RATE = 0.1 # 세금 등 공제율 10% 가정

def calculate_payroll(employee_id, month):
    """직원의 월별 급여를 계산합니다."""
    salary_info = get_salary_info(employee_id)
    base_salary = salary_info.get('base_salary', 0)

    overtime_hours = get_overtime_hours(employee_id, month)
    overtime_pay = overtime_hours * 20000 # 시간당 20,000원 가정

    gross_pay = base_salary + overtime_pay
    deductions = gross_pay * BASE_DEDUCTION_RATE
    net_pay = gross_pay - deductions

    return {
        "gross_pay": gross_pay,
        "deductions": deductions,
        "net_pay": net_pay
    }

# --- PDF Generation Logic ---
def create_payslip_pdf(payroll_data, employee_name, year, month):
    """PDF 급여 명세서를 생성합니다."""
    # 한글 폰트 등록
    # 로컬에 'NanumGothic.ttf' 폰트 파일이 있어야 합니다.
    try:
        pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))
    except Exception:
        print("경고: 나눔고딕 폰트 파일을 찾을 수 없습니다. 폰트 없이 진행합니다.")
        
    file_name = f"payslip_{employee_name}_{year}_{month}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    
    # 등록한 한글 폰트 사용
    c.setFont('NanumGothic', 12)
    
    c.drawString(100, 750, f"{year}년 {month}월 급여 명세서 ({employee_name})")
    c.line(100, 745, 500, 745)
    c.drawString(100, 725, f"총 지급액: {payroll_data['gross_pay']:,} 원")
    c.drawString(100, 705, f"공제액: {payroll_data['deductions']:,} 원")
    c.drawString(100, 685, f"실 지급액: {payroll_data['net_pay']:,} 원")
    
    c.save()
    return file_name