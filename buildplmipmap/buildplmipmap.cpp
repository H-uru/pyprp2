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

#include <ResManager/plResManager.h>
#include <PRP/plPageInfo.h>
#include <PRP/KeyedObject/plLocation.h>
#include <PRP/Surface/plMipmap.h>
#include <Util/plString.h>
#include <Stream/hsStream.h>

#include <IL/il.h>
#include <IL/ilu.h>
#include <Python.h>

unsigned int getClosestDXTSize(unsigned int size) {
    unsigned int p2 = 1;
    while (p2 < size)
        p2 <<= 1;
    if (size == 0)
        return 1;
    return p2;
}

void build_mipmap(const char* srcimage, const char* outfile, const char* type, unsigned int dxttype) {
    ILuint ImgId;
    ilInit();
    ilGenImages(1, &ImgId);
    ilBindImage(ImgId);
    ilLoadImage(srcimage);
    ILinfo ImageInfo;
    iluGetImageInfo(&ImageInfo);
    iluImageParameter(ILU_FILTER, ILU_BILINEAR);

    unsigned int new_w = getClosestDXTSize(ImageInfo.Width);
    unsigned int new_h = getClosestDXTSize(ImageInfo.Height);
    if (ImageInfo.Width != new_w || ImageInfo.Height != new_h) {
        //printf("Sizing to %i %i\n",new_w,new_h);
        iluScale(new_w, new_h, 1);
    }
    if (plString(type) == "mipmap") {
        plMipmap mip;
        if (dxttype == 1)
            mip.Create(new_w,new_h, 0, plMipmap::kDirectXCompression, plMipmap::kRGB8888,plMipmap::kDXT1);
        else if (dxttype == 5)
            mip.Create(new_w,new_h, 0, plMipmap::kDirectXCompression, plMipmap::kRGB8888,plMipmap::kDXT5);
        unsigned int width;
        unsigned int height;
        unsigned int size;

        for (size_t level=0; level < mip.getNumLevels(); level++) {
            width = mip.getLevelWidth(level);
            height = mip.getLevelHeight(level);
            size = mip.getLevelSize(level);
            unsigned char* ldata = new unsigned char[width*height*4];
            //printf("%i x %i\n",width,height);
            if (level != 0)
                iluScale(width, height, 1);
            ilCopyPixels(0, 0, 0, width, height, 1, IL_RGBA, IL_UNSIGNED_BYTE, ldata);
            mip.CompressImage(level, ldata, size);
        }
        hsFileStream os;
        os.open(outfile,fmWrite);
        mip.writeData(&os);
        os.close();
    }
}

static PyObject* build_m(PyObject* self, PyObject* args) {
    static char* srcimage;
    static char* outfile;
    static char* type;
    unsigned int dxttype;
    if (!PyArg_ParseTuple(args, "sssi", &srcimage, &outfile, &type, &dxttype))
        PyErr_SetString(PyExc_TypeError, "build expects string, string, string, int");
   build_mipmap(srcimage, outfile, type, dxttype);
   return Py_None;
}

static PyMethodDef BuildPlMipmapMethods[] = {
    {"build",  build_m, METH_VARARGS, "Build Mipmap."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef buildplmipmap_module = {
   PyModuleDef_HEAD_INIT,
   "buildplmipmap",
   NULL,
   -1,
   BuildPlMipmapMethods
};

PyMODINIT_FUNC
PyInit_buildplmipmap(void) {
    return PyModule_Create(&buildplmipmap_module);
}
