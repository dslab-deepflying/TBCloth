#! /bin/sh
result=`
mkdir imgs 
## unzip xxx_* will raise a error
unzip tianchi_fm_img3_1.zip
unzip tianchi_fm_img3_2.zip
unzip tianchi_fm_img3_3.zip
unzip tianchi_fm_img3_4.zip
ls tianchi_fm_img2_1 | xargs -t -I {} mv tianchi_fm_img2_1/{} imgs/
ls tianchi_fm_img2_2 | xargs -t -I {} mv tianchi_fm_img2_2/{} imgs/
ls tianchi_fm_img2_3 | xargs -t -I {} mv tianchi_fm_img2_3/{} imgs/
ls tianchi_fm_img2_4 | xargs -t -I {} mv tianchi_fm_img2_4/{} imgs/
`
$result
