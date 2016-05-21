# -*- coding: utf-8 -*-
"""
    https://tools.ietf.org/html/draft-sweet-rfc2910bis-07
    Internet Printing Protocol/1.1: Encoding and Transport

    3.1.1.  Request and Response

       An operation request or response is encoded as follows:

       -----------------------------------------------
       |                  version-number             |   2 bytes  - required
       -----------------------------------------------
       |               operation-id (request)        |
       |                      or                     |   2 bytes  - required
       |               status-code (response)        |
       -----------------------------------------------
       |                   request-id                |   4 bytes  - required
       -----------------------------------------------
       |                 attribute-group             |   n bytes - 0 or more
       -----------------------------------------------
       |              end-of-attributes-tag          |   1 byte   - required
       -----------------------------------------------
       |                     data                    |   q bytes  - optional
       -----------------------------------------------

"""
from __future__ import division, print_function
import sys
import os
import csv
from datetime import datetime
from pprint import pprint


IPP_BUF_SIZE = 32767

IPP_TAG_ZERO = 0x00             # Zero tag - used for separators
IPP_TAG_OPERATION = 1           # Operation group
IPP_TAG_JOB = 2                 # Job group
IPP_TAG_END = 3                 # End-of-attributes
IPP_TAG_PRINTER = 4             # Printer group
IPP_TAG_UNSUPPORTED_GROUP = 5   # Unsupported attributes group
IPP_TAG_SUBSCRIPTION = 6        # Subscription group
IPP_TAG_EVENT_NOTIFICATION = 7  # Event group
IPP_TAG_RESOURCE = 8            # Resource group @private@
IPP_TAG_DOCUMENT = 9            # Document group

GROUP_TAGS = set(range(IPP_TAG_OPERATION, IPP_TAG_DOCUMENT + 1))

IPP_TAG_UNSUPPORTED_VALUE = 0x10  # Unsupported value
IPP_TAG_DEFAULT = 0x11          # Default value
IPP_TAG_UNKNOWN = 0x12          # Unknown value
IPP_TAG_NOVALUE = 0x13          # No-value value

IPP_TAG_NOTSETTABLE = 0x15       # Not-settable value
IPP_TAG_DELETEATTR = 0x16           # Delete-attribute value
IPP_TAG_ADMINDEFINE = 0x17          # Admin-defined value

IPP_TAG_INTEGER = 0x21       # Integer value
IPP_TAG_BOOLEAN = 0x22          # Boolean value
IPP_TAG_ENUM = 0x23             # Enumeration value

IPP_TAG_STRING = 0x30        # Octet string value
IPP_TAG_DATE = 0x31             # Date/time value
IPP_TAG_RESOLUTION = 0x32           # Resolution value
IPP_TAG_RANGE = 0x33            # Range value
IPP_TAG_BEGIN_COLLECTION = 0x34     # Beginning of collection value
IPP_TAG_TEXTLANG = 0x35         # Text-with-language value
IPP_TAG_NAMELANG = 0x36         # Name-with-language value
IPP_TAG_END_COLLECTION = 0x37       # End of collection value

IPP_TAG_TEXT = 0x41          # Text value
IPP_TAG_NAME = 0x42             # Name value
IPP_TAG_RESERVED_STRING = 0x43      # Reserved for future string value @private@
IPP_TAG_KEYWORD = 0x44          # Keyword value
IPP_TAG_URI = 0x45             # URI value
IPP_TAG_URISCHEME = 0x46            # URI scheme value
IPP_TAG_CHARSET = 0x47          # Character set value
IPP_TAG_LANGUAGE = 0x48        # Language value
IPP_TAG_MIMETYPE = 0x49         # MIME media type value
IPP_TAG_MEMBERNAME = 0x4A           # Collection member name value

IPP_TAG_EXTENSION = 0x7f     # Extension point for 32-bit tags
IPP_TAG_CUPS_MASK = 0x7fffffff,   # Mask for copied attribute values @private@
# The following expression is used to avoid compiler warnings with +/-0x80000000
IPP_TAG_CUPS_CONST = -0x7fffffff - 1    # Bitflag for copied/const attribute values @private@

TAG_DICT = {k: v for k, v in globals().items() if k.startswith('IPP_TAG_')}
assert len(TAG_DICT.values()) == len(set(TAG_DICT.values()))
TAG_NAME = {v: k for k, v in TAG_DICT.items()}


DEBUG = False


def dprint(msg):
    if DEBUG:
        print(msg)

def recursive_glob(path):
    """Generator that returns all files in directory `path` if path is a directory, or path itself
        if path is not a directory.
    """
    if not os.path.isdir(path):
        yield path
    else:
        for root, _, files in os.walk(path):
            for filename in files:
                if not filename.startswith('.'):
                    yield(os.path.join(root, filename))


def T(text):
    return ''.join(chr(x) for x in text)


def H(text, n=None):
    if n is not None:
        text = text[:n]
    return ','.join(['%02x' % x for x in text])


def R(obj):
    if isinstance(obj, tuple):
        return list(obj)
    return obj


def be2(text):
    return text[0] << 8 | text[1]


def be4(text):
    return (((((text[0] << 8) | text[1]) << 8) | text[2]) << 8) | text[3]


class IPP:

    def __init__(ipp, text):
        ipp.text = text
        ipp.i = 0
        ipp.attrs = []

    def __repr__(self):
        return 'IPP{len=%d,i=%d}' % (len(self.text), self.i)

    def read(ipp, n):
        assert 0 <= ipp.i, (n, ipp.i, len(ipp.text))
        assert n > 0
        # print('!!@ read %d %4d %2d %s' % (len(ipp.text), ipp.i, n, H(ipp.text[ipp.i:], min(n, 20))))
        assert ipp.i + n <= len(ipp.text)
        assert ipp.i < len(ipp.text)
        if ipp.i + n >= len(ipp.text):
            dprint('Done reading IPP')
            return None
        bytes = ipp.text[ipp.i:ipp.i + n]
        ipp.i += n
        return bytes

    def read_tag(ipp):
        # print('!!!')
        bytes = ipp.read(1)
        if bytes is None:
            return None
        assert bytes
        # print('@@@', type(bytes), len(bytes))
        # We don't see end-of-attributes tags in CUPS control files
        assert bytes[0] != IPP_TAG_END
        return bytes[0]


def decode_datetime(value):
    """https://tools.ietf.org/html/rfc1903
        DateAndTime ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "2d-1d-1d,1d:1d:1d.1d,1a1d:1d"
        STATUS       current
        DESCRIPTION
                "A date-time specification.

                field  octets  contents                  range
                -----  ------  --------                  -----
                  1      1-2   year                      0..65536
                  2       3    month                     1..12
                  3       4    day                       1..31
                  4       5    hour                      0..23
                  5       6    minutes                   0..59
                  6       7    seconds                   0..60
                               (use 60 for leap-second)
                  7       8    deci-seconds              0..9
                  8       9    direction from UTC        '+' / '-'
                  9      10    hours from UTC            0..11
    """
    year = be2(value[:2])
    month = value[2]
    day = value[3]
    hour = value[4]
    minute = value[5]
    second = value[6]

    return str(datetime(year, month, day, hour, minute, second))


def decode_value(tag, value):
    """
        3.5.2 Value Tags

        The remaining tables show values for the "value-tag" field, which is
        the first octet of an attribute. The "value-tag" field specifies the
        type of the value of the attribute.

        The following table specifies the "out-of-band" values for the "value-tag" field.

        Tag Value (Hex)  Meaning

        0x10             unsupported
        0x11             reserved for 'default' for definition in a future IETF standards
        0x12             unknown
        0x13             no-value
        0x14-0x1F        reserved for "out-of-band" values in future IETF standards

        The following table specifies the integer values for the "value-tag" field:

        Tag Value (Hex)   Meaning

        0x20              reserved for definition in a future IETF
                         standards track document
        0x21              integer
        0x22              boolean
        0x23              enum
        0x24-0x2F         reserved for integer types for definition in
                         future IETF standards track documents

        NOTE: 0x20 is reserved for "generic integer" if it should ever be  needed.

        The following table specifies the octetString values for the "value- tag" field:

        Tag Value (Hex)   Meaning

        0x30              octetString with an  unspecified format
        0x31              dateTime
        0x32              resolution
        0x33              rangeOfInteger
        0x34              reserved for definition in a future IETF standards track document
        0x35              textWithLanguage
        0x36              nameWithLanguage
        0x37-0x3F         reserved for octetString type definitions in future IETF standards

        The following table specifies the character-string values for the "value-tag" field:

        Tag Value (Hex)   Meaning

        0x40              reserved for definition in a future IETF standards track document
        0x41              textWithoutLanguage
        0x42              nameWithoutLanguage
        0x43              reserved for definition in a future IETF standards track document
        0x44              keyword
        0x45              uri
        0x46              uriScheme
        0x47              charset
        0x48              naturalLanguage
        0x49              mimeMediaType
        0x4A-0x5F         reserved for character string type definitions in future IETF standards

        NOTE: 0x40 is reserved for "generic character-string" if it should ever be needed.
    """
    n = len(value)

    if tag in (IPP_TAG_INTEGER, IPP_TAG_ENUM):
        assert n == 4, (tag, n)
        return be4(value)

    elif tag == IPP_TAG_BOOLEAN:
        assert n == 1, (tag, n)
        return bool(value)

    elif tag in (IPP_TAG_NOVALUE,
                 IPP_TAG_NOTSETTABLE,
                 IPP_TAG_DELETEATTR,
                 IPP_TAG_ADMINDEFINE):
        assert False

        # These value types are not supposed to have values, however
        # some vendors (Brother) do not implement IPP correctly and so
        # we need to map non-empty values to text...

        if value.tag == tag:
            if n == 0:
                return
            # !@#$ has no effect
            attr.value_tag = IPP_TAG_TEXT

    if tag in (IPP_TAG_TEXT,
               IPP_TAG_NAME,
               IPP_TAG_KEYWORD,
               IPP_TAG_URI,
               IPP_TAG_URISCHEME,
               IPP_TAG_CHARSET,
               IPP_TAG_LANGUAGE,
               IPP_TAG_MIMETYPE):
        return T(value)

    elif tag == IPP_TAG_DATE:
        assert n == 11, (tag, n)
        return decode_datetime(value)

    elif tag == IPP_TAG_RESOLUTION:
        assert n == 9, (tag, n)
        xres = be4(value[:4])
        yres = be4(value[4:8])
        units = value[8]
        return xres, yres, units

    elif tag == IPP_TAG_RANGE:
        assert n == 8, (tag, n)
        lower = be4(value[:4])
        upper = be4(value[4:])
        return lower, upper

    elif tag in (IPP_TAG_TEXTLANG,
                 IPP_TAG_NAMELANG):
        assert n >= 4, (tag, n)

        buf = ipp.read(n)
        s = buf

        # text-with-language and name-with-language are composite values:
        #     language-length
        #     language
        #     text-length
        #     text

        n = be2[s]
        value['string.language'] = s[2:2 + n]

        s = buf[2 + n:]
        n = be2(s)
        value['string.text'] = s[2:2 + n]

    elif tag == IPP_TAG_BEGIN_COLLECTION:
        # Oh, boy, here comes a collection value, so read it...

        value['collection'] = None
        assert n == 0, (tag, n)

    elif tag == IPP_TAG_END_COLLECTION:

        return state == IPP_STATE_DATA

    elif tag == IPP_TAG_MEMBERNAME:
        # The value the name of the member in the collection, which
        # we need to carry over...
        assert attr, (tag, n)
        assert n, (tag, n)

        attr['name'] = text[:n]
        attr['num_values'] -= 1

    else:  # Other unsupported values
        pass

    return value


def parse_attr_1val(ipp):
    """Parse an attribute with one value

        https://tools.ietf.org/html/draft-sweet-rfc2910bis-07
        Internet Printing Protocol/1.1: Encoding and Transport

        3.1.4 Picture of the Encoding of an Attribute-with-one-value

        Each "attribute-with-one-value" field is encoded as follows:

        -----------------------------------------------
        |                   value-tag                 |   1 byte
        -----------------------------------------------
        |               name-length  (value is u)     |   2 bytes
        -----------------------------------------------
        |                     name                    |   u bytes
        -----------------------------------------------
        |              value-length  (value is v)     |   2 bytes
        -----------------------------------------------
        |                     value                   |   v bytes
        -----------------------------------------------
    """
    attributes = []
    while True:
        tag = ipp.read_tag()
        if tag is None or tag in GROUP_TAGS:
            return tag, attributes
        n = be2(ipp.read(2))
        name = None if n == 0 else ipp.read(n)
        v = be2(ipp.read(2))
        value = None if v == 0 else ipp.read(v)
        tag_s = TAG_NAME.get(tag, 'UNKNOWN')
        name_s = value_s = None
        dprint('\t\ttag=0x%02x %s n=%d,v=%d' % (tag, tag_s, n, v))
        if name is not None:
            name_s = T(name)
            dprint('\t\t    name="%s"' % name_s)
        if value is not None:
            value_s = decode_value(tag, value)
            try:
                dprint('\t\t    value=%r' % R(value_s))
            except Exception as e:
                print('^' * 80)
                print(type(value_s), len(value_s), str(value_s), value_s)
                print('e="%s"' % e)
                raise
        # assert (tag == IPP_TAG_NOVALUE) == (v == 0), (tag_s, name_s, value_s)
        attributes.append((tag_s, name_s, value_s))


def combine_attribute_values(attributes):
    combined_attributes = []
    values_c = []
    for i, (tag_s, name_s, value_s) in enumerate(attributes):
        if name_s is not None:
            if values_c:
                combined_attributes.append((tag_c, name_c, values_c))
            tag_c = tag_s
            name_c = name_s
            values_c = [value_s]
        else:
            # assert False, (i, tag_s, name_s, value_s, values_c)
            values_c.append(value_s)

    if values_c:
        combined_attributes.append((tag_c, name_c, values_c))

    return combined_attributes


def parse_group(ipp):
    """Parse an attribute group

        https://tools.ietf.org/html/draft-sweet-rfc2910bis-07
        Internet Printing Protocol/1.1: Encoding and Transport

        3.1.2 Attribute Group

        Each "attribute-group" field is encoded as follows:

        -----------------------------------------------
        |           begin-attribute-group-tag         |  1 byte
        ----------------------------------------------------------
        |                   attribute                 |  p bytes |- 0 or more
        ----------------------------------------------------------
    """
    from collections import OrderedDict
    attribute_dict = OrderedDict()
    tag = ipp.read_tag()
    while tag is not None:
        dprint('')
        tag_s = TAG_NAME.get(tag, 'UNKNOWN')
        dprint('\ttag=0x%02x %s' % (tag, tag_s))
        assert tag in GROUP_TAGS, tag
        tag, attributes = parse_attr_1val(ipp)
        combined_attributes = combine_attribute_values(attributes)
        attribute_dict[tag_s] = combined_attributes

    assert attribute_dict
    return attribute_dict


RESULTS = 'results.tables'


def save_attribute_dict(path_in, attribute_dict):

    path = os.path.join(RESULTS, '%s.csv' % path_in)
    assert path != path_in
    # assert not os.path.exists(path), path
    dir_name = os.path.dirname(path)
    try:
        os.makedirs(dir_name)
    except FileExistsError:
        pass

    with open(path, 'w') as f:
        w = csv.writer(f)
        w.writerow(['group_tag', 'tag_name', 'name', 'value'])
        for group_tag, attributes in attribute_dict.items():
            for tag_name, name, values in attributes:
                print([name] + values, [len(values), tag_name, group_tag])
                w.writerow([group_tag, tag_name, name] + values)


def parse_body(path, ipp, parent):
    """Based on ipp.c: ippReadIO()
        ipp: IPP data
        parent: parent request, if any
    """
    print('parse_body: ipp=%s,parent=%s' % (ipp, parent))

    ipp.header = {'version': ipp.read(2),
                  'op_status': be2(ipp.read(2)),
                  'request_id': be4(ipp.read(4))
                  }
    print('HEADER', ipp.header)

    attribute_dict = parse_group(ipp)
    save_attribute_dict(path, attribute_dict)


def dump(text):
    import string
    visible = []
    v = []
    i0 = None
    for i, c in enumerate(text):
        s = chr(c)
        if s not in string.printable:
            s = ''
            if v:
                visible.append((i0, v))
                v = []
            i0 = None
        else:
            v.append(s)
            if i0 is None:
                i0 = i

        print('%4d: %02x %s' % (i, c, s))

    if v:
        visible.append(v)
    visible = [(i, ''.join(v)) for i, v in visible]
    visible = [(i, v.strip(r' \t\n\x0A')) for i, v in visible]
    visible = [(i, v) for i, v in visible if len(v) >= 2]
    for i, v in visible:
        print('%3d: %s' % (i, ''.join(v)))
    assert False


def process_file(path):
    print('#' * 80)
    print(path, os.path.getsize(path))

    with open(path, 'rb') as f:
        text = f.read()

    t0 = text[0]
    dprint('type=%s,val=%s' % (type(t0), t0))
    assert all(isinstance(c, int) for c in text)
    text = [int(c) for c in text]
    # dump(text)

    # version = text[:2]
    # op_status = be2(text[2:])
    # request_id = be4(text[4:])

    print('path: %s' % path)
    # print('version: %s' % version)
    # print('op_status: %d' % op_status)
    # print('request_id: %d' % request_id)

    ipp = IPP(text)

    parse_body(path, ipp, None)


def main():

    assert len(sys.argv) > 1, 'Usage: %s <control file>' % sys.argv[1]
    dir_name = sys.argv[1]

    for path in recursive_glob(dir_name):
        process_file(path)

main()
