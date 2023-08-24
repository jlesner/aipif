cat story/_sample/tree_016_zzz6_url.xml \
    | tee >( aws s3 cp - s3://aipif-2023/sample/tree.xml ) \
    | tr -s " " \
    | xsltproc twine/xslt/problem_char_fix.xml /dev/stdin \
    | fmt -w 60 \
    | xsltproc twine/xslt/mmfc_generate.xml /dev/stdin \
    | tee >( aws s3 cp - s3://aipif-2023/sample/tree.html )  \
    > twine/_generated/mermaid_fc.html

# | tee remove_char.xml \