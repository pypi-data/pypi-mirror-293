.. file-tree documentation master file, created by
   sphinx-quickstart on Fri Jan 29 16:46:10 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to file-tree's documentation!
=====================================
This is the documentation for file-tree, a project designed to allow you to separate the directory structure of your pipeline inputs/outputs from the actual pipeline code.

Install using
::

   conda/pip install file-tree file-tree-fsl

Include the `file-tree-fsl` package if you want to use filetree definitions for the FSL tools.
If you want to use the terminal-based user interface, you will also need to install textual.
You can install this using `conda/pip install textual`.

The pipeline results can be visualised efficiently in FSLeyes as described in https://open.win.ox.ac.uk/pages/fsl/fsleyes/fsleyes/userdoc/filetree.html .

Please report any bugs/issues/feature requests using the gitlab interface (https://git.fmrib.ox.ac.uk/fsl/file-tree/-/issues).

.. raw:: html

   <iframe src="https://ox.cloud.panopto.eu/Panopto/Pages/Embed.aspx?id=fccf6d47-a745-4290-b218-af5a00aeb467&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

.. toctree::
   :maxdepth: 3

   tutorial
   changes
   file_tree
