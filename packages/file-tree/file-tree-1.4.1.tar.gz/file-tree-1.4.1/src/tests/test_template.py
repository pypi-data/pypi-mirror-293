"""Tests the basic Placeholder and Template classes underlying the main FileTree."""
from unittest import mock

import pytest

from file_tree import template


def test_fill_single():
    """Template can be filled with single values."""
    t = template.Template(None, "{subject}_{session}")
    with pytest.raises(KeyError):
        t.format_single(template.Placeholders({"subject": "A"}))
    assert t.format_single(
        template.Placeholders({"subject": "A", "session": "B"})
    ) == str("A_B")
    assert t.placeholders() == ["subject", "session"]


def test_fill_single_optional():
    """Optional placeholder can be filled with single value or is removed."""
    t = template.Template(None, "{subject}[_{session}]")
    assert t.format_single(template.Placeholders({"subject": "A"})) == str("A")
    assert t.format_single(
        template.Placeholders({"subject": "A", "session": "B"})
    ) == str("A_B")
    assert t.placeholders() == ["subject", "session"]

    assert t.placeholders(valid=["subject"]) == ["subject"]
    assert t.placeholders(valid=["subject", "session"]) == ["subject", "session"]
    with pytest.raises(ValueError):
        t.placeholders(valid=["session"])


def test_single_nested():
    """Placeholders can be nested in each other."""
    t = template.Template(None, "{A}_{B}")
    placeholders = template.Placeholders(
        {
            "A": "A_{B}",
            "B": "B_{C}_{D}",
            "C": "C_{D}",
            "D": "D",
        }
    )
    assert t.format_single(placeholders) == str("A_B_C_D_D_B_C_D_D")
    assert t.placeholders() == ["A", "B"]


def test_fill_multi():
    """Placeholders can be set to multiple values returning xarray datasets."""
    t = template.Template(None, "s{subject}[_{session}]")
    res = t.format_mult(template.Placeholders(subject=("01", "02", "03")))
    assert res.shape == (3,)
    assert list(res.data) == [str(n) for n in ["s01", "s02", "s03"]]
    assert list(res["subject"]) == ["01", "02", "03"]

    res = t.format_mult(
        template.Placeholders(subject=("01", "02", "03"), session=("A", "B"))
    )
    assert res.ndim == 2
    assert list(res["subject"]) == ["01", "02", "03"]
    assert list(res["session"]) == ["A", "B"]
    assert res.sel(subject="02", session="A") == str("s02_A")
    assert res.sel(subject="03", session="B") == str("s03_B")


def test_multi_nested():
    """Returning xarray datasets also works for nested placeholders."""
    t = template.Template(None, "{A}_{B}")
    placeholders = template.Placeholders(
        {
            "A": ("A_{B}", "A2_{C}"),
            "B": "B_{D}",
            "C": ["C_{D}", "C2_{B}"],
            "D": "D",
        }
    )
    res = t.format_mult(placeholders)
    assert res.ndim == 2
    assert list(res["A"]) == list(placeholders["A"])
    assert list(res["C"]) == list(placeholders["C"])
    assert res.sel(A="A_{B}", C="C_{D}") == str("A_B_D_B_D")
    assert res.sel(A="A_{B}", C="C2_{B}") == str("A_B_D_B_D")
    assert res.sel(A="A2_{C}", C="C_{D}") == str("A2_C_D_B_D")
    assert res.sel(A="A2_{C}", C="C2_{B}") == str("A2_C2_B_D_B_D")


def test_fill_typed():
    """Placholders can have types, which are respected when formatting."""
    t = template.Template(None, "{A}_{A:d}_{A:.2f}")
    assert t.format_single(template.Placeholders(A="3")) == str("3_3_3.00")
    assert t.format_single(template.Placeholders(A=3)) == str("3_3_3.00")
    assert t.format_single(template.Placeholders(A=3.1234)) == str("3.1234_3_3.12")
    with pytest.raises(ValueError):
        t.format_single(template.Placeholders(A="text"))


@mock.patch("file_tree.template.glob")
def test_get_all_placeholders_simple(mock_glob):
    """Placeholders can be inferred based on files existing on disk."""
    t = template.Template(None, "{A}_{B}")
    mock_glob.return_value = ["foo_bar", "foo2_bar", "foo_baz", "some_thing"]
    new_vars = t.get_all_placeholders(template.Placeholders({}))
    mock_glob.assert_called_with("*_*")
    mock_glob.assert_called_once()
    assert len(new_vars) == 2
    assert new_vars["A"] == ["foo", "foo2", "some"]
    assert new_vars["B"] == ["bar", "baz", "thing"]


@mock.patch("file_tree.template.glob")
def test_get_all_placeholders(mock_glob):
    """Placeholders can be inferred based on files existing on disk."""
    for template_string in [
        "{A}{B:d}",
        "{A}{C/B:d}",
        "{C/A}{C/B:d}",
        "{C/A}{B:d}",
    ]:
        t = template.Template(None, template_string)
        mock_glob.reset_mock()
        mock_glob.return_value = ["foo", "bar1", "bar3"]
        new_vars = t.get_all_placeholders(template.Placeholders({}))
        mock_glob.assert_called_with("*")
        mock_glob.assert_called_once()
        assert len(new_vars) == 2
        assert new_vars["A"] == ["bar"]
        assert new_vars["B"] == [1, 3]


@mock.patch("file_tree.template.glob")
def test_get_all_placeholders_optional(mock_glob):
    """Optional placeholders supported when inferring files on disk."""
    t = template.Template(None, "{A}[_age{B:d}]")

    def glob_return(input):
        if input == "*":
            return ("foo", "bar_age1", "bar_age2")
        elif input == "*_age*":
            return ("bar_age1", "bar_age2")
        raise AssertionError()

    mock_glob.side_effect = glob_return
    new_vars = t.get_all_placeholders(template.Placeholders({}))
    mock_glob.assert_any_call("*")
    mock_glob.assert_any_call("*_age*")
    assert mock_glob.call_count == 2
    assert len(new_vars) == 2
    assert new_vars["A"] == ["bar", "bar_age1", "bar_age2", "foo"]
    assert new_vars["B"] == [None, 1, 2]


@mock.patch("file_tree.template.glob")
def test_get_all_placeholders_optional_directory(mock_glob):
    """Optional directory placeholders supported when inferring files on disk."""
    mock_glob.return_value = [
        "sub-A/ses-A/text.txt",
        "sub-A/ses-B/text.txt",
        "sub-B/text.txt",
        # invalid directory structure; should not affect the results
        "sub-C/ses-D/sub-session-E/text.txt",
    ]

    t = template.Template(None, "sub-{A}/[ses-{B}]/{C}.txt")
    new_vars = t.get_all_placeholders(template.Placeholders({}))
    mock_glob.assert_any_call("sub-*/*.txt")
    mock_glob.assert_any_call("sub-*/ses-*/*.txt")
    assert mock_glob.call_count == 2
    assert len(new_vars) == 3
    assert new_vars["A"] == ["A", "B"]
    assert new_vars["B"] == [None, "A", "B"]
    assert new_vars["C"] == ["text"]

    for filter in (False, True):
        da = t.format_mult(new_vars, filter=filter)
        assert da.sel(A="A", B="A", C="text").data[()] == str("sub-A/ses-A/text.txt")
        assert da.sel(A="A", B="B", C="text").data[()] == str("sub-A/ses-B/text.txt")
        if filter:
            assert da.sel(A="B", B="B", C="text").data[()] == ""
        else:
            assert da.sel(A="B", B="B", C="text").data[()] == str(
                "sub-B/ses-B/text.txt"
            )

    mock_glob.reset_mock()
    new_vars = t.get_all_placeholders(template.Placeholders({"B": "B"}))
    mock_glob.assert_any_call("sub-*/*.txt")
    mock_glob.assert_any_call("sub-*/ses-*/*.txt")
    assert mock_glob.call_count == 2
    assert len(new_vars) == 2
    assert new_vars["A"] == ["A"]
    assert new_vars["C"] == ["text"]

    mock_glob.reset_mock()
    new_vars = t.get_all_placeholders(template.Placeholders({"A": ("A", "C")}))
    mock_glob.assert_any_call("sub-*/*.txt")
    mock_glob.assert_any_call("sub-*/ses-*/*.txt")
    assert mock_glob.call_count == 2
    assert len(new_vars) == 2
    assert new_vars["B"] == ["A", "B"]
    assert new_vars["C"] == ["text"]

    mock_glob.reset_mock()
    new_vars = t.get_all_placeholders(template.Placeholders({"B": (None,)}))
    mock_glob.assert_any_call("sub-*/*.txt")
    mock_glob.assert_any_call("sub-*/ses-*/*.txt")
    assert mock_glob.call_count == 2
    assert len(new_vars) == 2
    assert new_vars["A"] == ["B"]
    assert new_vars["C"] == ["text"]


def test_absolute_paths():
    """Template parents can be set to None to support absolute paths."""
    test_path = "/opt/test/something"
    t = template.Template(None, test_path)
    p = template.Placeholders({})
    assert test_path == str(t.format_single(p))

    parent = template.Template(None, "/opt/test")
    t = template.Template(parent, "something")
    assert test_path == str(t.format_single(p))

    parent = template.Template(None, "{var}")
    t = template.Template(parent, "something")
    p = template.Placeholders({"var": "/opt/test"})
    assert test_path == str(t.format_single(p))


def test_linkages_overwrite():
    """Linked placeholder values support."""
    p = template.Placeholders()
    p["A", "B"] = [(1, 2, 3), (4, 5, 6)]
    assert p["A"] == (1, 2, 3)
    assert p["B"] == (4, 5, 6)

    p["B"] = (4, 5)
    assert p["A"] == (1, 2)
    assert p["B"] == (4, 5)

    with pytest.raises(ValueError):
        p["A"] = 8

    with pytest.raises(ValueError):
        p["A"] = (2, 8)

    p["A"] = 2
    assert p["A"] == 2
    assert p["B"] == 5

    p = template.Placeholders()
    p["A", "B"] = [(1, 2, 3), (4, 5, 6)]
    p["B"] = (5, 4)
    assert p["A"] == (2, 1)
    assert p["B"] == (5, 4)

    # test duplicates
    p = template.Placeholders()
    p["A", "B"] = [(1, 2, 1), (4, 5, 6)]
    p["A"] = 1
    assert p["B"] == (4, 6)

    p = template.Placeholders()
    p["A", "B"] = [(1, 2, 1), (4, 5, 6)]
    p["A"] = (1, 2)
    assert p["A"] == (1, 1, 2)
    assert p["B"] == (4, 6, 5)

    # test iteratively linking variables
    p = template.Placeholders()
    for key in ["A", "B", "C", "D"]:
        p[key] = (1, 2, 3)
    assert len(list(p.iter_over(["A", "B", "C", "D"]))) == 3**4
    p.link("A", "B")
    p.link("A", "C", "D")
    assert len(list(p.iter_over(["A", "B", "C", "D"]))) == 3

    p = template.Placeholders()
    for key in ["A", "B", "C", "D"]:
        p[key] = (1, 2, 3)
    assert len(list(p.iter_over(["A", "B", "C", "D"]))) == 3**4
    p.link("A", "B")
    p.link("C", "D")
    assert len(list(p.iter_over(["A", "B", "C", "D"]))) == 3**2
    p.link("A", "B", "C")
    assert len(list(p.iter_over(["A", "B", "C", "D"]))) == 3



def test_missing_keys():
    p = template.Placeholders()
    assert p.missing_keys(["a", "b"]) == {"a", "b"}
    assert p.missing_keys(["a/s", "b/s"]) == {"s"}
    assert p.missing_keys(["a/b/s", "b/s"]) == {"s"}
    assert p.missing_keys(["a/b/s", "s"]) == {"s"}

    p = template.Placeholders({"b/s": ""})
    assert p.missing_keys(["a/s", "b/s"]) == {"s"}
    assert p.missing_keys(["a/b/s", "b/s"]) == set()
    assert p.missing_keys(["a/b/s", "s"]) == {"s"}

    assert p.missing_keys(["a/s", "b/s"], top_level=False) == {"a/s"}
    assert p.missing_keys(["a/b/s", "b/s"], top_level=False) == set()
    assert p.missing_keys(["a/s", "s"], top_level=False) == {"a/s", "s"}