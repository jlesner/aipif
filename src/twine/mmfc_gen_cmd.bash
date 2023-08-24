    # --metadata "Content-Disposition=inline") \
    # --metadata "Content-Disposition=inline")  \

## TODO make sure xml has <?xml version="1.0" encoding="UTF-8"?>

cat story/_sample/tree_016_zzz6_url.xml \
    | tee >( aws s3 cp - s3://aipif-2023/sample/tree.xml --content-type application/xml ) \
    | tr -s " " \
    | xsltproc twine/xslt/problem_char_fix.xml /dev/stdin \
    | fmt -w 60 \
    | xsltproc twine/xslt/mmfc_generate.xml /dev/stdin \
    | tee >( aws s3 cp - s3://aipif-2023/sample/tree.html --content-type text/html ) \
    > twine/_generated/mermaid_fc.html

# | tee remove_char.xml \
# http://aipif-2023.s3.amazonaws.com/sample/tree.html

# aws s3 cp story/_sample/tree_016_zzz6_url.xml s3://aipif-2023/sample/tree.xml --content-type application/xml
