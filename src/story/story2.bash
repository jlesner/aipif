# set -o pipefail
set -o xtrace
set -o nounset
set -o errexit
# export output_path=_generated

story_configure()
{
    local rq_id="$1"

    export phome=~/aipif
    export PYTHONPATH=${phome}/src
    export twine_path=${phome}/src/twine
    
    export output_path="_generated/story_${rq_id}"    
    export fs_path_prefix="${output_path}/p0090-"

    # . ~/aipif/.env # TODO move outside to prevent logging
    # export zzz_sample=_sample/tree_016_zzz3.xml

    export s3_bucket=aipif-2023
    export s3_bucket_prefix="story/story_${rq_id}/p0090-"
    export s3_path_prefix="s3://${s3_bucket}/${s3_bucket_prefix}"

    # export tweego_bin=/opt/tweego-2.1.1-linux-x64/tweego 
    export tweego_bin=${phome}/_exclude/tweego-2.1.1-linux-x64/tweego

    source ../common/aws.bash

} ; export -f story_configure


structure_cat()
{
    # cat structure_1111-11112-111110.xml # 2 endings
    # cat structure_1112-11112-111110.xml # 4 endings 
    # cat structure_1112-11112-121210.xml # 16 endings
    cat structure_1112-12112-121210.xml # 32 endings
} ; export -f structure_cat


xml_api_bridge()
{
    python3 ../api/SingleThreadXmlApiBridge8k.py
    # python3 ../api/MultiThreadXmlApiBridge.py
} ; export -f xml_api_bridge



xml_api_bridge2()
{
    local ss="$1"

    if [[ "$ss" -lt 7 ]]; then
        python3 ../api/SingleThreadXmlApiBridge.py
    else
        python3 ../api/SingleThreadXmlApiBridge8k.py
    fi
    
    # python3 ../api/StubXmlApiBridge.py
    # python3 ../api/SingleThreadXmlApiBridge8k.py
    # python3 ../api/MultiThreadXmlApiBridge.py
} ; export -f xml_api_bridge2


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


# rq_worker()
# {
#     python3 ../api/RqWorker.py
# } ; export -f rq_worker


MusicRqWorker()
{
    python3 ../api/MusicRqWorker.py
} ; export -f MusicRqWorker


PictureRqWorker()
{
    python3 ../api/PictureRqWorker.py
} ; export -f PictureRqWorker


SoundRqWorker()
{
    python3 ../api/SoundRqWorker.py
} ; export -f SoundRqWorker


StoryRqWorker()
{
    python3 ../api/StoryRqWorker.py
} ; export -f StoryRqWorker


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
    # local nss=005
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

                # grep -F '<error>' < ${output_path}/p0030_tree_${ss}_out.xml \
                #     && echo "tree_grow() ABORTED DUE TO ERROR in ${output_path}/p0030_tree_${ss}_out.xml" \
                #     && return 1
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


py_fs_story_make()
{
    export PYTHONPATH=~/aipif/src
    source ~/aipif/.env
    export OPENAI_API_KEY
    fs_story_make "$@"
}


fs_story_make()
{ 
    local rq_id="$1"
    local prompt="$2"
    
    (
        story_configure "$rq_id"
        # rm -f _cache/*.{json,xml} 2>/dev/null || true
        rm -rf ${output_path} 2>/dev/null || true
        mkdir -p ${output_path} 2>/dev/null || true

        # set -o allexport
        # source ${phome}/.env
        # export OPENAI_API_KEY
        tree_grow "$prompt" \
            | story_publish

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
        export PYTHONPATH=~/aipif/src
        . ~/aipif/.env
        export OPENAI_API_KEY


        # . ../common/aws.bash
        # fs_story_make bob "🎈🌵🦉🍉🚁🎻"
        # fs_story_make bill "🌓🍏🦜🍥🚝🎸"
        # fs_story_make c1 "🐔🎤🎶🕺💃🎉"
        # fs_story_make c2 "🐌🏎️💨🏁🎈🏆"
        # fs_story_make c4 "🐭🧀🌍🚀🌔🎉"
        # fs_story_make c3 "🐵🙈🙉🙊🍌🎢"
        # fs_story_make c5 "🐶🐱🐭🏫⛈🎾"
        # fs_story_make c6 "🐷🐮🐔🐑🐴🐶"
        # fs_story_make c7 "🐸🐢🐌👨‍💻🕵️‍♂️💎"
        fs_story_make c8 "🐹🐰🐻🐨🐼🐯"
    )
} ; export -f fs_story_make_run


# fs_queue_pass()
# {
#     while read f ; do
#         if test -f "${f}.lock" || test -f "${f}.log" ; then
#             continue
#         fi

#         touch "${f}.lock"

#         (
#             cat $f \
#                 | tee /dev/stderr \
#                 | rq_worker
#         ) 2>&1 \
#             | tee /dev/stderr \
#             | tee -a "${f}.log"

#         rm "${f}.lock"
#     done

# } ; export -f fs_queue_pass



# fs_rq_worker()
# {
#     local filter=$1
#     (
#         source ~/aipif/sd_venv/bin/activate
#         while true ; do
#             find _queue -type f -maxdepth 1 \
#                 | perl -pe's{^(.+-req.xml).*}{$1}g;' \
#                 | sort \
#                 | uniq -u \
#                 | ( egrep -a "$filter" || true ) \
#                 | head -n 1 \
#                 | fs_queue_pass
#             echo -n .
#             sleep 10
#         done
#     ) 2>&1 \
#         | tee _generated/fs_rq_worker.log
# } ; export -f fs_rq_worker


# fs_rq_worker_loop()
# {
#     (
#         clear
#         . ~/aipif/.env
#         . ../common/aws.bash
#         export PYTHONPATH=~/aipif/src
#         fs_rq_worker make_picture
#     )
# } ; export -f fs_rq_worker_loop


s3_queue_pass()
{
    local rq_worker=$1
    while read f ; do

        if s3_exists "_queue/${f}.lock" || s3_exists "_queue/${f}.log" ; then
            continue
        fi

        s3_touch "_queue/${f}.lock"
        # touch "_queue/${f}.lock"

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
        # rm "_queue/${f}.lock"
    done

} ; export -f s3_queue_pass


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


sound_worker_loop()
{
    story_configure stub
    (
        export worker_count=1
        export venv_path=${phome}/bark_venv
        export req_path=${phome}/src/sounds/bark_requirements.txt

        if [[ ! -d ${venv_path} ]] ; then
            (
                cd ${phome}
                python3 -m venv ${venv_path}
                . ${venv_path}/bin/activate
                pip install -r ${req_path}
            )
        fi

        seq $worker_count \
            | xargs -i -P $worker_count \
                bash -c "
                    source ${venv_path}/bin/activate
                    source story2.bash
                    story_configure stub
                    s3_rq_worker SoundRqWorker make_sound
                "
    )
} ; export -f sound_worker_loop


picture_worker_loop()
{
    story_configure stub
    (
        export worker_count=1
        export venv_path=${phome}/sd_venv
        export req_path=${phome}/src/pictures/requirements.txt

        if [[ ! -d ${venv_path} ]] ; then
            (
                cd ${phome}
                python3 -m venv ${venv_path}
                . ${venv_path}/bin/activate
                pip install -r ${req_path}
            )
        fi

        seq $worker_count \
            | xargs -i -P $worker_count \
                bash -c "
                    source ${venv_path}/bin/activate
                    source story2.bash
                    story_configure stub
                    s3_rq_worker PictureRqWorker make_picture
                "
    )
} ; export -f picture_worker_loop


music_worker_loop()
{
    story_configure stub
    (
        export worker_count=1
        export venv_path=${phome}/mus_venv
        export req_path=${phome}/src/music/requirements.txt

        if [[ ! -d ${venv_path} ]] ; then
            (
                cd ${phome}
                python3 -m venv ${venv_path}
                . ${venv_path}/bin/activate
                pip install -r ${req_path}
            )
        fi

        seq $worker_count \
            | xargs -i -P $worker_count \
                bash -c "
                    source ${venv_path}/bin/activate
                    source story2.bash
                    story_configure stub
                    s3_rq_worker MusicRqWorker make_music
                "
    )
} ; export -f music_worker_loop


apt_requirements_install()
{
    story_configure stub
    req_path=${phome}/src/story/apt_requirements.txt
    sudo xargs apt-get install -y < ${req_path}

    (
        mkdir -p ${phome}/exclude || true
        cd ${phome}/exclude
        aws s3 cp s3://aipif-2023/opt/tweego-2.1.1-linux-x64.tgz .
        unzip tweego-2.1.1-linux-x64.tgz
    ) 

} ; export -f apt_requirements_install


story_worker_loop()
{
    story_configure stub
    (
        export worker_count=1
        export venv_path=${phome}/story_venv
        export req_path=${phome}/src/story/requirements.txt

        if [[ ! -d ${venv_path} ]] ; then
            (
                cd ${phome}
                python3 -m venv ${venv_path}
                . ${venv_path}/bin/activate
                pip install -r ${req_path}
            )
        fi

        seq $worker_count \
            | xargs -i -P $worker_count \
                bash -c "
                    source ${venv_path}/bin/activate
                    source story2.bash
                    story_configure stub
                    s3_rq_worker StoryRqWorker make_story
                "
    )
} ; export -f story_worker_loop


queue_worker_loop()
{
    (
        story_configure stub
        source ../common/aws.bash
        
        # TODO watch job queue for issues and take action to fix them

        # aws s3 ls aipif-2023/_queue/ | tr -s " "  | cut -f4 | grep lock | cut -d" " -f4  | while read f ; do aws s3 rm s3://"aipif-2023/_queue/${f}" ; done

        # grep -l OutOfMemoryError  _queue/make_picture-*log | while read f ; do aws s3 rm s3://"aipif-2023/${f}" ; done

        # egrep -l 'Traceback|Errno|error|memory'  _queue/make_* | while read f ; do aws s3 rm s3://aipif-2023/$f ; done

        # aws s3 cp --recursive  s3://aipif-2023/_queue/ queue/
    )
} ; export -f queue_worker_loop

