cat story_structure_0010.xml \
    | xsltproc xslt_002/p0010_flatten_structure3.xml /dev/stdin \
    | xsltproc xslt_002/p0020_add_repeated_elements.xml /dev/stdin \
    | xsltproc xslt_002/p0030_first_scene_template.xml /dev/stdin \
    | python3 xml_format.py \
    | grep -v '^<\?xml' \
    | grep -v '^ *$' \
    >  first_scene_template.xml

cat story_structure_0010.xml \
    | xsltproc xslt_002/p0010_flatten_structure3.xml /dev/stdin \
    | xsltproc xslt_002/p0020_add_repeated_elements.xml /dev/stdin \
    | xsltproc xslt_002/p0033_next_scene_template.xml /dev/stdin \
    | python3 xml_format.py \
    | grep -v '^<\?xml' \
    | grep -v '^ *$' \
    >  next_scene_template.xml

