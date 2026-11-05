import json
from src.collection.client import ROOT
from src.analysis.dashboard import period_label, previous_quarter, snapshot


def test_quarter_labels_and_boundary():
    assert period_label('2026Q2')=='2026년 2분기'
    assert period_label('2026H1')=='2026년 상반기'
    assert previous_quarter('2026Q1')=='2025Q4'


def test_real_snapshot_uses_one_axis_only():
    rows=json.loads((ROOT/'data/processed/insurer_stats.json').read_text('utf-8'))
    result=snapshot(rows,'하나손해보험','2026Q2')
    assert result['total']==75 and result['change']==7
    assert result['top_types'][0]['category']=='보상(보험금)'
    assert result['top_types'][0]['count']==55
    result=snapshot(rows,'신한EZ손해보험','2026Q1')
    assert result['previous_total'] is None and result['growth'] is None


def test_missing_period_is_not_zero():
    result=snapshot([],'없는회사','2026Q2')
    assert result['total'] is None and result['rate'] is None and result['top_types']==[]
