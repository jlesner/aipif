cat story/_generated/decorated.xml \
    | tr -s " " \
    | fmt -w 60 \
    | xsltproc twine/xslt/pgallery_generate.xml /dev/stdin \
    | tee >( aws s3 cp - s3://aipif-2023/sample/gallery.html --content-type text/html ) \
    > twine/_generated/pgallery.html

cat story/_generated/decorated.xml \
    | tr -s " " \
    | fmt -w 60 \
    | xsltproc twine/xslt/mgallery_generate.xml /dev/stdin \
    | tee >( aws s3 cp - s3://aipif-2023/sample/gallery.html --content-type text/html ) \
    > twine/_generated/mgallery.html

cat story/_generated/decorated.xml \
    | tr -s " " \
    | fmt -w 60 \
    | xsltproc twine/xslt/sgallery_generate.xml /dev/stdin \
    | tee >( aws s3 cp - s3://aipif-2023/sample/gallery.html --content-type text/html ) \
    > twine/_generated/sgallery.html


# cat twine/_generated/example_decorated.xml \
#     | tr -s " " \
#     | fmt -w 60 \
#     | xsltproc twine/xslt/pgallery_generate.xml /dev/stdin \
#     > twine/_generated/gallery3.html
