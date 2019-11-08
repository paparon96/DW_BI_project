/usr/bin/docker login --username 18435 --password Pap8Dok!tor &&
/usr/bin/docker run --name mongotest -t --net host 18435/awesome &&
/usr/bin/docker stop mongotest &&
/usr/bin/docker rm mongotest &&
echo "done"
