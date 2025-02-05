from pricer.BSPricer import BSPricer
import pytest

def test_main():
    c = BSPricer('call', 0.25, 100, 95, 0.2, 0.03, True)
    assert c.price_basic_option() == pytest.approx(7.378954534893353)
