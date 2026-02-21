from app.services import (
    calculate_composite_score,
    calculate_graham_index,
    calculate_peg_fair_price,
)


def test_calculate_graham_index() -> None:
    result = calculate_graham_index(eps=6.0, bps=5.0)
    assert result > 0


def test_calculate_peg_fair_price() -> None:
    assert calculate_peg_fair_price(eps=4.0, eps_growth_rate=10.0) == 40.0


def test_calculate_composite_score_formula() -> None:
    score = calculate_composite_score(roe=20.0, per=10.0, revenue_growth_pct=15.0)
    assert score == 30.0
