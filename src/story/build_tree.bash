cat structure_0010.xml \
    | xsltproc xslt_002/p0010_structure_flatten.xml /dev/stdin \
    \
    | xsltproc xslt_002/p0020_path_add.xml /dev/stdin \
    | xsltproc xslt_002/p0025_tree_add.xml /dev/stdin \
    | tee _generated/p0025_tree_add.xml \
    \
    | xsltproc xslt_002/p0030_tree_grow.xml /dev/stdin \
    | tee _generated/p00311_response_simulate.xml \
    | xsltproc xslt_002/p0031_response_simulate.xml /dev/stdin \
    | tee _generated/p00312_response_simulate.xml \
    \
    | xsltproc xslt_002/p0030_tree_grow.xml /dev/stdin \
    | tee _generated/p00321_response_simulate.xml \
    | xsltproc xslt_002/p0032_response_simulate.xml /dev/stdin \
    | tee _generated/p00322_response_simulate.xml \
    \
    | xsltproc xslt_002/p0030_tree_grow.xml /dev/stdin \
    | xsltproc xslt_002/p0033_response_simulate.xml /dev/stdin \
    | tee _generated/p00332_response_simulate.xml \
    \
    | xsltproc xslt_002/p0030_tree_grow.xml /dev/stdin \
    | xsltproc xslt_002/p0034_response_simulate.xml /dev/stdin \
    | tee _generated/p00342_response_simulate.xml \
    \
    | xsltproc xslt_002/p0030_tree_grow.xml /dev/stdin \
    | tee _generated/p00351_response_simulate.xml \
    | xsltproc xslt_002/p0035_response_simulate.xml /dev/stdin \
    | tee _generated/p00352_response_simulate.xml \
    \
    | xsltproc xslt_002/p0030_tree_grow.xml /dev/stdin \
    | xsltproc xslt_002/p0036_response_simulate.xml /dev/stdin \
    | tee _generated/p00362_response_simulate.xml \
    \
    | xsltproc xslt_002/p0080_key_add.xml /dev/stdin \
    | xsltproc xslt_002/p0090_path_drop.xml /dev/stdin \
    \
    | python3 xml_format.py \
    | grep -v '^<\?xml' \
    | grep -v '^ *$' \
    | cat

exit
    | xsltproc xslt_002/p0090_drop_non_request_detail.xml /dev/stdin \
    
    
    

    | grep -v '^[A-Za-z]' \
    | cut -c 1-`tput cols` \
    | head -n `tput lines` \
