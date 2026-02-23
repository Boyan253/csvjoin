import csvjoin

LEFT = [{"id": "1", "name": "ada"}, {"id": "2", "name": "grace"}]
RIGHT = [{"id": "1", "city": "london"}, {"id": "3", "city": "york"}]


def test_inner_join_keeps_only_matches():
    fields, rows = csvjoin.join(LEFT, RIGHT, "id")
    assert fields == ["id", "name", "city"]
    assert rows == [{"id": "1", "name": "ada", "city": "london"}]

def test_left_join_keeps_unmatched_left():
    _, rows = csvjoin.join(LEFT, RIGHT, "id", how="left")
    assert len(rows) == 2
    assert rows[1] == {"id": "2", "name": "grace"}
