export outp=_generated


xml_api_bridge()
{
    python3 ../api/StubXmlApiBridge.py
    # python3 ../api/SingleThreadXmlApiBridge.py
    # python3 ../api/MultiThreadXmlApiBridge.py
} ; export -f xml_api_bridge


xml_fix()
{
    python3 xml_format.py \
        | grep -v '^<\?xml' \
        | grep -v '^ *$'
} ; export -f xml_fix


xml_trim()
{
    grep -v '^[A-Za-z]' \
    | cut -c 1-`tput cols` \
    | head -n `tput lines`
} ; export -f xml_trim


tree_grow()
{
    local pss=000;

    cat structure_0011.xml \
        | xsltproc xslt_002/p0010_structure_flatten.xml /dev/stdin \
        | xsltproc xslt_002/p0020_path_add.xml /dev/stdin \
        | xsltproc xslt_002/p0025_tree_add.xml /dev/stdin \
        | xml_fix \
        > ${outp}/tree_${pss}_out.xml

    seq 2 \
        | while read s ; do
            ss=`printf "%03d" $s`
            cat ${outp}/tree_${pss}_out.xml \
                | xsltproc xslt_002/p0030_tree_grow.xml /dev/stdin \
                | xml_fix \
                | tee${outp}/tree_${ss}_in.xml \
                | xml_api_bridge \
                | xml_fix \
                | tee ${outp}/tree_${ss}_out.xml \
                > /dev/null
            pss=$ss
        done

    cat ${outp}/tree_${pss}_out.xml \
        | xsltproc xslt_002/p0080_key_add.xml /dev/stdin \
        | xsltproc xslt_002/p0090_path_drop.xml /dev/stdin \
        | xml_fix \
        > ${outp}/tree_${pss}_last.xml

} ; export -f tree_grow

tree_grow
