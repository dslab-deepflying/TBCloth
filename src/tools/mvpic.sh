#! /bin/sh

result = 'ls tianchi_fm_img2_* | xargs -t -I {} mv {} imgs/{}'
echo result=$result