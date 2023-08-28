# set -o pipefail
set -o xtrace
set -o nounset
set -o errexit
# export output_path=_generated

# TODO make sure generated XML is marked with UTF-8 encoding
# TODO give media elements rq_id attribute before url attribute

story_configure()
{
    local rq_id="$1"
    
    export output_path="_generated/story_${rq_id}"    
    export fs_path_prefix="${output_path}/p0090-"

    export PYTHONPATH=~/aipif/src
    export twine_path=../twine
    # . ~/aipif/.env # TODO move outside to prevent logging
    # export zzz_sample=_sample/tree_016_zzz3.xml

    export s3_bucket=aipif-2023
    export s3_bucket_prefix="story/story_${rq_id}/p0090-"
    export s3_path_prefix="s3://${s3_bucket}/${s3_bucket_prefix}"


    # export tweego_bin=/opt/tweego-2.1.1-linux-x64/tweego 
    export tweego_bin=~/aipif/_exclude/tweego-2.1.1-linux-x64/tweego


} ; export -f story_configure


structure_cat()
{
    cat structure_1111-11112-111110.xml # 2 endings
    # cat structure_1112-11112-111110.xml # 4 endings 
    # cat structure_1112-11112-121210.xml # 16 endings
    # cat structure_1112-12112-121210.xml # 32 endings
} ; export -f structure_cat


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
    python3 ../api/S3RqApiBridge.py
    # python3 ../api/FsRqApiBridge.py
    # python3 ../api/RqXmlApiBridge.py

} ; export -f rq_api_bridge


rq_worker()
{
    python3 ../api/RqWorker.py
} ; export -f rq_worker


MusicRqWorker()
{
    python3 ../api/MusicRqWorker.py
} ; export -f MusicRqWorker


PictureRqWorker()
{
    python3 ../api/PictureRqWorker.py
} ; export -f PictureRqWorker


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


tree_grow()
{
    local prompt="$1"
    # local nss=011
    local nss=018
    # local nss=003
    local pss=000

    structure_cat \
        | tee ${output_path}/p0000_tree_cat_out.xml \
        \
        | xsltproc xslt_002/p0010_structure_flatten.xml /dev/stdin \
        | xml_fix \
        | tee ${output_path}/p0010_structure_flatten_out.xml \
        \
        | xsltproc xslt_002/p0020_path_add.xml /dev/stdin \
        | xml_fix \
        | tee ${output_path}/p0020_path_add_out.xml \
        \
        | xsltproc xslt_002/p0022_reaction_add.xml /dev/stdin \
        | xml_fix \
        | tee ${output_path}/p0022_reaction_add_out.xml \
        \
        | xsltproc xslt_002/p0025_tree_add.xml /dev/stdin \
        | perl -pe"s{⛄🌞🚚🗻🍦}{$prompt}g" \
        | xml_fix \
        | tee ${output_path}/p0025_tree_add_out.xml \
        \
        > ${output_path}/p0030_tree_${pss}_out.xml

    seq $nss \
        | while read s ; do
            ss=`printf "%03d" $s`
            cat ${output_path}/p0030_tree_${pss}_out.xml \
                \
                | xsltproc xslt_002/p0030_tree_grow.xml /dev/stdin \
                | xml_fix \
                | tee ${output_path}/p0030_tree_${ss}_in.xml \
                \
                | xml_api_bridge \
                | xml_fix \
                | tee ${output_path}/p0030_tree_${ss}_out.xml \
                \
                > /dev/null
            pss=$ss
        done

    cat ${output_path}/p0030_tree_${nss}_out.xml \
        | xsltproc xslt_002/p0050_key_add.xml /dev/stdin \
        | xml_fix \
        | tee ${output_path}/p0050_key_add_out.xml \
        \
        | xsltproc xslt_002/p0060_path_drop.xml /dev/stdin \
        | xml_fix \
        | tee ${output_path}/p0060_path_drop_out.xml \
        \
        | xsltproc xslt_002/p0065_patch_sound.xml /dev/stdin \
        | xml_fix \
        | tee ${output_path}/p0065_patch_sound_out.xml 

        # \
        # \
        # | tee ${output_path}/tree_${nss}_zzz.xml

} ; export -f tree_grow


# tree_grow_run()
# {
#     (rm -f ${output_path}/*.xml || true )  2> /dev/null
#     (rm -f _cache/*.{json,xml} || true )  2> /dev/null
#     tree_grow
# } ; export -f tree_grow_run


tree_decorate()
{
    xsltproc xslt_002/p0070_media_request.xml /dev/stdin \
        | xml_fix \
        | tee ${output_path}/p0070_media_request_out.xml \
        \
        | rq_api_bridge \
        | xml_fix \
        | tee ${output_path}/p0071_rq_api_bridge_out.xml \
        \
        | xsltproc xslt_002/p0080_url_add.xml /dev/stdin \
        | xml_fix \
        | tee ${output_path}/p0080_url_add_out.xml
} ; export -f tree_decorate


story_publish()
{
    cat - \
        | tree_decorate \
        > ${fs_path_prefix}decorated.xml

    cat ${fs_path_prefix}decorated.xml \
        | tee >( aws s3 cp - ${s3_path_prefix}tree.xml --content-type application/xml ) \
        | tr -s " " \
        | xsltproc ${twine_path}/xslt/problem_char_fix.xml /dev/stdin \
        | fmt -w 40 \
        | xsltproc ${twine_path}/xslt/mmfc_generate.xml /dev/stdin \
        | tee >( aws s3 cp - ${s3_path_prefix}tree.html --content-type text/html ) \
        > ${fs_path_prefix}tree.html

    cat ${fs_path_prefix}decorated.xml \
        | tr -s " " \
        | fmt -w 60 \
        | xsltproc ${twine_path}/xslt/pgallery_generate.xml /dev/stdin \
        | tee >( aws s3 cp - ${s3_path_prefix}pgallery.html --content-type text/html ) \
        > ${fs_path_prefix}pgallery.html

    cat ${fs_path_prefix}decorated.xml \
        | tr -s " " \
        | fmt -w 60 \
        | xsltproc ${twine_path}/xslt/sgallery_generate.xml /dev/stdin \
        | tee >( aws s3 cp - ${s3_path_prefix}sgallery.html --content-type text/html ) \
        > ${fs_path_prefix}sgallery.html

    cat ${fs_path_prefix}decorated.xml \
        | tr -s " " \
        | fmt -w 60 \
        | xsltproc ${twine_path}/xslt/mgallery_generate.xml /dev/stdin \
        | tee >( aws s3 cp - ${s3_path_prefix}mgallery.html --content-type text/html ) \
        > ${fs_path_prefix}mgallery.html

        # | xsltproc ${twine_path}/xslt/prompt_remove.xml /dev/stdin \
    cat ${fs_path_prefix}decorated.xml  \
        | xsltproc ${twine_path}/xslt/sugarcube_twine_generate6.xml /dev/stdin \
        | perl -pe"s{http://aipif-2023.s3.amazonaws.com/sample/}{http://${s3_bucket}.s3.amazonaws.com/${s3_bucket_prefix}}g;" \
        | tee >( aws s3 cp - ${s3_path_prefix}twine.twee.txt --content-type "text/plain" --metadata "Content-Disposition=inline") \
        > ${fs_path_prefix}twine.twee

    $tweego_bin -f sugarcube-2 -o /dev/stdout \
        ${fs_path_prefix}twine.twee \
        | tee >( aws s3 cp - ${s3_path_prefix}twine.html --content-type "text/html" --metadata "Content-Disposition=inline") \
        > ${fs_path_prefix}twine.html

} ; export -f story_publish


# story_publish_run() {
#     (
#         story_configure
#         cat _sample/tree_016_zzz3.xml \
#             | story_publish
#     )
# } ; export -f story_publish_run


fs_story_make()
{ 
    local rq_id="$1"
    local prompt="$2"
    
    story_configure "$rq_id"
    
    # rm -f _cache/*.{json,xml} 2>/dev/null || true
    rm -rf ${output_path} 2>/dev/null || true
    mkdir -p ${output_path} 2>/dev/null || true
    (        
        tree_grow "$prompt" \
            | story_publish 
    )

    (
        export s3_bucket=${s3_bucket}b # TODO fix
        s3_touch "${rq_id}_${prompt}"
    )

    # tar cfz - ${output_path} \
    #     | aws s3 cp - ${fs_path_prefix}trace.tar.gz

    # rm -rf ${output_path} 2>/dev/null || true

} ; export -f fs_story_make


fs_story_make_run()
{
    (
        . ~/aipif/.env
        export OPENAI_API_KEY
        . ../common/aws.bash
        export PYTHONPATH=~/aipif/src
        # fs_story_make bob "🎈🌵🦉🍉🚁🎻"
        # fs_story_make bill "🌓🍏🦜🍥🚝🎸"
        # fs_story_make c1 "🐔🎤🎶🕺💃🎉"
        # fs_story_make c2 "🐌🏎️💨🏁🎈🏆"
        # fs_story_make c4 "🐭🧀🌍🚀🌔🎉"
        fs_story_make c3 "🐵🙈🙉🙊🍌🎢"
    )
} ; export -f fs_story_make_run


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
    local rq_worker=$1
    while read f ; do

        if s3_exists "_queue/${f}.lock" || s3_exists "_queue/${f}.log" ; then
            continue
        fi

        s3_touch "_queue/${f}.lock"
        touch "_queue/${f}.lock"

        (
            s3_get "_queue/${f}" \
                | tee /dev/stderr \
                | ${rq_worker}
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
    local rq_worker=$1
    local filter=$2
    mkdir -p _queue 2>/dev/null || true
    (
        while true ; do
            s3_file_ls "_queue/" \
                | perl -pe's{^(.+-req.xml).*}{$1}g;' \
                | sort \
                | uniq -u \
                | ( egrep -a "$filter" || true ) \
                | sort -R \
                | s3_queue_pass ${rq_worker}
                # | head -n 1 \
            echo -n .
            # break
            sleep 10
        done
    ) 2>&1 \
        | tee s3_rq_worker_${filter}.log
} ; export -f s3_rq_worker


s3_queue_push()
{
    aws s3 rm --recursive s3://${s3_bucket}/_queue
    aws s3 cp --recursive _queue s3://${s3_bucket}/_queue
} ; export -f s3_queue_push


s3_queue_pull()
{
    # rm -rf _queue
    aws s3 cp --recursive s3://${s3_bucket}/_queue _queue 
} ; export -f s3_queue_pull


picture_worker_run()
{
    (
        story_configure stub
        source ../common/aws.bash
        source ~/aipif/sd_venv/bin/activate
        pip install -r ../pictures/requirements.txt
        # s3_queue_sync
        s3_rq_worker PictureRqWorker make_picture
        # aws s3 rm s3://aipif-2023/_queue/make_picture-7ccab19d-req.xml.log
        # aws s3 rm s3://aipif-2023/_queue/make_picture-7ccab19d-req.xml.lock
        # echo make_picture-7ccab19d-req.xml \
        #     | s3_queue_pass 
    )
} ; export -f picture_worker_run


music_worker_run()
{
    (
        story_configure stub
        source ../common/aws.bash
        source ~/aipif/mu_venv/bin/activate
        pip install -r ../music/requirements.txt
        # s3_queue_sync
        s3_rq_worker MusicRqWorker make_music
        # aws s3 rm s3://aipif-2023/_queue/make_picture-7ccab19d-req.xml.log
        # aws s3 rm s3://aipif-2023/_queue/make_picture-7ccab19d-req.xml.lock
        # echo make_picture-7ccab19d-req.xml \
        #     | s3_queue_pass 
    )
} ; export -f music_worker_run

# aws s3 ls aipif-2023/_queue/ | tr -s " "  | cut -f4 | grep lock | cut -d" " -f4  | while read f ; do aws s3 rm s3://"aipif-2023/_queue/${f}" ; done

#  grep -l OutOfMemoryError  _queue/make_picture-*log | while read f ; do aws s3 rm s3://"aipif-2023/${f}" ; done
