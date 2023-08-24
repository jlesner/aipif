# xsltproc xslt/act_part_remove.xml story_input.xml | xsltproc xslt/chapbook_twine_generate.xml /dev/stdin > test.twee
# /opt/tweego-2.1.1-linux-x64/tweego -f chapbook-1  -o test.html test.twee

# /opt/tweego-2.1.1-linux-x64/tweego -o index.html src

# xsltproc xslt/act_part_remove.xml story_input.xml | xsltproc xslt/sugarcube_twine_generate.xml /dev/stdin > test.twee
# /opt/tweego-2.1.1-linux-x64/tweego -f sugarcube-2  -o test.html test.twee

# cat sample_story_tree.xml \
#     | xsltproc twine/xslt/prompt_remove.xml /dev/stdin \
#     | xsltproc twine/xslt/sugarcube_twine_generate2.xml /dev/stdin \
#     > _generated/pengu_alien.twee

# /opt/tweego-2.1.1-linux-x64/tweego -f sugarcube-2 \
#     -o _generated/pengu_alien.html \
#     _generated/pengu_alien.twee

cat story/_sample/tree_016_zzz6_url.xml \
    | xsltproc twine/xslt/prompt_remove.xml /dev/stdin \
    | xsltproc twine/xslt/sugarcube_twine_generate3.xml /dev/stdin \
    > twine/_generated/tree_016_zzz6_url.twee

/opt/tweego-2.1.1-linux-x64/tweego -f sugarcube-2 \
    -o twine/_generated/tree_016_zzz6_url.html \
    twine/_generated/tree_016_zzz6_url.twee