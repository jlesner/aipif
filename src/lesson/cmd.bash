( 
    export PYTHONPATH=src ;
    cat src/lesson/books.txt  \
        | while read book ; do \
            echo "Please summarize all the individual lessons that are in '$book'. Output them one per line nested using XML tag <lesson>. Do not number them or given any other output." \
            | python src/text/Gpt4oMiniTextMaker.py \
            > src/lesson/_generated/"$book".lesson  
        ; echo $book  ; 
    done 
)

cat src/lesson/books.txt  \
    | while read book ; do \
        [[ -f src/lesson/_generated/"$book".lesson ]] || echo $book
    done

