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
        | ( grep -v '^<\?xml' || true ) \
        | ( grep -v '^ *$' || true ) \
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


story_publish_run() {
    (
        story_configure
        cat _sample/tree_016_zzz3.xml \
            | story_publish
    )
} ; export -f story_publish_run


story_configure()
{
    export job_label=tw0102
    export zzz_sample=_sample/tree_016_zzz3.xml

    . ~/aipif/.env
    export PYTHONPATH=~/aipif/src
    export s3_bucket=aipif-2023
    export s3_path_prefix="sample/${job_label}_"
    export s3_prefix="s3://${s3_bucket}/${s3_path_prefix}"
    export fs_prefix="_generated/${job_label}_"
} ; export -f story_configure


story_publish()
{
    local twine_path=../twine

    cat - \
        | tree_decorate \
        > ${fs_prefix}decorated.xml

    cat ${fs_prefix}decorated.xml \
        | tee >( aws s3 cp - ${s3_prefix}tree.xml --content-type application/xml ) \
        | tr -s " " \
        | xsltproc ${twine_path}/xslt/problem_char_fix.xml /dev/stdin \
        | fmt -w 60 \
        | xsltproc ${twine_path}/xslt/mmfc_generate.xml /dev/stdin \
        | tee >( aws s3 cp - ${s3_prefix}tree.html --content-type text/html ) \
        > ${fs_prefix}tree.html

    cat ${fs_prefix}decorated.xml  \
        | xsltproc ${twine_path}/xslt/prompt_remove.xml /dev/stdin \
        | xsltproc ${twine_path}/xslt/sugarcube_twine_generate4.xml /dev/stdin \
        | perl -pe"s{http://aipif-2023.s3.amazonaws.com/sample/}{http://${s3_bucket}.s3.amazonaws.com/${s3_path_prefix}}g;" \
        | tee >( aws s3 cp - ${s3_prefix}twine.twee.txt --content-type "text/plain" --metadata "Content-Disposition=inline") \
        > ${fs_prefix}twine.twee

    /opt/tweego-2.1.1-linux-x64/tweego -f sugarcube-2 -o /dev/stdout \
        ${fs_prefix}twine.twee \
        | tee >( aws s3 cp - ${s3_prefix}twine.html --content-type "text/html" --metadata "Content-Disposition=inline") \
        > ${fs_prefix}twine.html

} ; export -f story_publish


fs_queue_pass()
{
    while read f ; do
        if test -f "${f}.lock" || test -f "${f}.log" ; then
            continue
        fi

        touch "${f}.lock"

        (
            cat $f \
                | tee /dev/stderr \
                | rq_worker
        ) 2>&1 \
            | tee /dev/stderr \
            | tee -a "${f}.log"

        rm "${f}.lock"
    done

} ; export -f fs_queue_pass



fs_rq_worker()
{
    local filter=$1
    (
        source ~/aipif/sd_venv/bin/activate
        while true ; do
            find _queue -type f -maxdepth 1 \
                | perl -pe's{^(.+-req.xml).*}{$1}g;' \
                | sort \
                | uniq -u \
                | ( egrep -a "$filter" || true ) \
                | head -n 1 \
                | fs_queue_pass
            echo -n .
            sleep 10
        done
    ) 2>&1 \
        | tee _generated/fs_rq_worker.log
} ; export -f fs_rq_worker


fs_rq_worker_run()
{
    (
        clear
        . ~/aipif/.env
        . ../common/aws.bash
        export PYTHONPATH=~/aipif/src
        fs_rq_worker make_picture
    )
} ; export -f fs_rq_worker_run


s3_queue_pass()
{
    while read f ; do

        if s3_exists "_queue/${f}.lock" || s3_exists "_queue/${f}.log" ; then
            continue
        fi

        s3_touch "_queue/${f}.lock"
        touch "_queue/${f}.lock"

        (
            s3_get "_queue/${f}" \
                | tee /dev/stderr \
                | rq_worker
        ) 2>&1 \
            | tee /dev/stderr \
            | tee "_queue/${f}.log" \
            | s3_txt_stream "_queue/${f}.log"
            # | tee /dev/stderr \

        s3_rm "_queue/${f}.lock"
        rm "_queue/${f}.lock"
    done

} ; export -f fs_queue_pass


s3_rq_worker()
{
    local filter=$1
    mkdir -p _queue 2>/dev/null || true
    (
        while true ; do
            s3_file_ls "_queue/" \
                | tee s3_file_ls.out \
                | perl -pe's{^(.+-req.xml).*}{$1}g;' \
                | sort \
                | uniq -u \
                | ( egrep -a "$filter" || true ) \
                | head -n 1 \
                | s3_queue_pass
            echo -n .
            break
            sleep 10
        done
    ) 2>&1 \
        | tee s3_rq_worker.log
} ; export -f s3_rq_worker


s3_queue_sync()
{
    aws s3 rm --recursive s3://${s3_bucket}/_queue
    aws s3 cp --recursive _queue s3://${s3_bucket}/_queue
} ; export -f s3_queue_sync


s3_rq_worker_run()
{
    (
        story_configure
        source ../common/aws.bash
        source ~/aipif/sd_venv/bin/activate
        pip install -r ../pictures/requirements.txt
        # s3_queue_sync
        s3_rq_worker make_picture
        # aws s3 rm s3://aipif-2023/_queue/make_picture-7ccab19d-req.xml.log
        # aws s3 rm s3://aipif-2023/_queue/make_picture-7ccab19d-req.xml.lock
        # echo make_picture-7ccab19d-req.xml \
        #     | s3_queue_pass 
    )
} ; export -f s3_rq_worker_run

