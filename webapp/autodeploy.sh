git fetch
if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ];
then
	date
    echo Merging...
	git merge
    echo Killing server...
    curl http://127.0.0.1:5000/tajnejkill
fi >> autodeploy.log

