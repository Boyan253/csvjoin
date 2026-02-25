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


def test_outer_join_adds_unmatched_right():
    _, rows = csvjoin.join(LEFT, RIGHT, "id", how="outer")
    ids = sorted(r["id"] for r in rows)
    assert ids == ["1", "2", "3"]

def test_clashing_columns_get_a_suffix():
    left = [{"id": "1", "name": "ada"}]
    right = [{"id": "1", "name": "lovelace"}]
    fields, rows = csvjoin.join(left, right, "id")
    assert fields == ["id", "name", "name_r"]
    assert rows[0]["name_r"] == "lovelace"


def test_duplicate_keys_produce_a_row_each():
    right = [{"id": "1", "city": "a"}, {"id": "1", "city": "b"}]
    _, rows = csvjoin.join(LEFT, right, "id")
    assert len(rows) == 2
