#include "ResManager/plResManager.h"
#include "PRP/plPageInfo.h"
#include "PRP/KeyedObject/plLocation.h"
#include "PRP/Surface/plMipmap.h"
#include "Util/plString.h"
#include "3rdPartyLibs/squish/squish.h"

#include <math.h>

#include <IL/il.h>
#include <IL/ilu.h>


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
    unsigned int pw = (unsigned int)log((float)ImageInfo.Width)/log(2.0f);
    unsigned int ph = (unsigned int)log((float)ImageInfo.Height)/log(2.0f);
    printf("%i, %i\n",pw,ph);
    unsigned int new_w = (unsigned int)pow(2, (float)pw);
    unsigned int new_h = (unsigned int)pow(2, (float)ph);
    printf("Sizing to %i %i\n",new_w,new_h);
    iluScale(new_w, new_h, 1);
    if (plString(argv[3]) == "mipmap") {
        plMipmap* mip = new plMipmap;
        if (plString(argv[4]) == "DXT1")
            mip->Create(new_w,new_h,plMipmap::kRGB32Config,0,plMipmap::kDirectXCompression,plMipmap::kDXT1);
        else if (plString(argv[4]) == "DXT5")
            mip->Create(new_w,new_h,plMipmap::kARGB32Config,0,plMipmap::kDirectXCompression,plMipmap::kDXT5);
        printf("Mipmapping %i levels...\n",mip->getNumLevels());
        unsigned int width;
        unsigned int height;

        for (size_t level=0; level < mip->getNumLevels(); level++) {
            width = mip->getLevelWidth(level);
            height = mip->getLevelHeight(level);
            unsigned char* ldata = new unsigned char[width*height*4];
            printf("%i x %i\n",width,height);
            if (level != 0)
                iluScale(width, height, 1);
            ilCopyPixels(0, 0, 0, width, height, 1, IL_RGBA, IL_UNSIGNED_BYTE, ldata);
            unsigned char* temp_compressed_data = new unsigned char[mip->getLevelSize(level)];

            if (mip->getDXCompression() == plMipmap::kDXT1)
                squish::CompressImage(ldata, width, height, temp_compressed_data, squish::kDxt1);
            else if (mip->getDXCompression() == plMipmap::kDXT5)
                squish::CompressImage(ldata, width, height, temp_compressed_data, squish::kDxt5);
            mip->setLevelData(level,temp_compressed_data);
            delete[] temp_compressed_data;
            delete[] ldata;
	    }
        hsFileStream* os = new hsFileStream;
        os->open(argv[2],FileMode::fmWrite);
        mip->writeData(os);
        os->close();
    }
    return 0;
}
