
aws_config()
{
    # aws configure
    export s3_bucket=aipif-2023
} ; export -f aws_config


s3_touch()
{
    local fs_path=$1
    aws s3api put-object --bucket ${s3_bucket} --key $fs_path --content-length 0
} ; export -f s3_touch


s3_txt_stream()
{
    local fs_path=$1
    aws s3 cp - s3://${s3_bucket}/${fs_path} \
        --content-type text/plain
        # --content-type application/xml \
        # --metadata "Content-Disposition=inline"
} ; export -f s3_txt_stream


s3_get()
{
    local fs_path=$1
    aws s3 cp s3://${s3_bucket}/${fs_path} -
} ; export -f s3_get


s3_put()
{
    local fs_path=$1
    local content_type=$2
    aws s3 cp - s3://${s3_bucket}/${fs_path} \
        --content-type ${content_type} \
        --metadata "Content-Disposition=inline"
} ; export -f s3_put


s3_rm()
{
    local fs_path=$1
    aws s3 rm s3://${s3_bucket}/$fs_path
} ; export -f s3_rm


s3_ls()
{
    # empty arg for root
    # / on the end any folder
    local fs_path=$1
    aws s3 ls s3://${s3_bucket}/$fs_path
} ; export -f s3_ls


s3_file_ls()
{
    # empty arg for root
    # / on the end any folder
    local fs_path=$1
    aws s3 ls s3://${s3_bucket}/$fs_path \
        | egrep -v ' PRE ' \
        | tr -s " " \
        | cut -d" " -f4
} ; export -f s3_file_ls


s3_exists()
{
    local fs_path=$1
    aws s3 ls s3://${s3_bucket}/$fs_path > /dev/null
} ; export -f s3_exists


s3_content_type()
{
    local fs_path=$1
    local content_type=$2
    aws s3 cp s3://${s3_bucket}/${fs_path} s3://${s3_bucket}/${fs_path} \
        --content-type ${content_type} \
        --metadata "Content-Disposition=inline"
} ; export -f s3_content_type


content_type_cat()
{
    cat <<'EOF'
text/plain
text/html
text/xml
application/xml
application/json
image/jpeg
image/png
audio/mpeg
audio/wav
audio/ogg
EOF
} ; export -f content_type_cat

