from ctypes import (
    c_char,
    c_char_p,
    c_int,
    c_int32,
    c_long,
    c_longlong,
    c_short,
    c_size_t,
    c_ubyte,
    c_uint,
    c_uint32,
    c_ulong,
    c_ushort,
    c_void_p,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # intentionally annotate with a pseudo type.
    from ctypes import _FuncPointer  # pyright: ignore[reportPrivateUsage]
    # provided by typeshed, and does not exist in ctypes module

FT_Byte    = c_ubyte
"""A simple typedef for the unsigned char type."""

FT_Bytes   = c_char_p
"""A typedef for constant memory areas."""

FT_Char    = c_char
"""A simple typedef for the signed char type."""

FT_Int     = c_int
"""A typedef for the int type."""

FT_UInt    = c_uint
"""A typedef for the unsigned int type."""

FT_Int16   = c_short
"""A typedef for a 16bit signed integer type."""

FT_UInt16  = c_ushort
"""A typedef for a 16bit unsigned integer type."""

FT_Int32   = c_int32
"""A typedef for a 32bit signed integer type."""

FT_UInt32  = c_uint32
"""A typedef for a 32bit unsigned integer type."""

FT_Short   = c_short
"""A typedef for signed short."""

FT_UShort  = c_ushort
"""A typedef for unsigned short."""

FT_Long    = c_long
"""A typedef for signed long."""

FT_ULong   = c_ulong
"""A typedef for unsigned long."""

FT_Bool    = c_char
"""A typedef of unsigned char, used for simple booleans. As
usual, values 1 and 0 represent true and false,
respectively."""

FT_Offset  = c_size_t
"""This is equivalent to the ANSI C 'size_t' type, i.e.,
the largest unsigned integer type used to express a file
size or position, or a memory block size."""

FT_PtrDist = c_longlong
"""This is equivalent to the ANSI C 'ptrdiff_t' type,
i.e., the largest signed integer type used to express
the distance between two pointers."""

FT_String  = c_char
"""A simple typedef for the char type, usually used for strings. """

FT_String_p= c_char_p

FT_Tag     = FT_UInt32
"""A typedef for 32-bit tags (as used in the SFNT format)."""

FT_Error   = c_int
"""The FreeType error code type. A value of 0 is always
interpreted as a successful operation."""

FT_Fixed   = c_long
"""This type is used to store 16.16 fixed float values,
like scaling values or matrix coefficients."""

FT_Angle   = FT_Fixed
"""This type is used to model angle values in FreeType.  Note that the
angle is a 16.16 fixed-point value expressed in degrees."""

FT_Pointer = c_void_p
"""A simple typedef for a typeless pointer."""

FT_Pos     = c_long
"""The type FT_Pos is used to store vectorial
coordinates. Depending on the context, these can
represent distances in integer font units, or 16.16, or
26.6 fixed float pixel coordinates."""

FT_FWord   = c_short
"""A signed 16-bit integer used to store a distance in
original font units."""

FT_UFWord  = c_ushort
"""An unsigned 16-bit integer used to store a distance in
original font units."""

FT_F2Dot14 = c_short
"""A signed 2.14 fixed float type used for unit vectors."""

FT_F26Dot6 = c_long
"""A signed 26.6 fixed float type used for vectorial pixel
coordinates."""

FT_Glyph_Format = c_int

FT_Encoding     = c_int

FT_Generic_Finalizer = _FuncPointer  # Callable[[c_void_p], None]
"""
Describe a function used to destroy the 'client' data of any FreeType
object. See the description of the FT_Generic type for details of usage.
"""

# ----------------------------------------------------------------------------
# Types that does not exist in module
_Tag = int
"""A type alias in Python level for FT_Tag which is a 32-bit tag."""

_Encoding = int
"""A type alias in Python level for FT_Encoding which is a tag."""

_Fixed = int
"""A type alias in Python level for FT_Fixed which is a 16.16 fixed float."""

_Angle = int
"""A type alias in Python level for FT_Angle which is a 16.16 fixed float."""

_Pos = int
"""A type alias in Python level for FT_Pos which may vary from integer, 16.16
fixed float, or 26.6 fixed float depending on the context."""

_F2Dot14 = int
"""A type alias in Python level for FT_Angle which is a 2.14 fixed float."""

_F26Dot6 = int
"""A type alias in Python level for FT_Angle which is a 26.6 fixed float."""
