cat structure.xml \
    | xsltproc xslt/flatten_structure2.xml /dev/stdin \
    >  flat_structure2.xml
