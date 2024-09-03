"""Test the main FileTree interface."""
import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import pytest

from file_tree import FileTree, Template, convert, parse_tree

directory = Path(__file__).parent.joinpath("test_trees")


def test_template_interface():
    """Adds and renames some templates (with or without conflicts)."""
    tree = FileTree.empty()

    assert tree.top_level == "."
    assert FileTree.empty(return_path=True).top_level == Path(".")
    tree.add_template("directory")
    assert tree.get_template("directory").as_path == Path("directory")
    tree.add_template("file1.txt")
    assert tree.get_template("file1").as_path == Path("file1.txt")

    tree.add_template("file1.doc")
    with pytest.raises(ValueError):
        tree.get_template("file1")

    tree.add_template("file2.txt", parent="directory")
    assert tree.get_template("file2").as_path == Path("directory/file2.txt")

    tree.add_template("file1.txt", key="other_file1", parent="directory")
    assert tree.get_template("other_file1").as_path == Path("directory/file1.txt")


def test_overwrite_templates():
    """Overwrite existing templates."""
    tree = FileTree.read(directory / "base.tree", subject="A", top_level="directory")

    assert tree.get("top_file") == "directory/top_file.txt"
    tree.add_template("new_top_file.txt", key="top_file", parent=None, overwrite=True)
    assert tree.get("top_file") == "new_top_file.txt"
    tree.add_template("new_top_file.txt", key="top_file", overwrite=True)
    assert tree.get("top_file") == "directory/new_top_file.txt"

    # overwriting a parent template changes the child
    assert tree.get("nested_dir") == "directory/A/nested_dir"
    assert tree.get("deep_file") == "directory/A/nested_dir/deep_file.txt"
    tree.add_template("new_dir", key="nested_dir", overwrite=True)
    assert tree.get("nested_dir") == "directory/new_dir"
    assert tree.get("deep_file") == "directory/new_dir/deep_file.txt"


def test_variable_interface():
    """Placeholder variabes can be accessed directly."""
    tree = FileTree.read(directory.joinpath("parent.tree"))
    with pytest.raises(KeyError):
        assert tree.placeholders["session"]
    with pytest.raises(KeyError):
        assert tree.placeholders["other_var"]
    assert tree.placeholders["base1/session"] == "01"
    with pytest.raises(KeyError):
        assert tree.placeholders["base1/other_var"]
    assert tree.placeholders["base2/session"] == "02"
    assert tree.placeholders["base2/other_var"] == "foo"
    assert tree.placeholders["base3/session"] == "03"

    tree2 = tree.update(inplace=True, session="03")
    assert tree is tree2
    assert tree.placeholders["session"] == "03"
    assert tree.placeholders["base1/session"] == "01"

    tree2 = tree.update(inplace=False, session="05")
    assert tree is not tree2
    assert tree.placeholders["session"] == "03"
    assert tree.placeholders["base1/session"] == "01"
    assert tree2.placeholders["session"] == "05"
    assert tree2.placeholders["base1/session"] == "01"

    tree.update(inplace=True, subject="A")
    assert tree.placeholders["session"] == "03"
    assert tree.placeholders["base1/session"] == "01"
    assert tree.placeholders["subject"] == "A"
    assert tree.placeholders["base1/subject"] == "A"


def test_template_keys():
    """All templates are correctly extracted."""
    tree = FileTree.read(directory.joinpath("base.tree"))
    assert len(tree.template_keys()) == 8
    assert sorted(tree.template_keys()) == sorted(
        [
            "",
            "{subject}",
            "file1",
            "file2",
            "nested_dir",
            "deep_file",
            "int_file",
            "top_file",
        ]
    )

    assert len(tree.template_keys(only_leaves=True)) == 5
    assert sorted(tree.template_keys(only_leaves=True)) == sorted(
        [
            "file1",
            "file2",
            "deep_file",
            "int_file",
            "top_file",
        ]
    )


def test_linked_placeholders():
    """Linked placeholder values are correctly processed."""
    tree = FileTree.read(directory / "parent.tree")
    vars = (["A", "B", "C"], [1, 2, 3])
    tree.placeholders[("subject", "session")] = vars
    assert tree.placeholders["subject"] == vars[0]
    assert tree.placeholders["session"] == vars[1]
    for idx, sub_tree in enumerate(tree.iter_vars(["subject", "session"])):
        assert sub_tree.placeholders["subject"] == vars[0][idx]
        assert sub_tree.placeholders["session"] == vars[1][idx]
    for idx, sub_tree in enumerate(tree.iter_vars(["subject"])):
        assert sub_tree.placeholders["subject"] == vars[0][idx]
        assert sub_tree.placeholders["session"] == vars[1][idx]

    with pytest.raises(KeyError):
        del tree.placeholders["subject"]

    del tree.placeholders[("session", "subject")]
    tree.placeholders["subject"] = vars[0]
    tree.placeholders["session"] = vars[1]
    assert len(list(tree.iter_vars(["subject", "session"]))) == 9

    tree.placeholders.link("subject", "session")
    assert len(list(tree.iter_vars(["subject", "session"]))) == 3
    for idx, sub_tree in enumerate(tree.iter_vars(["subject", "session"])):
        assert sub_tree.placeholders["subject"] == vars[0][idx]
        assert sub_tree.placeholders["session"] == vars[1][idx]

    # test IO
    new_tree = FileTree.from_string(tree.to_string())
    assert len(list(new_tree.iter_vars(["subject", "session"]))) == 3
    for idx, sub_tree in enumerate(new_tree.iter_vars(["subject", "session"])):
        assert sub_tree.placeholders["subject"] == vars[0][idx]
        assert int(sub_tree.placeholders["session"]) == vars[1][idx]

    tree.placeholders.unlink("subject", "session")
    assert len(list(tree.iter_vars(["subject", "session"]))) == 9
    assert tree.placeholders["subject"] == vars[0]
    assert tree.placeholders["session"] == vars[1]

    # test creating sub-tree with linked variables
    tree.placeholders.link("subject", "session")
    new_tree = FileTree.empty()
    new_tree.add_subtree(tree, precursor=["test"])
    assert new_tree.placeholders["test/subject"] == vars[0]
    assert new_tree.placeholders["test/session"] == vars[1]
    assert len(list(tree.iter_vars(["subject", "session"]))) == 3


def test_get():
    """Placeholder values are correctly filled into filenames."""
    for return_path, return_type in [(False, str), (True, Path)]:
        tree = FileTree.read(
            directory / "base.tree", subject="A", return_path=return_path
        )
        assert tree.get("file1") == return_type("A/file1.txt")
        assert tree.get("file2") == return_type("A/01_file2.txt")

        allp = tree.get_mult("file2")
        assert allp.shape == ()
        assert allp.data[()] == return_type("A/01_file2.txt")

        tree2 = tree.update(session=None)
        assert tree2.get("file1") == return_type("A/file1.txt")
        with pytest.raises(KeyError):
            tree2.get("file2")

        tree3 = tree.update(subject=None)
        with pytest.raises(KeyError):
            tree3.get("file1")
        with pytest.raises(KeyError):
            tree3.get("file2")

        tree4 = tree.update(subject=["A", "B"])
        with pytest.raises(KeyError):
            tree4.get("file1")
        with pytest.raises(KeyError):
            tree4.get("file2")

        allp = tree4.get_mult("file2")
        assert allp.shape == (2,)
        assert allp.sel(subject="A") == return_type("A/01_file2.txt")
        assert allp.sel(subject="B") == return_type("B/01_file2.txt")

        tree5 = tree.update(subject=["A", "B"], session=(1, 2))
        allp = tree5.get_mult(("file1", "file2"))
        assert allp["file1"].shape == (2,)
        assert allp["file2"].shape == (2, 2)
        assert allp.sel(subject="A")["file1"] == return_type("A/file1.txt")
        assert allp.sel(subject="A")["file2"].shape == (2,)
        assert allp.sel(subject="A", session=2)["file2"] == return_type("A/2_file2.txt")


def test_get_mult_child_placholder():
    """Test a bug in the names used for the xarray dimensions when using sub-trees."""
    tree = FileTree.from_string(
        "sub-file-{sub/place}.txt (sub/file)", place=("A", "B", "C")
    )
    res = tree.get_mult("sub/file")
    assert res.shape == (3,)
    assert res.dims[0] == "place"
    assert res.name == "sub/file"
    assert res.sel(place="B").values[()] == "sub-file-B.txt"

    tree.placeholders["sub/place"] = ("D", "E")
    res = tree.get_mult("sub/file")
    assert res.shape == (2,)
    assert res.dims[0] == "sub/place"
    assert res.name == "sub/file"
    assert res.sel({"sub/place": "E"}).values[()] == "sub-file-E.txt"


def test_iteration():
    """Iterate over multiple placeholder variable values."""
    tree = FileTree.read(
        directory / "base.tree", subject=("A", "B", "C"), session=(1, 2)
    )
    allp = tree.get_mult("file2")
    assert allp.size == 6
    assert allp.sel(subject="B", session=1) == "B/1_file2.txt"

    assert len(list(tree.iter("file1"))) == 3
    all_subjects = set()
    for stree in tree.iter("file1"):
        subject = stree.placeholders["subject"]
        all_subjects.add(subject)
        assert stree.get("file1") == f"{subject}/file1.txt"
        assert stree.get_mult("file2").shape == (2,)
    assert tuple(sorted(all_subjects)) == ("A", "B", "C")

    assert len(list(tree.iter("file2"))) == 6
    all_subjects = set()
    all_sessions = set()
    for stree in tree.iter("file2"):
        subject = stree.placeholders["subject"]
        all_subjects.add(subject)
        session = stree.placeholders["session"]
        all_sessions.add(session)
        assert stree.get("file1") == f"{subject}/file1.txt"
        assert stree.get("file2") == f"{subject}/{session}_file2.txt"
    assert tuple(sorted(all_subjects)) == ("A", "B", "C")
    assert tuple(sorted(all_sessions)) == (1, 2)

    # tests fixed bug where iteration fails
    # if both linked and unlinked variables are iterated over
    tree = FileTree.from_string(
        """{As}_{Bs} (fn)
As=1,2
Bs=3,4,5
Cs=6,7"""
    )
    tree.placeholders.link("As", "Cs")
    for stree in tree.iter_vars(["As", "Bs"]):
        assert int(stree.placeholders["As"]) in (1, 2)
        assert int(stree.placeholders["Bs"]) in (3, 4, 5)
        assert int(stree.placeholders["Cs"]) in (6, 7)


def test_io():
    """Input and output of FileTree definitions are consistent with each other."""
    for tree_name in ("base", "parent", "multi_key"):
        for top_level in (".", "/data"):
            tree = FileTree.read(
                directory / f"{tree_name}.tree",
                top_level=top_level,
                subject=("A", "B", "C"),
                session=(1, 2),
                my_param=(None, 1.23),
            )
            new_tree = parse_tree.read_file_tree_text(
                tree.to_string().splitlines(), Template(None, top_level)
            )
            assert tree.to_string() == new_tree.to_string()
            for key in tree._templates:
                assert (
                    tree.get_template(key).as_path == new_tree.get_template(key).as_path
                )
                for key2 in tree._templates:
                    if tree.get_template(key) is tree.get_template(key2):
                        assert new_tree.get_template(key) is new_tree.get_template(key2)
                    else:
                        assert new_tree.get_template(key) is not new_tree.get_template(
                            key2
                        )
            for key in tree.placeholders:
                if key in ["subject", "session"]:
                    assert [str(elem) for elem in tree.placeholders[key]] == list(
                        new_tree.placeholders[key]
                    )
                elif key == "my_param":
                    assert list(new_tree.placeholders["my_param"]) == [None, "1.23"]
                else:
                    assert str(tree.placeholders[key]) == new_tree.placeholders[key]


def test_multi_key():
    """Multiple template keys can refer to the same Template."""
    tree = FileTree.read(directory / "multi_key.tree")
    assert tree.get_template("file") is tree.get_template("top_level")
    assert tree.get_template("sub1/") is tree.get_template("sub2/")
    assert tree.get_template("sub1/file1") is not tree.get_template("sub2/file1")


@mock.patch("file_tree.template.glob")
def test_glob(mock_glob):
    """Placeholder variable values can be inferred from disk."""
    mock_glob.return_value = [
        "sub-A/ses-A/text.txt",
        "sub-A/ses-B/text.txt",
        "sub-B/text.txt",
        "sub-B/other_text.txt",
        # invalid directory structure; should not affect the results
        "sub-C/ses-D/sub-session-E/text.txt",
    ]

    tree = FileTree.from_string(
        """
    sub-{A}/[ses-{B}]/{C}.txt (all)
    sub-A/ses-{B}/{C}.txt (subA)
    sub-B/{C}.txt (subB)
    """
    )
    placholders = tree.update_glob("subB").placeholders
    assert len(placholders) == 1
    assert placholders["C"] == ["other_text", "text"]

    placholders = tree.update_glob("subA").placeholders
    assert len(placholders) == 2
    assert placholders["B"] == ["A", "B"]
    assert placholders["C"] == ["text"]

    placholders = tree.update_glob("all").placeholders
    assert len(placholders) == 3
    assert placholders["A"] == ["A", "B"]
    assert placholders["B"] == [None, "A", "B"]
    assert placholders["C"] == ["other_text", "text"]

    placholders = tree.update(B=["B", "A", "fake"]).update_glob("all").placeholders
    assert len(placholders) == 3
    assert placholders["A"] == ["A"]
    assert placholders["B"] == ["B", "A", "fake"]
    assert placholders["C"] == ["text"]

    placholders = tree.update_glob(("subA", "all")).placeholders
    assert len(placholders) == 3
    assert placholders["A"] == ["A", "B"]
    assert placholders["B"] == [None, "A", "B"]
    assert placholders["C"] == ["other_text", "text"]

    placholders = tree.update_glob(("subA", "subB")).placeholders
    assert len(placholders) == 2
    assert placholders["B"] == ["A", "B"]
    assert placholders["C"] == ["other_text", "text"]

    for filter in (False, True):
        da = tree.update_glob("subA").get_mult("subB", filter=filter)
        assert da.shape == (1,)
        assert da.sel(C="text").data[()] == "sub-B/text.txt"
        assert da.sel(C="text").shape == ()

        da = tree.update_glob("all").get_mult("subA", filter=filter)
        assert da.ndim == 2
        assert da.sel(B="A", C="text").data[()] == "sub-A/ses-A/text.txt"
        assert da.sel(B="A", C="text").shape == ()
        if filter:
            assert da.sel(B="A", C="other_text").data[()] == ""
            assert da.sel(B="A", C="other_text").shape == ()
        else:
            assert (
                da.sel(B="A", C="other_text").data[()] == "sub-A/ses-A/other_text.txt"
            )
            assert da.sel(B="A", C="other_text").shape == ()

    for template in tree.template_keys():
        assert (
            tree.update_glob(template).get_mult(template, filter=True)
            == tree.get_mult_glob(template)
        ).data.all()
    da1 = tree.update_glob(tree.template_keys()).get_mult(
        tree.template_keys(), filter=True
    )
    da2 = tree.get_mult_glob(tree.template_keys())
    for key in tree.template_keys():
        assert (da1[key] == da2[key]).data.all()


@mock.patch("file_tree.template.glob")
def test_glob_subtree(mock_glob):
    """Placeholder variable value extraction from disk also works for sub-trees."""
    mock_glob.return_value = [
        "sub-A/ses-A/text.txt",
        "sub-A/ses-B/text.txt",
        "sub-B/text.txt",
        "sub-B/other_text.txt",
        # invalid directory structure; should not affect the results
        "sub-C/ses-D/sub-session-E/text.txt",
    ]

    tree = FileTree.from_string(
        """
    sub-{A}/[ses-{sub/B}]/{C}.txt (all)
    sub-A/ses-{sub/B}/{C}.txt (subA)
    sub-B/{C}.txt (subB)
    """
    )

    placeholders = tree.update_glob("all").placeholders
    print("first", placeholders)
    assert len(placeholders) == 3
    assert placeholders["A"] == ["A", "B"]
    assert placeholders["B"] == [None, "A", "B"]
    assert "B" in placeholders
    assert placeholders["C"] == ["other_text", "text"]

    placeholders = (
        tree.update(**{"sub/B": ["B", "A", "fake"]}).update_glob("all").placeholders
    )
    print("second", placeholders)
    assert len(placeholders) == 3
    assert placeholders["A"] == ["A"]
    assert placeholders["sub/B"] == ["B", "A", "fake"]
    assert "B" not in placeholders
    assert placeholders["C"] == ["text"]

    placeholders = (
        tree.update(**{"B": ["B", "A", "fake"]}).update_glob("all").placeholders
    )
    print("third", placeholders)
    assert len(placeholders) == 3
    assert placeholders["A"] == ["A"]
    assert placeholders["B"] == ["B", "A", "fake"]
    assert "B" in placeholders
    assert "sub/B" in placeholders
    assert placeholders["C"] == ["text"]

    # test linked update_glob
    placeholders = tree.update_glob("all", link=["A", "sub/B"]).placeholders
    assert placeholders["A"] == ("A", "A", "B")
    assert placeholders["sub/B"] == ("A", "B", None)
    assert placeholders["C"] == ["other_text", "text"]
    assert 'B' not in placeholders

    placeholders = tree.update_glob("all", link=["A", "sub/B", "C"]).placeholders
    assert placeholders["A"] == ("A", "A", "B", "B")
    assert placeholders["sub/B"] == ("A", "B", None, None)
    assert placeholders["C"] == ("text", "text", "other_text", "text")
    assert 'B' not in placeholders

    placeholders = tree.update(A=["A", "fake"]).update_glob("all", link=["A", "sub/B", "C"]).placeholders
    assert placeholders["A"] == ("A", "A")
    assert placeholders["sub/B"] == ("A", "B")
    assert placeholders["C"] == ("text", "text")
    assert 'B' not in placeholders

    placeholders = tree.update(A="A").update_glob("all", link=["A", "sub/B", "C"]).placeholders
    assert placeholders["A"] == ("A", "A")
    assert placeholders["sub/B"] == ("A", "B")
    assert placeholders["C"] == ("text", "text")
    assert 'B' not in placeholders

@mock.patch("file_tree.template.glob")
def test_glob_subtree_simple(mock_glob):
    """Placeholder variable value extraction from disk also works for sub-trees."""
    mock_glob.return_value = [
        "sub-A/sub-A.txt",
        "sub-A/sub-C.txt",
        "sub-B/sub-B.txt",
        "sub-D/sub-E.txt",
    ]

    tree = FileTree.from_string(
        """
    sub-{s}/sub-{f/s}.txt (test)
    """
    )
    template = tree.get_template("test")

    placeholders = tree.update_glob("test").placeholders
    print("first", placeholders)
    assert len(placeholders) == 1
    assert placeholders["s"] == ["A", "B"]
    assert len(template.all_matches(tree.placeholders)) == 2

    placeholders = (
        tree.update(**{"f/s": ["A", "C", "E"]}).update_glob("test").placeholders
    )
    print("second", placeholders)
    assert len(placeholders) == 2
    assert placeholders["f/s"] == ["A", "C", "E"]
    assert placeholders["s"] == ["A", "D"]
    assert (
        len(template.all_matches(tree.update(**{"f/s": ["A", "C", "E"]}).placeholders))
        == 3
    )
    assert (
        len(
            template.all_matches(
                tree.update(**{"f/s": ["A", "C", "E", "fake"]}).placeholders
            )
        )
        == 3
    )

    placeholders = tree.update(**{"s": ["A", "C"]}).update_glob("test").placeholders
    print("third", placeholders)
    assert len(placeholders) == 1
    assert placeholders["s"] == ["A", "C"]
    assert len(template.all_matches(tree.update(**{"s": ["A", "C"]}).placeholders)) == 1
    assert (
        len(template.all_matches(tree.update(**{"s": ["A", "C", "fake"]}).placeholders))
        == 1
    )


def test_mult_linked():
    """Linked variables should produce 1D DataArrays in `get_mult`."""
    tree = FileTree.from_string(
        """
{A}.txt (single)
{A}_{B}.txt (mult)
"""
    )
    tree.placeholders[("A", "B")] = [(1, 2, 3), ("a", "b", "c")]
    xa = tree.get_mult("single")
    assert xa.shape == (3,)
    assert xa.sel(A=1).data[()] == "1.txt"
    # I would like the following to be true, but it is not:
    # assert xa.sel(A=1).shape == ()

    xa = tree.get_mult("mult")
    assert xa.shape == (3,)
    assert xa.sel(A=2).data[()] == "2_b.txt"
    assert xa.sel(B="b").data[()] == "2_b.txt"
    assert xa.sel(A=1).shape == (1,)
    assert xa.sel(B="b").shape == (1,)


def test_convert():
    """Convert filenames between file-trees."""
    tree = FileTree.from_string(
        """
    A=1,2
    {A}_old.txt (old)
    {A}_new.txt (new)
    """
    )

    def expected_conversions(mocker, conversions):
        assert mocker.call_args_list == [
            mock.call(Path(fn1), Path(fn2), ([], []), overwrite=False, symlink=False)
            for fn1, fn2 in conversions
        ]

    with mock.patch("file_tree.file_tree._convert_file") as my_convert:
        convert(tree, keys=[("old", "new")])
        expected_conversions(
            my_convert,
            [
                ("1_old.txt", "1_new.txt"),
                ("2_old.txt", "2_new.txt"),
            ],
        )

    with mock.patch("file_tree.file_tree._convert_file") as my_convert:
        convert(tree, tree)
        expected_conversions(
            my_convert,
            [
                ("1_new.txt", "1_new.txt"),
                ("2_new.txt", "2_new.txt"),
                ("1_old.txt", "1_old.txt"),
                ("2_old.txt", "2_old.txt"),
            ],
        )

    with mock.patch("file_tree.file_tree._convert_file") as my_convert:
        convert(tree, tree.update(A=["A", "B"]))
        expected_conversions(
            my_convert,
            [
                ("1_new.txt", "A_new.txt"),
                ("2_new.txt", "B_new.txt"),
                ("1_old.txt", "A_old.txt"),
                ("2_old.txt", "B_old.txt"),
            ],
        )

    src = FileTree.from_string(
        """
    subject=A,B
    session=sess
    sub-{subject}
        session-{session}
            T1w.nii.gz
            FLAIR.nii.gz
    """
    )

    target = FileTree.from_string(
        """
    sub-{subject}
        T1w.nii.gz
        T2w.nii.gz
    """
    )

    with mock.patch("file_tree.file_tree._convert_file") as my_convert:
        convert(src, target)
        expected_conversions(
            my_convert,
            [
                ("sub-A/session-sess/T1w.nii.gz", "sub-A/T1w.nii.gz"),
                ("sub-B/session-sess/T1w.nii.gz", "sub-B/T1w.nii.gz"),
            ],
        )

    with mock.patch("file_tree.file_tree._convert_file") as my_convert:
        convert(src, target, keys=["T1w", ("FLAIR", "T2w")])
        expected_conversions(
            my_convert,
            [
                ("sub-A/session-sess/FLAIR.nii.gz", "sub-A/T2w.nii.gz"),
                ("sub-B/session-sess/FLAIR.nii.gz", "sub-B/T2w.nii.gz"),
                ("sub-A/session-sess/T1w.nii.gz", "sub-A/T1w.nii.gz"),
                ("sub-B/session-sess/T1w.nii.gz", "sub-B/T1w.nii.gz"),
            ],
        )

    with mock.patch("file_tree.file_tree._convert_file") as my_convert:
        convert(src, target.update(subject=("1", "2")), keys=["T1w", ("FLAIR", "T2w")])
        expected_conversions(
            my_convert,
            [
                ("sub-A/session-sess/FLAIR.nii.gz", "sub-1/T2w.nii.gz"),
                ("sub-B/session-sess/FLAIR.nii.gz", "sub-2/T2w.nii.gz"),
                ("sub-A/session-sess/T1w.nii.gz", "sub-1/T1w.nii.gz"),
                ("sub-B/session-sess/T1w.nii.gz", "sub-2/T1w.nii.gz"),
            ],
        )

    with mock.patch("file_tree.file_tree._convert_file") as my_convert:
        convert(
            src.update(subject=None),
            target.update(subject=(1, 2)),
            keys=["T1w", ("FLAIR", "T2w")],
        )
        expected_conversions(
            my_convert,
            [
                ("sub-1/session-sess/FLAIR.nii.gz", "sub-1/T2w.nii.gz"),
                ("sub-2/session-sess/FLAIR.nii.gz", "sub-2/T2w.nii.gz"),
                ("sub-1/session-sess/T1w.nii.gz", "sub-1/T1w.nii.gz"),
                ("sub-2/session-sess/T1w.nii.gz", "sub-2/T1w.nii.gz"),
            ],
        )

    with mock.patch("file_tree.file_tree._convert_file") as my_convert:
        with pytest.raises(ValueError):
            # subject not defined
            convert(src.update(subject=None), target)

        with pytest.raises(ValueError):
            # session not defined
            convert(src.update(session=None), target)

        with pytest.raises(ValueError):
            # target tree or keys should be defined
            convert(src)

        with pytest.raises(ValueError):
            # target subject is singular, while src has multiple elements
            convert(src, target.update(subject="hi"))

        with pytest.raises(ValueError):
            # src and target subjects have different number of values
            convert(src, target.update(subject=[1, 2, 3]))

        my_convert.assert_not_called()


def test_filter():
    """Filetree templates can be filtered."""
    tree = FileTree.from_string(
        """
    A=1,2
    B=c,d,e
    top
        mid_{A} (mid)
            base_file
            var_file{B} (var_file)
        other_dir
    """
    )
    assert tree.template_keys() == {
        "",
        "top",
        "mid",
        "base_file",
        "var_file",
        "other_dir",
    }

    new_tree = tree.filter_templates(["base_file"])
    assert new_tree.template_keys() == {"", "top", "mid", "base_file"}

    new_tree = tree.filter_templates(["base_file", "mid"])
    assert new_tree.template_keys() == {"", "top", "mid", "base_file"}

    new_tree = tree.filter_templates(["base_file", "var_file"])
    assert new_tree.template_keys() == {"", "top", "mid", "base_file", "var_file"}

    new_tree = tree.filter_templates(["other_dir"])
    assert new_tree.template_keys() == {"", "top", "other_dir"}

    # check unknown template name behaviour
    with pytest.raises(KeyError):
        tree.filter_templates(["base_file", "unknown"])

    new_tree = tree.filter_templates(["base_file", "unknown"], check=False)
    assert new_tree.template_keys() == {"", "top", "mid", "base_file"}


def test_various_read():
    """Consistent file-trees independent of reading method."""
    with parse_tree.extra_tree_dirs([directory]):
        ref_tree = FileTree.read("base.tree")

    parse_tree.available_subtrees.update(
        {
            "as_path": directory / "base.tree",
            "as_str": open(directory / "base.tree").read(),
            "as_tree": ref_tree,
        }
    )

    for s in ("as_path", "as_str", "as_tree"):
        tree = FileTree.read(s)
        assert ref_tree.to_string() == tree.to_string()


def test_convert_glob():
    """Using placeholder variables inferred from disk for conversion."""
    with TemporaryDirectory() as dir:
        src_tree = FileTree.from_string(
            """
        subject=A,B
        src
            sub-{subject}
                scan-{id}_T1w.txt (T1w)
                scan-{id}_T2w.txt (T2w)
        """,
            top_level=dir,
        )

        target_tree = FileTree.from_string(
            """
        target
            sub-{subject}
                T1w.txt
                T2w.txt
        """,
            top_level=dir,
        )

        all_ids = [(1, 2), (3, 4)]
        for subject, subject_ids in zip(src_tree.placeholders["subject"], all_ids):
            for key, scan_id in zip(("T1w", "T2w"), subject_ids):
                with open(
                    src_tree.update(id=scan_id, subject=subject).get(
                        key, make_dir=True
                    ),
                    "w",
                ) as f:
                    f.write(subject + "\n")
                    f.write(str(scan_id) + "\n")

        with pytest.raises(ValueError):
            convert(src_tree, target_tree)

        convert(src_tree, target_tree, glob_placeholders=["id"])
        for subject, subject_ids in zip(src_tree.placeholders["subject"], all_ids):
            for key, scan_id in zip(("T1w", "T2w"), subject_ids):
                with open(target_tree.update(subject=subject).get(key), "r") as f:
                    assert f.readline()[:-1] == subject
                    assert int(f.readline()[:-1]) == scan_id

        shutil.rmtree(target_tree.get("target"))
        target_tree_id = FileTree.from_string(
            """
        target
            sub-{subject}
                T1w_{id}.txt (T1w)
                T2w_{id}.txt (T2w)
        """,
            top_level=dir,
        )
        convert(src_tree, target_tree_id, glob_placeholders=["id"])
        for subject, subject_ids in zip(src_tree.placeholders["subject"], all_ids):
            for key, scan_id in zip(("T1w", "T2w"), subject_ids):
                with open(
                    target_tree_id.update(subject=subject, id=scan_id).get(key), "r"
                ) as f:
                    assert f.readline()[:-1] == subject
                    assert int(f.readline()[:-1]) == scan_id

        shutil.rmtree(target_tree.get("target"))
        os.remove(src_tree.update(subject="B", id=4).get("T2w"))

        with pytest.warns(UserWarning):
            convert(src_tree, target_tree, glob_placeholders=["id"])
        for subject, subject_ids in zip(src_tree.placeholders["subject"], all_ids):
            for key, scan_id in zip(("T1w", "T2w"), subject_ids):
                fn = target_tree.update(subject=subject).get(key)
                if scan_id == 4:
                    assert not os.path.exists(fn)
                else:
                    with open(fn, "r") as f:
                        assert f.readline()[:-1] == subject
                        assert int(f.readline()[:-1]) == scan_id


def test_app_import():
    """Check file_tree.app import for any issues."""
    try:
        import textual
    except ImportError:
        return
    from file_tree import app  # noqa: F401


def test_duplicate_key():
    """Duplicate keys should raise an error when accessed, not on creation."""
    as_string = """duplicate
i
    duplicate
        input.txt
o
    duplicate
        output.txt
"""
    tree = FileTree.from_string(as_string)
    assert tree.get("input") == "i/duplicate/input.txt"
    assert tree.get("output") == "o/duplicate/output.txt"
    with pytest.raises(ValueError):
        tree.get("duplicate")
    assert len(tree.get_template("duplicate", error_duplicate=False).templates) == 3
    assert tree.to_string().strip() == as_string.strip()
    assert tree.template_keys() == {"", "i", "o", "input", "output"}
    assert tree.template_keys(skip_duplicates=False) == {"", "duplicate", "i", "o", "input", "output"}

    part_tree = tree.filter_templates(["output"])
    print(part_tree.to_string())
    assert part_tree.to_string().strip() == """
o
    duplicate
        output.txt""".strip()
    assert part_tree.get("duplicate") == "o/duplicate"

    tree.add_subtree(tree, "test", "i")
    assert tree.get("test/output") == "i/o/duplicate/output.txt"
    with pytest.raises(ValueError):
        tree.get("test/duplicate")
    assert len(tree.get_template("duplicate", error_duplicate=False).templates) == 3
    assert len(tree.get_template("test/duplicate", error_duplicate=False).templates) == 3

    tree.add_subtree(tree, None, "o")
    with pytest.raises(ValueError):
        tree.get("output")
    assert len(tree.get_template("output", error_duplicate=False).templates) == 2
    with pytest.raises(ValueError):
        tree.get("test/duplicate")
    assert len(tree.get_template("duplicate", error_duplicate=False).templates) == 6


def test_override():
    """Test FileTree.override."""

    base_string = """
base_input
    input_dir
        data1.txt
        data2.txt
output
    result.txt
"""
    tree = FileTree.from_string(base_string)
    assert tree.to_string().strip() == base_string.strip()
    assert tree.template_keys() == {"", "base_input", "input_dir", "data1", "data2", "output", "result"}

    override_data1 = FileTree.from_string("""
user_input (input_dir)
    my_data.txt (data1)
""", top_level="test")
    def test_result(ft):
        assert ft.to_string().strip() == """
base_input
    input_dir
        data2.txt
output
    result.txt

!test ()
    user_input ()
        my_data.txt (data1)
""".strip()
        assert ft.get("data1") == "test/user_input/my_data.txt"
        assert ft.get("data2") == "base_input/input_dir/data2.txt"
        assert ft.template_keys() == tree.template_keys()
    test_result(tree.override(override_data1, required=["data1"]))
    test_result(tree.override(override_data1, optional=["data1"]))

    assert tree.to_string().strip() == base_string.strip()
    assert tree.override(override_data1, optional=["data2"]).to_string().strip() == base_string.strip()

    ft = tree.override(override_data1, required=["input_dir"])
    assert ft.to_string().strip() == """
base_input
output
    result.txt

!test ()
    user_input (input_dir)
        data1.txt
        data2.txt
""".strip()
    assert ft.template_keys() == tree.template_keys()
    assert ft.get("data1") == "test/user_input/data1.txt"
    assert ft.get("data2") == "test/user_input/data2.txt"

    ft = tree.override(override_data1, optional=["input_dir", "data1", "data2"])
    print(ft.to_string())
    assert ft.to_string().strip() == """
base_input
output
    result.txt

!test ()
    user_input (input_dir)
        data2.txt
        my_data.txt (data1)
""".strip()
    assert ft.template_keys() == tree.template_keys()
    assert ft.get("data1") == "test/user_input/my_data.txt"
    assert ft.get("data2") == "test/user_input/data2.txt"



def test_print_relinked_variables():
    from file_tree import FileTree
    tree = FileTree.from_string("{test}")
    tree.placeholders["test"] = [1, 2, 3]
    tree.placeholders["unlinked"] = ["a", "b"]
    assert tree.to_string().strip() == """
test = 1, 2, 3
unlinked = a, b

{test}""".strip()
    tree.placeholders.link("test")
    assert tree.to_string().strip() == """
test = 1, 2, 3
unlinked = a, b
&LINK test

{test}""".strip()

    tree.placeholders["other"] = [4, 5, 6]
    tree.placeholders.link("test", "other")
    assert tree.to_string().strip() == """
other = 4, 5, 6
test = 1, 2, 3
unlinked = a, b
&LINK other, test

{test}""".strip()
    tree.placeholders["one_more"] = [7, 8, 9]
    tree.placeholders.link("test", "one_more")
    assert tree.to_string().strip() == """
one_more = 7, 8, 9
other = 4, 5, 6
test = 1, 2, 3
unlinked = a, b
&LINK one_more, other, test

{test}""".strip()