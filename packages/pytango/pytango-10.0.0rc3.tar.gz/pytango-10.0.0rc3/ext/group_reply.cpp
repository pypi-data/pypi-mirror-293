/******************************************************************************
  This file is part of PyTango (http://pytango.rtfd.io)

  Copyright 2006-2012 CELLS / ALBA Synchrotron, Bellaterra, Spain
  Copyright 2013-2014 European Synchrotron Radiation Facility, Grenoble, France

  Distributed under the terms of the GNU Lesser General Public License,
  either version 3 of the License, or (at your option) any later version.
  See LICENSE.txt for more info.
******************************************************************************/

#include "precompiled_header.hpp"
#include "pytgutils.h"
#include "device_attribute.h"

namespace PyGroupAttrReply
{
bopy::object get_data(Tango::GroupAttrReply &self, PyTango::ExtractAs extract_as)
{
    // Usually we pass a device_proxy to "convert_to_python" in order to
    // get the data_format of the DeviceAttribute for Tango versions
    // older than 7.0. However, GroupAttrReply has no device_proxy to use!
    // So, we are using update_data_format() in:
    //       GroupElement::read_attribute_reply/read_attributes_reply
    return PyDeviceAttribute::convert_to_python(new Tango::DeviceAttribute(self.get_data()), extract_as);
}
} // namespace PyGroupAttrReply

void export_group_reply()
{
    bopy::class_<Tango::GroupReply> GroupReply("GroupReply", "", bopy::no_init);
    GroupReply
        //         .def(init<>())
        //         .def(init<const Tango::GroupReply &>())
        //         .def(init<const std::string, const std::string, bool>()) /// @todo args?
        //         .def(init<const std::string, const std::string, const Tango::DevFailed&, bool>())
        .def("has_failed", &Tango::GroupReply::has_failed)
        .def("group_element_enabled", &Tango::GroupReply::group_element_enabled)
        .def("dev_name", &Tango::GroupReply::dev_name, bopy::return_value_policy<bopy::copy_const_reference>())
        .def("obj_name", &Tango::GroupReply::obj_name, bopy::return_value_policy<bopy::copy_const_reference>())
        .def("get_err_stack",
             &Tango::GroupReply::get_err_stack,
             bopy::return_value_policy<bopy::copy_const_reference>());

    bopy::class_<Tango::GroupCmdReply, bopy::bases<Tango::GroupReply>> GroupCmdReply("GroupCmdReply", bopy::no_init);
    GroupCmdReply.def("get_data_raw", &Tango::GroupCmdReply::get_data, bopy::return_internal_reference<1>());

    bopy::class_<Tango::GroupAttrReply, bopy::bases<Tango::GroupReply>> GroupAttrReply("GroupAttrReply", bopy::no_init);
    GroupAttrReply.def(
        "__get_data", &PyGroupAttrReply::get_data, (arg_("self"), arg_("extract_as") = PyTango::ExtractAsNumpy));
}
