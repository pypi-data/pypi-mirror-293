Changes with respect to FileTree in fslpy
=========================================

An earlier version of file-tree was included in fslpy (https://git.fmrib.ox.ac.uk/fsl/fslpy).
This is a complete rewrite with many new features.
Some changes are backwards incompatible, although most pipelines should work.
Please let me know if yours does not!

Some of the main changes are:

    - Some terminology changes: I now refer to template short names as template keys and to variables as placeholder values.
    - Iteration has completely been rewritten with placeholders now being able to have multiple values.
      All possible values can be automatically determined (described in :ref:`iteration`).
      This replaces the old interface of the `get_all...` methods.
    - There is a new interface to add/overwrite templates (:meth:`FileTree.add_template <file_tree.file_tree.FileTree.add_template>`)
      or add sub-trees (:meth:`FileTree.add_subtree <file_tree.file_tree.FileTree.add_subtree>`) after reading in the FileTree.
    - Sub-trees no longer need to have a precorsor key. This used to be a requirement with all keys in the sub-trees being updated
      with to "<precursor>/<original key>". If no precursor is provided, the keys in the sub-tree will simply not be updated.
    - Sub-trees are also now incorporated into the main tree rather than stored separately. This means you can no longer use `get_subtree`.
    - You can now write FileTrees back to a string (:meth:`FileTree.to_string <file_tree.file_tree.FileTree.to_string>`).
      This allows you to see what templates are defined in the FileTree without opening the original definition (or to write the FileTree back to disk).
