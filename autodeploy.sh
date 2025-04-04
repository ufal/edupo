git fetch
if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ];
then
	date
    echo Merging...
	git merge
    echo Reloading backend...
    ./reload.sh
fi >> autodeploy.log

