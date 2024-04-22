git fetch
if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ];
then
	date
	git merge
	# TODO restart server
fi >> autodeploy.log

