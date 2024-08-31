/******************************************************************************
  This file is part of PyTango (http://pytango.rtfd.io)

  Copyright 2006-2012 CELLS / ALBA Synchrotron, Bellaterra, Spain
  Copyright 2013-2014 European Synchrotron Radiation Facility, Grenoble, France

  Distributed under the terms of the GNU Lesser General Public License,
  either version 3 of the License, or (at your option) any later version.
  See LICENSE.txt for more info.
******************************************************************************/

#include "precompiled_header.hpp"
#include <tango/tango.h>

void export_user_default_fwdattr_prop()
{
    bopy::class_<Tango::UserDefaultFwdAttrProp, boost::noncopyable>("UserDefaultFwdAttrProp")
        .def("set_label", &Tango::UserDefaultFwdAttrProp::set_label);
}

void export_fwdattr()
{
    bopy::class_<Tango::FwdAttr, boost::noncopyable>("FwdAttr", bopy::init<const std::string &, const std::string &>())
        .def("set_default_properties", &Tango::FwdAttr::set_default_properties);
}
