/******************************************************************************
  This file is part of PyTango (http://pytango.rtfd.io)

  Copyright 2006-2012 CELLS / ALBA Synchrotron, Bellaterra, Spain
  Copyright 2013-2014 European Synchrotron Radiation Facility, Grenoble, France

  Distributed under the terms of the GNU Lesser General Public License,
  either version 3 of the License, or (at your option) any later version.
  See LICENSE.txt for more info.
******************************************************************************/

#include "tango_numpy.h"

PyArrayObject *to_PyArrayObject(PyObject *obj)
{
    if(PyArray_Check(obj))
    {
        return (PyArrayObject *) (obj);
    }
    else
    {
        throw std::runtime_error("PyObject is not a numpy array");
    }
}
