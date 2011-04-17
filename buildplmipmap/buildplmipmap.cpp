/* This file is part of PyPRP2.
 *
 * Copyright (C) 2010 PyPRP2 Project Team
 * See the file AUTHORS for more info about the team.
 *
 * PyPRP2 is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * PyPRP2 is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with PyPRP2.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "ResManager/plResManager.h"
#include "PRP/plPageInfo.h"
#include "PRP/KeyedObject/plLocation.h"
#include "PRP/Surface/plMipmap.h"
#include "Util/plString.h"
#include "Stream/hsStream.h"
#include "3rdPartyLibs/squish/squish.h"

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
            mip.Create(new_w,new_h,plMipmap::kRGB32Config,0,plMipmap::kDirectXCompression,plMipmap::kDXT1);
        else if (plString(argv[4]) == "DXT5")
            mipCreate(new_w,new_h,plMipmap::kARGB32Config,0,plMipmap::kDirectXCompression,plMipmap::kDXT5);
        printf("Mipmapping %i levels... this could take a very long time\n",mip.getNumLevels());
        unsigned int width;
        unsigned int height;

        for (size_t level=0; level < mip.getNumLevels(); level++) {
            width = mip.getLevelWidth(level);
            height = mip.getLevelHeight(level);
            unsigned char* ldata = new unsigned char[width*height*4];
            printf("%i x %i\n",width,height);
            if (level != 0)
                iluScale(width, height, 1);
            ilCopyPixels(0, 0, 0, width, height, 1, IL_RGBA, IL_UNSIGNED_BYTE, ldata);
            unsigned char* temp_compressed_data = new unsigned char[mip.getLevelSize(level)];

            if (mip.getDXCompression() == plMipmap::kDXT1)
                squish::CompressImage(ldata, width, height, temp_compressed_data, squish::kDxt1 | squish::kColourRangeFit);
            else if (mip.getDXCompression() == plMipmap::kDXT5)
                squish::CompressImage(ldata, width, height, temp_compressed_data, squish::kDxt5 | squish::kColourRangeFit);
            mip.setLevelData(level,temp_compressed_data);
            delete[] temp_compressed_data;
            delete[] ldata;
        }
        hsFileStream os;
        os.open(argv[2],FileMode::fmWrite);
        mip.writeData(&os);
        os.close();
    }
    return 0;
}
