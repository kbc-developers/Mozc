host_dir=$(dirname $(dirname `pwd`))
sudo docker run --interactive -v $host_dir:/home/mozc_builder/work/mozc --tty --rm $USER/mozc_ubuntu14.04

