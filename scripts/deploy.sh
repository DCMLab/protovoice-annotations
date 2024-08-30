#!/bin/sh

process_file() {
    cat <<EOF
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Protovoice Viewer</title>
    <link href="https://dcmlab.github.io/protovoice-annotation-tool/viewer/css/pure/pure-min.css" rel="stylesheet" type="text/css">
    <link href="https://dcmlab.github.io/protovoice-annotation-tool/viewer/css/pure/grids-responsive-min.css"
          rel="stylesheet" type="text/css">
    <link href="https://dcmlab.github.io/protovoice-annotation-tool/viewer/css/pv-style.css" rel="stylesheet" type="text/css">
  </head>
  <body>
    <div id="widget"></div>
    <script type="module">
      import * as viewer from "https://dcmlab.github.io/protovoice-annotation-tool/viewer/module/module.js";

      fetch("/$1")
        .then((resp) => resp.text())
        .then((json) => viewer.createViewer("#widget", json));
    </script>
  </body>
</html>
EOF
}

[ -d dist ] && rm -r dist
mkdir dist
files=$(find . -type f -name "*.analysis.json")
echo "$files" | while read -r file; do
    base="dist/${file%.analysis.json}"
    mkdir -p "$(dirname "$base")"
    cp "$file" "dist/$file"
    process_file "$file" > "${base}.html"
done
