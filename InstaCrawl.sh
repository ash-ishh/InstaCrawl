name=$(head -n 1 source.txt)
mkdir "${name}"
cp source.txt ./${name}
cd "${name}"
cat source.txt | grep -Pio 'https://.*?\.jpg' | uniq > links.txt
cat links.txt | while read line
do
    wget -nc "${line}"
done

