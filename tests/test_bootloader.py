import pytest

@pytest.mark.usefixtures("flash_bootloader")
@pytest.mark.order(1)
class TestBootloader:
    def test_bootloader_first(self):
        assert 41 == 42

    def test_bootloader_second(self):
        assert 43 == 43

    def test_bootloader_third(self):
        assert 44 == 44
