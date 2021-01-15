import pytest

@pytest.mark.order(3)
class TestGPIO:
    def test_first(self):
        assert 1 == 1

    def test_second(self):
        assert 2 == 2
