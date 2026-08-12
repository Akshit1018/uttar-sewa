from backend.services.mala_counter import BEADS_PER_CYCLE, sankalpa_remaining


def test_sankalpa_is_a_vow_not_a_streak():
    assert sankalpa_remaining(0, 1) == 1
    assert sankalpa_remaining(1, 1) == 0
    assert sankalpa_remaining(3, 1) == 0
    assert BEADS_PER_CYCLE == 108
