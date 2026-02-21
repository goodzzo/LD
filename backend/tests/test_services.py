from app.services import calculate_valuation_score


def test_calculate_valuation_score_returns_reasonable_range() -> None:
    score = calculate_valuation_score(
        revenue_growth=0.2,
        operating_margin=0.3,
        pe_ratio=25,
        debt_to_equity=0.7,
        free_cash_flow_b=20,
    )
    assert 0 <= score <= 100


def test_calculate_valuation_score_penalizes_high_pe() -> None:
    low_pe = calculate_valuation_score(0.1, 0.2, 20, 1.0, 10)
    high_pe = calculate_valuation_score(0.1, 0.2, 80, 1.0, 10)
    assert low_pe > high_pe
