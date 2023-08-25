cat story/_generated/decorated.xml \
    | tr -s " " \
    | fmt -w 60 \
    | xsltproc twine/xslt/gallery_generate.xml /dev/stdin \
    | tee >( aws s3 cp - s3://aipif-2023/sample/gallery.html --content-type text/html ) \
    > twine/_generated/gallery.html

