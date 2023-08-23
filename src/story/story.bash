# set -o errexit
# set -o pipefail
set -o nounset
set -o xtrace

export outp=_generated

xml_api_bridge()
{
    # python3 ../api/StubXmlApiBridge.py
    python3 ../api/SingleThreadXmlApiBridge.py
    # python3 ../api/MultiThreadXmlApiBridge.py
} ; export -f xml_api_bridge

xml_api_worker()
{
    python3 ../api/XmlApiQueueWorker.py
} ; export -f xml_api_worker

rq_xml_api_bridge()
{
    python3 ../api/QueuingXmlApiBridge.py 
} ; export -f rq_xml_api_bridge


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

tree_cat()
{
    cat structure_0010.xml
    # cat structure_0011.xml
    # cat structure_0011.xml
} ; export -f tree_cat

tree_grow()
{
    # local nss=011
    # local nss=016
    local nss=003
    local pss=000

    tree_cat \
        | xsltproc xslt_002/p0010_structure_flatten.xml /dev/stdin \
        | xsltproc xslt_002/p0020_path_add.xml /dev/stdin \
        | xsltproc xslt_002/p0025_tree_add.xml /dev/stdin \
        | xml_fix \
        > ${outp}/tree_${pss}_out.xml

    seq $nss \
        | while read s ; do
            ss=`printf "%03d" $s`
            cat ${outp}/tree_${pss}_out.xml \
                | xsltproc xslt_002/p0030_tree_grow.xml /dev/stdin \
                | xml_fix \
                | tee ${outp}/tree_${ss}_in.xml \
                | xml_api_bridge \
                | xml_fix \
                | tee ${outp}/tree_${ss}_out.xml \
                > /dev/null
            pss=$ss
        done

    cat ${outp}/tree_${nss}_out.xml \
        | xsltproc xslt_002/p0050_key_add.xml /dev/stdin \
        | xsltproc xslt_002/p0060_path_drop.xml /dev/stdin \
        | xml_fix \
        > ${outp}/tree_${nss}_zzz.xml

} ; export -f tree_grow


tree_grow_run()
{
    (rm -f ${outp}/*.xml || true )  2> /dev/null
    (rm -f _cache/*.{json,xml} || true )  2> /dev/null
    tree_grow
} ; export -f tree_grow_run


tree_decorate()
{
    xsltproc xslt_002/p0070_media_request.xml /dev/stdin \
        | rq_xml_api_bridge \
        | xml_fix
} ; export -f tree_decorate


queue_pass()
{
    while read f ; do
        if test -f "${f}.lock" || test -f "${f}.res.xml" ; then
            continue
        fi
        
        touch "${f}.lock"

        (
            cat $f \
                | xml_api_worker
        ) \
            | tee -a "${f}.res.xml"

        rm "${f}.lock"
    done

} ; export -f queue_pass


picture_worker()
{
    (
        source ~/aipif/sd_venv/bin/activate        
        queue_path=_queue
        while true ; do
            find $queue_path -type f -name 'make_picture-*-req.xml' \
                | head -n 1 \
                | queue_pass
            echo -n . 
            sleep 4
        done
    )
} ; export -f picture_worker