cd img
set -x
for color in red blue ; do
	magick montage ${color}-d6.png ${color}-d6.png ${color}-d6.png ${color}-d6.png ${color}-d6.png ${color}-d6.png -background none -tile 3x2 -geometry +0+0 6-${color}-d6.png
	magick -size 357x250 xc:none     ${color}-d6.png -geometry +0+0 -composite     ${color}-d6.png -geometry +119+62 -composite     ${color}-d6.png -geometry +238+0 -composite     ${color}-d6.png -geometry +0+125 -composite     ${color}-d6.png -geometry +238+120 -composite     5-${color}-d6.png
	magick -size 357x250 xc:none     ${color}-d6.png -geometry +60+0 -composite     ${color}-d6.png -geometry +178+0 -composite     ${color}-d6.png -geometry +60+125 -composite     ${color}-d6.png -geometry +178+120 -composite     4-${color}-d6.png
	magick -size 357x250 xc:none     ${color}-d6.png -geometry +0+0 -composite     ${color}-d6.png -geometry +119+62 -composite     ${color}-d6.png -geometry +238+120 -composite     3-${color}-d6.png
	magick -size 357x250 xc:none     ${color}-d6.png -geometry +178+0 -composite     ${color}-d6.png -geometry +60+125 -composite     2-${color}-d6.png
	magick -size 357x250 xc:none     ${color}-d6.png -geometry +119+62 -composite    1-${color}-d6.png
done
