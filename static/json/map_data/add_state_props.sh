find *.json | xargs -i topojson -o {} -p name=STATENAM -- {}
find *.json | xargs -i topojson -o {} -e states.csv --id-property=name -p abbrev=abbreviation -p -- {}

state=&lccn=&dateFilterType=yearRange&date1=1847&date2=1847&language=&ortext=&andtext=&phrasetext=&proxtext=taft&rows=20&searchType=advanced&sort=state&format=json
&date1=1847&sort=state&rows=20&sequence=0&format=json&date2=1847&dateFilterType=yearRange&page=1&protext=taft
&date1=1847&sort=state&rows=20&format=json&date2=1847&dateFilterType=yearRange&protext=taft
&proxtext=taft&date1=1847&date2=1847&dateFilterType=yearRange&rows=20&sort=state&format=json