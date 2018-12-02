export VERSION=3.4.4

wget -c https://github.com/opencv/opencv/archive/${VERSION}/opencv-${VERSION}.tar.gz
tar xf opencv-${VERSION}.tar.gz
cd opencv-${VERSION}/
find ./ -iname "len*.*" -exec rm {} \;
rm -rf modules/xfeatures2d/
cd ..; tar zcf opencv-clean-${VERSION}.tar.gz opencv-${VERSION}/
rm -rf opencv-${VERSION}/

wget -c https://github.com/opencv/opencv_contrib/archive/${VERSION}/opencv_contrib-${VERSION}.tar.gz
tar xf opencv_contrib-${VERSION}.tar.gz
cd opencv_contrib-${VERSION}/
rm -rf modules/xfeatures2d/
cd ..; tar zcf opencv_contrib-clean-${VERSION}.tar.gz opencv_contrib-${VERSION}/
rm -rf opencv_contrib-${VERSION}/
