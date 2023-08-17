cat structure2.xml \
    | xsltproc xslt/flatten_structure3.xml /dev/stdin \
    >  flat_structure3.xml
