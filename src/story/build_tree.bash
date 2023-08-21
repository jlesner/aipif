cat structure_0010.xml \
    | xsltproc xslt_002/p0010_flatten_structure3.xml /dev/stdin \
    | xsltproc xslt_002/p0020_add_path.xml /dev/stdin \
    | xsltproc xslt_002/p0025_add_tree.xml /dev/stdin \
    | xsltproc xslt_002/p0030_build_tree.xml /dev/stdin \
    | python3 xml_format.py \
    | grep -v '^<\?xml' \
    | grep -v '^ *$' \
    | cat \
    | less -S

exit
    | xsltproc xslt_002/p0031_simulate_response.xml /dev/stdin \


    | xsltproc xslt_002/p0040_build_tree.xml /dev/stdin \

    | perl -pe's/\${emoji_list}/🐧🍕🥄🏝👽/g;' \