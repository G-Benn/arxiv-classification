#!/bin/sh
echo "Running (test) detex script"
# unTar all files into their .gz forms, then remove the .tar file
for file in *.tar; do tar xvf "${file}" && rm "${file}"; done
# Move files up one level
mv */* . && rmdir *

# Remove all .pdf from resulting subdirectories because we can't parse them
rm *.pdf

# Do the parsing
for f in *.gz; do
	echo $f
	echo "${f%.*}"
	tar xvzf $f
	TEXFILE=$(find . -type f \( -iname \*.tex \))
	echo $TEXFILE
	./delatex.run -n "${TEXFILE}" > "${f%.*}.txt"
	find . -type f \( ! \( -iname \*.txt -o -iname \*.sh -o -iname \*.gz -o -iname \*.run \) \) -delete

	#find . -type f \( ! (-iname "*.txt" -o -iname "*.sh" -o -iname "*.gz") \) #-delete #only use delete once it works - removes all except txt file, script, and gz files
	#exit 1 # Just for testing to make sure it works
done
rm *.gz #delete gz files/folders
find . -empty -type d -delete # remove empty directories
find . ! \( -iname '????.*.txt' -o -iname '.' -o -iname '*.sh' -o -iname '*.run' \) -delete # get rid of everything that isn't an arxiv-conventional txt file
