from todolist_hexagon.result import Ok, Result, Err


def test_ok_result() -> None:
    result : Result[None, str] = Ok(None)
    assert result.is_ok()
    assert not result.is_err()
    assert result == Ok(None)


def test_ok_can_have_value() -> None:
    result : Result[str, str] = Ok("value")
    assert result.is_ok()
    assert not result.is_err()
    assert result == Ok("value")
    assert result.unwrap() == "value"
    assert result.map(lambda x: x.upper()) == Ok("VALUE")
    assert result.and_then(lambda x: Ok(x.upper())) == Ok("VALUE")
    assert result.and_then(lambda x: Err("other error")) == Err("other error")



def test_err_result() -> None:
    result : Result[None, str] = Err("any error")
    assert not result.is_ok()
    assert result.is_err()
    assert result == Err("any error")
    assert result.map(lambda x: x) == Err("any error")
    assert result.and_then(lambda x: Err("other error")) == Err("any error")


def test_err_result_can_have_no_value() -> None:
    result : Result[None, None] = Err(None)
    assert not result.is_ok()
    assert result.is_err()
    assert result == Err(None)