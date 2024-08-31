/******************************************************************************
  This file is part of PyTango (http://pytango.rtfd.io)

  Copyright 2006-2012 CELLS / ALBA Synchrotron, Bellaterra, Spain
  Copyright 2013-2014 European Synchrotron Radiation Facility, Grenoble, France

  Distributed under the terms of the GNU Lesser General Public License,
  either version 3 of the License, or (at your option) any later version.
  See LICENSE.txt for more info.
******************************************************************************/

#ifndef _ATTRIBUTE_H_
#define _ATTRIBUTE_H_

#include <boost/python.hpp>
#include <tango/tango.h>

namespace PyAttribute
{
void set_value(Tango::Attribute &, bopy::object &);

void set_value(Tango::Attribute &, bopy::str &, bopy::str &);

void set_value(Tango::Attribute &, bopy::str &, bopy::object &);

void set_value(Tango::Attribute &, bopy::object &, long);

void set_value(Tango::Attribute &, bopy::object &, long, long);

void set_value_date_quality(Tango::Attribute &, bopy::object &, double, Tango::AttrQuality);

void set_value_date_quality(Tango::Attribute &, bopy::str &, bopy::str &, double, Tango::AttrQuality);

void set_value_date_quality(Tango::Attribute &, bopy::str &, bopy::object &, double, Tango::AttrQuality);

void set_value_date_quality(Tango::Attribute &, bopy::object &, double, Tango::AttrQuality, long);

void set_value_date_quality(Tango::Attribute &, bopy::object &, double, Tango::AttrQuality, long, long);

bopy::object get_properties(Tango::Attribute &, bopy::object &);

bopy::object get_properties_2(Tango::Attribute &, bopy::object &);

bopy::object get_properties_3(Tango::Attribute &, bopy::object &);

bopy::object get_properties_multi_attr_prop(Tango::Attribute &, bopy::object &);

void set_properties(Tango::Attribute &, bopy::object &, bopy::object &);

void set_properties_3(Tango::Attribute &, bopy::object &, bopy::object &);

void set_properties_multi_attr_prop(Tango::Attribute &, bopy::object &);
}; // namespace PyAttribute

#endif // _ATTRIBUTE_H_
