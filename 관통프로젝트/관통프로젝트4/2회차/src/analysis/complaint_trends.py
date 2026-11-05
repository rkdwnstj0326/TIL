"""통계의 비교 기준을 먼저 확인한다. 익명 사례와 회사별 건수는 결합하지 않는다."""


def growth(previous, current):
    if previous < 0 or current < 0:
        raise ValueError('음수 민원 건수')
    return None if previous == 0 else (current - previous) / previous * 100


def comparable_periods(first, second):
    return (first['period_type'] == second['period_type'] and
            ('H' not in first['period'] or first['period'][-2:] == second['period'][-2:]))


def insurer_total(rows, company, period):
    # 총민원은 한 분류축에서만 계산한다. 세 축을 모두 더하면 세 배로 부풀려진다.
    selected = [r for r in rows if r['company'] == company and r['period'] == period
                and r['axis'] == '접수경로']
    if not selected:
        return None
    total = next((r for r in selected if r['category'] == '합계'), None)
    return total['count'] if total else sum(r['count'] for r in selected)


def validate_company_case_link(case, company):
    return bool(case.get('company_name')) and case['company_name'] == company
