"""Test the parsing of the FileTree definitions."""
from pathlib import Path

import pytest

from file_tree import FileTree, extra_tree_dirs

directory = Path(__file__).parent.joinpath("test_trees")


def check_base_tree(tree: FileTree, name, top_level=".", session="01"):
    """Check template extraction from basic FileTree definition."""
    top_level = Path(top_level)
    for key, filename in [
        ("{subject}", f"{{{name}subject}}"),
        ("file1", f"{{{name}subject}}/file1.txt"),
        ("file2", f"{{{name}subject}}/{{{name}session}}_file2.txt"),
        ("nested_dir", f"{{{name}subject}}/nested_dir"),
        ("deep_file", f"{{{name}subject}}/nested_dir/deep_file.txt"),
        ("int_file", f"{{{name}subject}}/int_file.txt"),
        ("top_file", "top_file.txt"),
    ]:
        assert tree.get_template(name + key).as_path == top_level / filename
    assert tree.update(subject="A").get(name + "file2") == str(
        top_level / "A" / (session + "_file2.txt")
    )


def test_parse_base_tree():
    """Parses the base FileTree in various ways."""
    with pytest.raises(ValueError):
        FileTree.read("base.tree")

    with extra_tree_dirs([directory]):
        tree = FileTree.read("base.tree")
    check_base_tree(tree, "")

    with pytest.raises(ValueError):
        FileTree.read("base.tree")

    tree = FileTree.read(directory.joinpath("base.tree"))
    check_base_tree(tree, "")


def test_parse_parent_tree():
    """Parses a FileTree with sub-trees."""
    tree = FileTree.read(directory.joinpath("parent.tree"))
    assert tree.get_template("file1").as_path == Path("A/file1.txt")
    assert tree.get_template("file2").as_path == Path("A/01_file2.txt")
    for name, top_level, session in [
        ("base1", ".", "01"),
        ("base2", "sub", "02"),
        ("base3", ".", "03"),
    ]:
        check_base_tree(tree, name + "/", top_level, session)


def test_subtree_finder():
    """Find sub-trees in different ways."""
    with pytest.raises(ValueError):
        FileTree.from_string(
            top_level=directory.parent,
            definition="""
        test_trees
            ->base (base)
        """,
        )

    with pytest.raises(ValueError):
        FileTree.from_string(
            top_level=directory.parent,
            definition="""
        {sub_dir}
            ->base (base)
        """,
        )


def test_no_key():
    """Allow templates with no key access."""
    as_string = """
level_a (a)
    level_b ()
        level_c (c)
"""
    tree = FileTree.from_string(as_string)
    assert tree.get("") == "."
    assert tree.get("a") == "level_a"
    assert tree.get("c") == "level_a/level_b/level_c"
    assert tree.template_keys() == {"", "a", "c"}
    assert tree.to_string().strip() == as_string.strip()