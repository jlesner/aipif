cat tree_016_zzz3.xml \
| tr -s " " \
| xsltproc xslt/problem_char_fix.xml /dev/stdin \
| fmt -w 60 \
| xsltproc xslt/mmfc_generate.xml /dev/stdin > _generated/mermaid_fc.html

# | tee remove_char.xml \