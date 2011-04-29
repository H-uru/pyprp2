#include <ResManager/plResManager.h>
#include <PRP/plPageInfo.h>
#include <PRP/KeyedObject/plLocation.h>
#include <PRP/Surface/plMipmap.h>
#include <Util/plString.h>
#include <Stream/hsStream.h>
#include "squish.h"

#include <IL/il.h>
#include <IL/ilu.h>

unsigned int getClosestDXTSize(unsigned int size) {
    unsigned int p2 = 1;
    while (p2 < size)
        p2 <<= 1;
    if (size == 0)
        return 1;
    return p2;
}

int main(int argc, char **argv) {
    if (argc != 5) {
        printf("Usage: buildplmipmap [srcimage] [outfile] [type] [dxttype]");
        return 0;
    }
    ILuint ImgId;
    ilInit();
    ilGenImages(1, &ImgId);
    ilBindImage(ImgId);
    ilLoadImage(argv[1]);
    ILinfo ImageInfo;
    iluGetImageInfo(&ImageInfo);
    iluImageParameter(ILU_FILTER, ILU_BILINEAR);

    unsigned int new_w = getClosestDXTSize(ImageInfo.Width);
    unsigned int new_h = getClosestDXTSize(ImageInfo.Height);
    if (ImageInfo.Width != new_w || ImageInfo.Height != new_h) {
        printf("Sizing to %i %i\n",new_w,new_h);
        iluScale(new_w, new_h, 1);
    }
    if (plString(argv[3]) == "mipmap") {
        plMipmap mip;
        if (plString(argv[4]) == "DXT1")
            mip.Create(new_w,new_h, 0, plMipmap::kDirectXCompression, plMipmap::kRGB8888,plMipmap::kDXT1);
        else if (plString(argv[4]) == "DXT5")
            mip.Create(new_w,new_h, 0, plMipmap::kDirectXCompression, plMipmap::kRGB8888,plMipmap::kDXT5);
        unsigned int width;
        unsigned int height;
        unsigned int size;

        for (size_t level=0; level < mip.getNumLevels(); level++) {
            width = mip.getLevelWidth(level);
            height = mip.getLevelHeight(level);
            size = mip.getLevelSize(level);
            unsigned char* ldata = new unsigned char[width*height*4];
            printf("%i x %i\n",width,height);
            if (level != 0)
                iluScale(width, height, 1);
            ilCopyPixels(0, 0, 0, width, height, 1, IL_RGBA, IL_UNSIGNED_BYTE, ldata);

            unsigned char* temp_compressed_data = new unsigned char[size];

            if (mip.getDXCompression() == plMipmap::kDXT1)
                squish::CompressImage(ldata, width, height, temp_compressed_data, squish::kDxt1 | squish::kColourRangeFit);
            else if (mip.getDXCompression() == plMipmap::kDXT5)
                squish::CompressImage(ldata, width, height, temp_compressed_data, squish::kDxt5 | squish::kColourRangeFit);
            mip.setLevelData(level,temp_compressed_data, size);
            delete[] temp_compressed_data;
            delete[] ldata;
        }
        hsFileStream os;
        os.open(argv[2],fmWrite);
        mip.writeData(&os);
        os.close();
    }
    return 0;
}