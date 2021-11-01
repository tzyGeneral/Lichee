from image_registration import match_template, ORB, SIFT
from baseImage import IMAGE, Rect

orb = ORB()
sift = SIFT()

im_source = IMAGE('./image/test.png')
im_search = IMAGE('./image/start.png')

# tpl = match_template()

result = orb.find_all(im_source=im_source, im_search=im_search)
print(result)
