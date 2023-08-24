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


xml_format()
{
    python3 ../common/xml_format.py
} ; export -f xml_format


rq_api_bridge()
{
    python3 ../api/RqXmlApiBridge.py
} ; export -f rq_api_bridge


rq_worker()
{
    python3 ../api/RqWorker.py
} ; export -f rq_worker


xml_fix()
{
    xml_format \
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
        | rq_api_bridge \
        | xsltproc xslt_002/p0080_url_add.xml /dev/stdin \
        | xml_fix
} ; export -f tree_decorate


fs_queue_pass()
{
    while read f ; do
        if test -f "${f}.lock" || test -f "${f}.log" ; then
            continue
        fi

        touch "${f}.lock"

        (
            cat $f \
                | rq_worker
        ) 2>&1 \
            | tee -a "${f}.log"

        rm "${f}.lock"
    done

} ; export -f fs_queue_pass


s3_queue_pass()
{
    while read f ; do

        if s3_exists "_queue/${f}.lock" || s3_exists "_queue/${f}.log" ; then
            continue
        fi

        s3_touch "_queue/${f}.lock"

        (
            s3_cat "_queue/${f}" \
                | rq_worker
        ) 2>&1 \
            | tee "_queue/${f}.log" \
            | s3_txt_stream "_queue/${f}.log"
            # | tee /dev/stderr \

        s3_rm "_queue/${f}.lock"
    done

} ; export -f fs_queue_pass


fs_rq_worker()
{
    local filter=$1
    (
        source ~/aipif/sd_venv/bin/activate
        while true ; do
            find _queue -type f \
                | perl -pe's{^(.+-req.xml).*}{$1}g;' \
                | sort \
                | uniq -u \
                | ( egrep -a "$filter" || true ) \
                | head -n 1 \
                | queue_pass
            echo -n .
            sleep 4
        done
    ) 2>&1 \
        | tee fs_rq_worker.log
} ; export -f fs_rq_worker


s3_rq_worker()
{
    local filter=$1
    mkdir -p _queue 2>/dev/null || true
    (
        source ~/aipif/sd_venv/bin/activate
        while true ; do
            s3_file_ls "_queue/" \
                | perl -pe's{^(.+-req.xml).*}{$1}g;' \
                | sort \
                | uniq -u \
                | ( egrep -a "$filter" || true ) \
                | head -n 1 \
                | s3_queue_pass
            echo -n .
            sleep 5
        done
    ) 2>&1 \
        | tee s3_rq_worker.log
} ; export -f s3_rq_worker


s3_queue_sync()
{
    aws s3 cp --recursive src/story/_queue s3://${s3_bucket}/_queue
} ; export -f s3_queue


run() {
    (
        clear
        . ~/aipif/.env
        export PYTHONPATH=~/aipif/src
        cat _sample/tree_016_zzz3.xml \
            | tree_decorate \
            > _generated/decorated.xml
    )
} ; export -f run
