/usr/bin/docker run --name mongotest -t --net host 18435/awesome &&
/usr/bin/docker stop mongotest &&
/usr/bin/docker rm mongotest &&
echo "done"
