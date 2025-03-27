git fetch
if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ];
then
	date
    echo Merging...
	git merge
    echo Killing backend server...
    kill -HUP $(cat backend/gunicorn.pid)
    #echo Killing frontend server...
    #kill -HUP $(cat frontend/gunicorn.pid)
fi >> autodeploy.log

