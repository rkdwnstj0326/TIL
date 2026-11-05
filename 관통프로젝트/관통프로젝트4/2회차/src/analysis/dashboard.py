"""화면 수치는 실제 공시 관측값으로만 계산한다. 제안 질문은 담당자 검토용이다."""
from src.analysis.complaint_trends import insurer_total, growth


def period_label(period):
    if 'Q' in period:
        year, quarter = period.split('Q')
        return f'{year}년 {quarter}분기'
    if 'H' in period:
        year, half = period.split('H')
        return f"{year}년 {'상반기' if half == '1' else '하반기'}"
    return f'{period}년'


def previous_quarter(period):
    year, quarter = map(int, period.split('Q'))
    return f'{year}Q{quarter-1}' if quarter > 1 else f'{year-1}Q4'


def snapshot(rows, company, period):
    current = [r for r in rows if r['company'] == company and r['period'] == period]
    previous = previous_quarter(period)
    total = insurer_total(rows, company, period)
    prior_total = insurer_total(rows, company, previous)
    regime=lambda p:'생명보험 별도 기준' if company=='교보생명' else '2024Q2 개선 이후' if p>='2024Q2' else '2024Q2 개선 이전'
    comparable=regime(period)==regime(previous)
    types = sorted([r for r in current if r['axis'] == '유형' and r['category'] != '합계'],
                   key=lambda r: (-r['count'], r['category']))
    total_row = next((r for r in current if r['axis']=='접수경로' and r['category']=='합계'), None)
    return {'company': company, 'period': period, 'rows': current, 'total': total,
            'previous_period': previous, 'previous_total': prior_total,
            'change': None if total is None or prior_total is None or not comparable else total-prior_total,
            'growth': None if total is None or prior_total is None or not comparable else growth(prior_total,total),
            'comparison_blocked':not comparable,'definition_regime':regime(period),
            'types': types, 'top_types': [r for r in types if r['count'] > 0][:3],
            'rate': total_row['rate_per_100k'] if total_row else None,
            'source_url': current[0]['source_url'] if current else None}


def review_question(category):
    """담당자 검토 질문. 사례가 선택 회사에서 발생했다는 의미가 아니다."""
    category={'지급':'보상(보험금)','판매':'보험모집','유지':'유지관리'}.get(category,category)
    return {
        '보상(보험금)': ('보험금 청구 때 어떤 자료와 보장 조건을 확인해야 할까요?',
                    '보험금 청구 진료비 영수증 추가 서류'),
        '보험모집': ('가입 과정에서 설명과 동의는 어떻게 확인했을까요?',
                 '유니버셜 종신보험 설명의무 해피콜'),
        '유지관리': ('해지된 계약을 다시 유지할 때 어떤 조건을 확인했을까요?',
                 '보험료 연체 계약 해지 부활'),
    }.get(category, ('비슷한 분쟁에서 어떤 약관과 사실을 확인했을까요?', '보험 약관 보상 기준'))
