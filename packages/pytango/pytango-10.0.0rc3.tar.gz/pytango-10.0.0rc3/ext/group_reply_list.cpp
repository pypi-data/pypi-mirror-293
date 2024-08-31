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

void export_group_reply_list()
{
    typedef std::vector<Tango::GroupReply> StdGroupReplyVector_;
    typedef std::vector<Tango::GroupCmdReply> StdGroupCmdReplyVector_;
    typedef std::vector<Tango::GroupAttrReply> StdGroupAttrReplyVector_;

    bopy::class_<Tango::GroupReplyList, bopy::bases<StdGroupReplyVector_>> GroupReplyList("GroupReplyList",
                                                                                          bopy::init<>());
    GroupReplyList.def("has_failed", &Tango::GroupReplyList::has_failed)
        .def("reset", &Tango::GroupReplyList::reset)
        .def("push_back", &Tango::GroupReplyList::push_back);

    bopy::class_<Tango::GroupCmdReplyList, bopy::bases<StdGroupCmdReplyVector_>> GroupCmdReplyList("GroupCmdReplyList",
                                                                                                   bopy::init<>());
    GroupCmdReplyList.def("has_failed", &Tango::GroupCmdReplyList::has_failed)
        .def("reset", &Tango::GroupCmdReplyList::reset)
        .def("push_back", &Tango::GroupCmdReplyList::push_back);

    bopy::class_<Tango::GroupAttrReplyList, bopy::bases<StdGroupAttrReplyVector_>> GroupAttrReplyList(
        "GroupAttrReplyList", bopy::init<>());
    GroupAttrReplyList.def("has_failed", &Tango::GroupAttrReplyList::has_failed)
        .def("reset", &Tango::GroupAttrReplyList::reset)
        .def("push_back", &Tango::GroupAttrReplyList::push_back);
}
