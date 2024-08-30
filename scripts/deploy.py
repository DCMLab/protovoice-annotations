import glob
from pathlib import Path
import shutil
from string import Template


def insert_path(path, node, parts=None):
    if parts is None:
        parts = path.parts

    if len(parts) > 1:
        if parts[0] in node:
            next_node = node[parts[0]]
        else:
            next_node = {}
        insert_path(path, next_node, parts[1:])
    else:
        next_node = path
    node[parts[0]] = next_node


def tree_to_html(node, node_name=""):
    if isinstance(node, Path):
        return f'<a href="{node}">{node.stem}</a>'
    else:
        entries = sorted(node.keys())
        content = "\n".join([f'<li>{tree_to_html(node[entry], entry)}</li>'
                             for entry in entries])
        return f"{node_name}\n<ul>\n{content}\n</ul>"


def deploy():
    # reset dist dir
    dist = Path("dist/")
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()

    # load templates
    with open("scripts/viewer.html") as f:
        template_viewer = Template(f.read())

    # walk over analysis files
    dir_tree = {}
    for fn in glob.glob("**/*.analysis.json", recursive=True):
        ana_path = Path(fn)
        ana_dest = dist / ana_path
        ana_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ana_path, ana_dest)
        html_path = ana_path.with_suffix('').with_suffix(".html")
        html_dest = dist / html_path
        insert_path(html_path, dir_tree)
        viewer_html = template_viewer.substitute({
            "filename":
            Path("https://dcmlab.github.io/protovoice-annotations/") / ana_path
        })
        with open(html_dest, "w", encoding="utf-8") as f:
            f.write(viewer_html)
        print("Wrote", html_path)

    # generate index.html with the directory tree
    with open("scripts/index.html") as f:
        template_index = Template(f.read())
    index_html = template_index.substitute({"listing": tree_to_html(dir_tree)})
    with open(Path("dist/index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)


deploy()
