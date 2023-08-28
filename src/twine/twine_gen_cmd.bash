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

# cat story/_sample/tree_016_zzz6_url.xml \
# cat story/_generated/decorated.xml \
#     | xsltproc twine/xslt/prompt_remove.xml /dev/stdin \
#     | xsltproc twine/xslt/sugarcube_twine_generate4.xml /dev/stdin \
#     > twine/_generated/tree_016_zzz6_url.twee

# /opt/tweego-2.1.1-linux-x64/tweego -f sugarcube-2 -o /dev/stdout \
#     twine/_generated/tree_016_zzz6_url.twee \
#     | tee >( aws s3 cp - s3://aipif-2023/sample/twine.html --content-type "text/html" --metadata "Content-Disposition=inline") \
#     > twine/_generated/tree_016_zzz6_url.html

# http://aipif-2023.s3-website-us-west-1.amazonaws.com/sample/twine.html

# http://aipif-2023.s3.amazonaws.com/sample/twine.html

# src/story/_generated/story_c4/p0090-decorated.xml
cat twine/_generated/example_decorated.xml \
    | xsltproc twine/xslt/sugarcube_twine_generate6.xml /dev/stdin \
    > twine/_generated/decorated_tree.twee

/opt/tweego-2.1.1-linux-x64/tweego -f sugarcube-2 -o /dev/stdout \
    twine/_generated/decorated_tree.twee \
    > twine/_generated/decorated_tree.html
    | tee >( aws s3 cp - s3://aipif-2023/sample/twine.html --content-type "text/html" --metadata "Content-Disposition=inline") \