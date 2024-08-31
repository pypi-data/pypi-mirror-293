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

void export_device_data_history()
{
    bopy::class_<Tango::DeviceDataHistory, bopy::bases<Tango::DeviceData>> DeviceDataHistory("DeviceDataHistory",
                                                                                             bopy::init<>());

    DeviceDataHistory
        .def(bopy::init<const Tango::DeviceDataHistory &>())

        .def("has_failed", &Tango::DeviceDataHistory::has_failed)
        .def("get_date", &Tango::DeviceDataHistory::get_date, bopy::return_internal_reference<>())
        .def("get_err_stack",
             &Tango::DeviceDataHistory::get_err_stack,
             bopy::return_value_policy<bopy::copy_const_reference>());
}
