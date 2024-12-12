git fetch
if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ];
then
	date
    echo Merging...
	git merge
    echo Killing server...
    kill -HUP $(cat gunicorn.pid)
fi >> autodeploy.log

