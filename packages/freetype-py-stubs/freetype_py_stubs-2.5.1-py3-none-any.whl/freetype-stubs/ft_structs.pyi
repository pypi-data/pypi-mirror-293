#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
"""
Freetype structured types
-------------------------

FT_Library: A handle to a FreeType library instance.

FT_Vector: A simple structure used to store a 2D vector.

FT_BBox: A structure used to hold an outline's bounding box.

FT_Matrix: A simple structure used to store a 2x2 matrix.

FT_UnitVector: A simple structure used to store a 2D vector unit vector.

FT_Bitmap: A structure used to describe a bitmap or pixmap to the raster.

FT_Data: Read-only binary data represented as a pointer and a length.

FT_Generic: Client applications generic data.

FT_Bitmap_Size: Metrics of a bitmap strike.

FT_Charmap: The base charmap structure.

FT_Glyph_Metrics:A structure used to model the metrics of a single glyph.

FT_Outline: This structure is used to describe an outline to the scan-line
            converter.

FT_GlyphSlot: FreeType root glyph slot class structure.

FT_Glyph: The root glyph structure contains a given glyph image plus its
           advance width in 16.16 fixed float format.

FT_Size_Metrics: The size metrics structure gives the metrics of a size object.

FT_Size: FreeType root size class structure.

FT_Face: FreeType root face class structure.

FT_Parameter: A simple structure used to pass more or less generic parameters
              to FT_Open_Face.

FT_Open_Args: A structure used to indicate how to open a new font file or
              stream.

FT_SfntName: A structure used to model an SFNT 'name' table entry.

FT_Stroker: Opaque handler to a path stroker object.

FT_BitmapGlyph: A structure used for bitmap glyph images.
"""
from ctypes import (
    Structure,
    c_char,
    c_int,
    c_long,
    c_short,
    c_ubyte,
    c_uint,
    c_void_p,
)
from dataclasses import dataclass
from typing import TYPE_CHECKING

from freetype.ft_types import (
    FT_Bool,
    FT_Byte,
    FT_Encoding,
    FT_F2Dot14,
    FT_Fixed,
    FT_Generic_Finalizer,
    FT_Glyph_Format,
    FT_Int,
    FT_Long,
    FT_Pointer,
    FT_Pos,
    FT_Short,
    FT_String_p,
    FT_UInt,
    FT_ULong,
    FT_UShort,
)

if TYPE_CHECKING:
    # intentionally annotate with a pseudo type.
    from ctypes import _FuncPointer, _Pointer  # pyright: ignore[reportPrivateUsage]


class FT_LibraryRec(Structure):
    """
    A handle to a FreeType library instance. Each 'library' is completely
    independent from the others; it is the 'root' of a set of objects like
    fonts, faces, sizes, etc.
    """
    ...


FT_Library = _Pointer[FT_LibraryRec]


@dataclass
class FT_Vector(Structure):
    """
    A simple structure used to store a 2D vector; coordinates are of the FT_Pos
    type.
    """
    x: FT_Pos = ...
    """The horizontal coordinate."""
    y: FT_Pos = ...
    """The vertical coordinate."""


@dataclass
class FT_BBox(Structure):
    """
    A structure used to hold an outline's bounding box, i.e., the coordinates
    of its extrema in the horizontal and vertical directions.

    The bounding box is specified with the coordinates of the lower left and
    the upper right corner. In PostScript, those values are often called
    (llx, lly) and (urx, ury), respectively.

    If `yMin` is negative, this value gives the glyph's descender. Otherwise,
    the glyph doesn't descend below the baseline. Similarly, if `yMax` is
    positive, this value gives the glyph's ascender.

    `xMin` gives the horizontal distance from the glyph's origin to the left
    edge of the glyph's bounding box. If `xMin` is negative, the glyph extends
    to the left of the origin.
    """
    xMin: FT_Pos = ...
    """The horizontal minimum (left-most)."""
    yMin: FT_Pos = ...
    """The vertical minimum (bottom-most)."""
    xMax: FT_Pos = ...
    """The horizontal maximum (right-most)."""
    yMax: FT_Pos = ...
    """The vertical maximum (top-most)."""


@dataclass
class FT_Matrix(Structure):
    """
    A simple structure used to store a 2x2 matrix. Coefficients are in 16.16
    fixed float format. The computation performed is:

    x' = x*xx + y*xy
    y' = x*yx + y*yy
    """
    xx: FT_Fixed = ...
    """Matrix coefficient."""
    xy: FT_Fixed = ...
    """Matrix coefficient."""
    yx: FT_Fixed = ...
    """Matrix coefficient."""
    yy: FT_Fixed = ...
    """Matrix coefficient."""


@dataclass
class FT_UnitVector(Structure):
    """
    A simple structure used to store a 2D vector unit vector. Uses FT_F2Dot14
    types.
    """
    x: FT_F2Dot14 = ...
    """The horizontal coordinate."""
    y: FT_F2Dot14 = ...
    """The vertical coordinate."""


@dataclass
class FT_Bitmap(Structure):
    """
    A structure used to describe a bitmap or pixmap to the raster. Note that we
    now manage pixmaps of various depths through the `pixel_mode` field.
    """
    rows: c_int = ...
    """The number of bitmap rows."""
    width: c_int = ...
    """The number of pixels in bitmap row."""
    pitch: c_int = ...
    """
    The pitch's absolute value is the number of bytes taken by one bitmap row,
    including padding. However, the pitch is positive when the bitmap has a
    'down' flow, and negative when it has an 'up' flow. In all cases, the pitch
    is an offset to add to a bitmap pointer in order to go down one row.

    Note that 'padding' means the alignment of a bitmap to a byte border, and
    FreeType functions normally align to the smallest possible integer value.

    For the B/W rasterizer, 'pitch' is always an even number.

    To change the pitch of a bitmap (say, to make it a multiple of 4), use
    FT_Bitmap_Convert. Alternatively, you might use callback functions to
    directly render to the application's surface; see the file 'example2.py'
    in the tutorial for a demonstration.
    """
    # declaring buffer as c_char_p confuses ctypes
    buffer: _Pointer[c_ubyte] = ...
    """
    A typeless pointer to the bitmap buffer. This value should be aligned on
    32-bit boundaries in most cases.
    """
    num_grays: c_short = ...
    """
    This field is only used with FT_PIXEL_MODE_GRAY; it gives the number of
    gray levels used in the bitmap.
    """
    pixel_mode: c_ubyte = ...
    """
    The pixel mode, i.e., how pixel bits are stored. See FT_Pixel_Mode for
    possible values.
    """
    palette_mode: c_char = ...
    """
    This field is intended for paletted pixel modes; it indicates how the
    palette is stored. Not used currently.
    """
    palette: c_void_p = ...
    """
    A typeless pointer to the bitmap palette; this field is intended for
    paletted pixel modes. Not used currently.
    """


@dataclass
class FT_Data(Structure):
    """
    Read-only binary data represented as a pointer and a length.
    """
    pointer: _Pointer[FT_Byte] = ...
    """The data."""
    length: FT_UInt = ...
    """The length of the data in bytes."""


@dataclass
class FT_Generic(Structure):
    """
    Client applications often need to associate their own data to a variety of
    FreeType core objects. For example, a text layout API might want to
    associate a glyph cache to a given size object.

    Most FreeType object contains a 'generic' field, of type FT_Generic, which
    usage is left to client applications and font servers.

    It can be used to store a pointer to client-specific data, as well as the
    address of a 'finalizer' function, which will be called by FreeType when
    the object is destroyed (for example, the previous client example would put
    the address of the glyph cache destructor in the 'finalizer' field).
    """
    data: c_void_p = ...
    """
    A typeless pointer to any client-specified data. This field is completely
    ignored by the FreeType library.
    """
    finalizer: FT_Generic_Finalizer = ...
    """
    A pointer to a 'generic finalizer' function, which will be called when the
    object is destroyed. If this field is set to NULL, no code will be called.
    """


@dataclass
class FT_Bitmap_Size(Structure):
    """
    This structure models the metrics of a bitmap strike (i.e., a set of glyphs
    for a given point size and resolution) in a bitmap font. It is used for the
    'available_sizes' field of FT_Face.
    """
    height: FT_Short = ...
    """
    The vertical distance, in pixels, between two consecutive baselines. It is
    always positive.
    """
    width: FT_Short = ...
    """The average width, in pixels, of all glyphs in the strike."""
    size: FT_Pos = ...
    """
    The nominal size of the strike in 26.6 fractional points. This field is not
    very useful.
    """
    x_ppem: FT_Pos = ...
    """The horizontal ppem (nominal width) in 26.6 fractional pixels."""
    y_ppem: FT_Pos = ...
    """The vertical ppem (nominal height) in 26.6 fractional pixels."""


@dataclass
class FT_CharmapRec(Structure):
    """
    The base charmap structure.
    """
    face: c_void_p = ...  # Should be FT_Face
    """
    A handle to the parent face object.

    Cast to `FT_Face` manually if needed.
    """
    encoding: FT_Encoding = ...
    """
    An FT_Encoding tag identifying the charmap. Use this with
    FT_Select_Charmap.
    """
    platform_id: FT_UShort = ...
    """
    An ID number describing the platform for the following encoding ID. This
    comes directly from the TrueType specification and should be emulated for
    other formats.
    """
    encoding_id: FT_UShort = ...
    """
    A platform specific encoding number. This also comes from the TrueType
    specification and should be emulated similarly.
    """


FT_Charmap = _Pointer[FT_CharmapRec]


@dataclass
class FT_Glyph_Metrics(Structure):
    """
    A structure used to model the metrics of a single glyph. The values are
    expressed in 26.6 fractional pixel format; if the flag FT_LOAD_NO_SCALE has
    been used while loading the glyph, values are expressed in font units
    instead.
    """
    width: FT_Pos = ...
    """The glyph's width."""
    height: FT_Pos = ...
    """The glyph's height."""
    horiBearingX: FT_Pos = ...
    """Left side bearing for horizontal layout."""
    horiBearingY: FT_Pos = ...
    """Top side bearing for horizontal layout."""
    horiAdvance: FT_Pos = ...
    """Advance width for horizontal layout."""
    vertBearingX: FT_Pos = ...
    """Left side bearing for vertical layout."""
    vertBearingY: FT_Pos = ...
    """Top side bearing for vertical layout."""
    vertAdvance: FT_Pos = ...
    """Advance height for vertical layout."""


@dataclass
class FT_Outline(Structure):
    """
    This structure is used to describe an outline to the scan-line converter.
    """
    n_contours: c_short = ...
    """The number of contours in the outline."""
    n_points: c_short = ...
    """The number of points in the outline."""
    points: _Pointer[FT_Vector] = ...
    """
    A pointer to an array of 'n_points' FT_Vector elements, giving the
    outline's point coordinates.
    """
    # declaring buffer as c_char_p would prevent us to access all tags
    tags: _Pointer[c_ubyte] = ...
    """
    A pointer to an array of 'n_points' chars, giving each outline point's
    type.

    If bit 0 is unset, the point is 'off' the curve, i.e., a Bezier control
    point, while it is 'on' if set.

    Bit 1 is meaningful for 'off' points only. If set, it indicates a
    third-order Bezier arc control point; and a second-order control point if
    unset.

    If bit 2 is set, bits 5-7 contain the drop-out mode (as defined in the
    OpenType specification; the value is the same as the argument to the
    SCANMODE instruction).

    Bits 3 and 4 are reserved for internal purposes.
    """
    contours: _Pointer[c_short] = ...
    """
    An array of `n_contours` shorts, giving the end point of each contour
    within the outline. For example, the first contour is defined by the points
    `0` to `contours[0]`, the second one is defined by the points
    `contours[0]+1` to `contours[1]`, etc.
    """
    flags: c_int = ...
    """
    A set of bit flags used to characterize the outline and give hints to the
    scan-converter and hinter on how to convert/grid-fit it. See
    FT_OUTLINE_FLAGS.
    """


FT_Outline_MoveToFunc = _FuncPointer
""">>> CFUNCTYPE(c_int, _Pointer[FT_Vector], py_object)"""
FT_Outline_LineToFunc = _FuncPointer
""">>> CFUNCTYPE(c_int, _Pointer[FT_Vector], py_object)"""
FT_Outline_ConicToFunc = _FuncPointer
""">>> CFUNCTYPE(c_int, _Pointer[FT_Vector], _Pointer[FT_Vector], py_object)"""
FT_Outline_CubicToFunc = _FuncPointer
""">>> CFUNCTYPE(c_int, _Pointer[FT_Vector], _Pointer[FT_Vector], _Pointer[FT_Vector], py_object)"""


@dataclass
class FT_Outline_Funcs(Structure):
    """
    This structure holds a set of callbacks which are called by
    FT_Outline_Decompose.
    """
    move_to: FT_Outline_MoveToFunc = ...
    """Callback when outline needs to jump to a new path component."""
    line_to: FT_Outline_LineToFunc = ...
    """
    Callback to draw a straight line from the current position to the control
    point.
    """
    conic_to: FT_Outline_ConicToFunc = ...
    """
    Callback to draw a second-order Bézier curve from the current position
    using the passed control points.
    """
    cubic_to: FT_Outline_CubicToFunc = ...
    """
    Callback to draw a third-order Bézier curve from the current position using
    the passed control points.
    """
    shift: c_int = ...
    """
    Passed to FreeType which will transform vectors via
        `x = (x << shift) - delta` and `y = (y << shift) - delta`
    """
    delta: FT_Pos = ...
    """
    Passed to FreeType which will transform vectors via
        `x = (x << shift) - delta` and `y = (y << shift) - delta`
    """


@dataclass
class FT_GlyphRec(Structure):
    """
    The root glyph structure contains a given glyph image plus its advance
    width in 16.16 fixed float format.
    """
    library: FT_Library = ...
    """A handle to the FreeType library object."""
    clazz: c_void_p = ...
    """A pointer to the glyph's class. Private."""
    format: FT_Glyph_Format = ...
    """The format of the glyph's image."""
    advance: FT_Vector = ...
    """A 16.16 vector that gives the glyph's advance width."""


FT_Glyph = _Pointer[FT_GlyphRec]


@dataclass
class FT_GlyphSlotRec(Structure):
    """
    FreeType root glyph slot class structure. A glyph slot is a container where
    individual glyphs can be loaded, be they in outline or bitmap format.
    """
    library: FT_Library = ...
    """A handle to the FreeType library instance this slot belongs to."""
    face: c_void_p = ...
    """
    A handle to the parent face object.
    
    Cast to `FT_Face` manually if needed.
    """
    next: c_void_p = ...
    """
    In some cases (like some font tools), several glyph slots per face object
    can be a good thing. As this is rare, the glyph slots are listed through a
    direct, single-linked list using its 'next' field.
    """
    
    # new in FreeType 2.10;
    # was reserved previously and retained for binary compatibility
    glyph_index: c_uint = ...
    """
    The glyph index passed as an argument to FT_Load_Glyph while initializing
    the glyph slot.
    """
    generic: FT_Generic = ...
    """
    A typeless pointer which is unused by the FreeType library or any of its
    drivers. It can be used by client applications to link their own data to
    each glyph slot object.
    """

    metrics: FT_Glyph_Metrics = ...
    """
    The metrics of the last loaded glyph in the slot. The returned values
    depend on the last load flags (see the FT_Load_Glyph API function) and can
    be expressed either in 26.6 fractional pixels or font units.

    Note that even when the glyph image is transformed, the metrics are not.
    """
    linearHoriAdvance: FT_Fixed = ...
    """
    The advance width of the unhinted glyph. Its value is expressed in 16.16
    fractional pixels, unless FT_LOAD_LINEAR_DESIGN is set when loading the
    glyph. This field can be important to perform correct WYSIWYG layout. Only
    relevant for outline glyphs.
    """
    linearVertAdvance: FT_Fixed = ...
    """
    The advance height of the unhinted glyph. Its value is expressed in 16.16
    fractional pixels, unless FT_LOAD_LINEAR_DESIGN is set when loading the
    glyph. This field can be important to perform correct WYSIWYG layout. Only
    relevant for outline glyphs.
    """
    advance: FT_Vector = ...
    """
    This shorthand is, depending on FT_LOAD_IGNORE_TRANSFORM, the transformed
    advance width for the glyph (in 26.6 fractional pixel format). As specified
    with FT_LOAD_VERTICAL_LAYOUT, it uses either the 'horiAdvance' or the
    'vertAdvance' value of 'metrics' field.
    """

    format: FT_Glyph_Format = ...
    """
    This field indicates the format of the image contained in the glyph slot.
    Typically FT_GLYPH_FORMAT_BITMAP, FT_GLYPH_FORMAT_OUTLINE, or
    FT_GLYPH_FORMAT_COMPOSITE, but others are possible.
    """

    bitmap: FT_Bitmap = ...
    """
    This field is used as a bitmap descriptor when the slot format is
    FT_GLYPH_FORMAT_BITMAP. Note that the address and content of the bitmap
    buffer can change between calls of FT_Load_Glyph and a few other functions.
    """
    bitmap_left: FT_Int = ...
    """
    This is the bitmap's left bearing expressed in integer pixels. Of course,
    this is only valid if the format is FT_GLYPH_FORMAT_BITMAP.
    """
    bitmap_top: FT_Int = ...
    """
    This is the bitmap's top bearing expressed in integer pixels. Remember that
    this is the distance from the baseline to the top-most glyph scanline,
    upwards y coordinates being positive.
    """

    outline: FT_Outline = ...
    """
    The outline descriptor for the current glyph image if its format is
    FT_GLYPH_FORMAT_OUTLINE. Once a glyph is loaded, `outline` can be
    transformed, distorted, embolded, etc. However, it must not be freed.
    """
    num_subglyphs: FT_UInt = ...
    """
    The number of subglyphs in a composite glyph. This field is only valid for
    the composite glyph format that should normally only be loaded with the
    FT_LOAD_NO_RECURSE flag. For now this is internal to FreeType.
    """
    subglyphs: c_void_p = ...
    """
    An array of subglyph descriptors for composite glyphs. There are
    `num_subglyphs` elements in there. Currently internal to FreeType.
    """

    control_data: c_void_p = ...
    """
    Certain font drivers can also return the control data for a given glyph
    image (e.g. TrueType bytecode, Type 1 charstrings, etc.). This field is a
    pointer to such data.
    """
    control_len: c_long = ...
    """This is the length in bytes of the control data."""

    lsb_delta: FT_Pos = ...
    """
    The difference between hinted and unhinted left side bearing while
    autohinting is active. Zero otherwise.
    """
    rsb_delta: FT_Pos = ...
    """
    The difference between hinted and unhinted right side bearing while
    autohinting is active. Zero otherwise.
    """
    other: c_void_p = ...
    """
    Really wicked formats can use this pointer to present their own glyph image
    to client applications. Note that the application needs to know about the
    image format.
    """
    internal: c_void_p = ...


FT_GlyphSlot = _Pointer[FT_GlyphSlotRec]


@dataclass
class FT_Size_Metrics(Structure):
    """
    The size metrics structure gives the metrics of a size object.
    """
    x_ppem: FT_UShort = ...
    """
    The width of the scaled EM square in pixels, hence the term 'ppem' (pixels
    per EM). It is also referred to as 'nominal width'.
    """
    y_ppem: FT_UShort = ...
    """
    The height of the scaled EM square in pixels, hence the term 'ppem' (pixels
    per EM). It is also referred to as 'nominal height'.
    """

    x_scale: FT_Fixed = ...
    """
    A 16.16 fractional scaling value used to convert horizontal metrics from
    font units to 26.6 fractional pixels. Only relevant for scalable font
    formats.
    """
    y_scale: FT_Fixed = ...
    """
    A 16.16 fractional scaling value used to convert vertical metrics from font
    units to 26.6 fractional pixels. Only relevant for scalable font formats.
    """

    ascender: FT_Pos = ...
    """
    The ascender in 26.6 fractional pixels. See FT_FaceRec for the details.
    """
    descender: FT_Pos = ...
    """
    The descender in 26.6 fractional pixels. See FT_FaceRec for the details.
    """
    height: FT_Pos = ...
    """The height in 26.6 fractional pixels. See FT_FaceRec for the details."""
    max_advance: FT_Pos = ...
    """
    The maximal advance width in 26.6 fractional pixels. See FT_FaceRec for the
    details.
    """


@dataclass
class FT_SizeRec(Structure):
    """
    FreeType root size class structure. A size object models a face object at a
    given size.
    """
    face: c_void_p = ...
    """
    Handle to the parent face object.

    Cast to `FT_Face` manually if needed.
    """
    generic: FT_Generic = ...
    """
    A typeless pointer, which is unused by the FreeType library or any of its
    drivers. It can be used by client applications to link their own data to
    each size object.
    """
    metrics: FT_Size_Metrics = ...
    """Metrics for this size object. This field is read-only."""
    internal: c_void_p = ...


FT_Size = _Pointer[FT_SizeRec]


@dataclass
class FT_FaceRec(Structure):
    """
    FreeType root face class structure. A face object models a typeface in a
    font file.
    """
    num_faces: FT_Long = ...
    """
    The number of faces in the font file. Some font formats can have multiple
    faces in a font file.
    """
    face_index: FT_Long = ...
    """
    The index of the face in the font file. It is set to 0 if there is only one
    face in the font file.
    """

    face_flags: FT_Long = ...
    """
    A set of bit flags that give important information about the face; see
    FT_FACE_FLAG_XXX for the details.
    """
    style_flags: FT_Long = ...
    """
    A set of bit flags indicating the style of the face; see FT_STYLE_FLAG_XXX
    for the details.
    """

    num_glyphs: FT_Long = ...
    """
    The number of glyphs in the face. If the face is scalable and has sbits
    (see 'num_fixed_sizes'), it is set to the number of outline glyphs.

    For CID-keyed fonts, this value gives the highest CID used in the font.
    """

    family_name: FT_String_p = ...
    """
    The face's family name. This is an ASCII string, usually in English, which
    describes the typeface's family (like 'Times New Roman', 'Bodoni',
    'Garamond', etc). This is a least common denominator used to list fonts.
    Some formats (TrueType & OpenType) provide localized and Unicode versions
    of this string. Applications should use the format specific interface to
    access them. Can be NULL (e.g., in fonts embedded in a PDF file).
    """
    style_name: FT_String_p = ...
    """
    The face's style name. This is an ASCII string, usually in English, which
    describes the typeface's style (like 'Italic', 'Bold', 'Condensed', etc).
    Not all font formats provide a style name, so this field is optional, and
    can be set to NULL. As for 'family_name', some formats provide localized
    and Unicode versions of this string. Applications should use the format
    specific interface to access them.
    """

    num_fixed_sizes: FT_Int = ...
    """
    The number of bitmap strikes in the face. Even if the face is scalable,
    there might still be bitmap strikes, which are called 'sbits' in that case.
    """
    available_sizes: _Pointer[FT_Bitmap_Size] = ...
    """
    An array of FT_Bitmap_Size for all bitmap strikes in the face. It is set to
    NULL if there is no bitmap strike.
    """

    num_charmaps: c_int = ...
    """The number of charmaps in the face."""
    charmaps: _Pointer[FT_Charmap] = ...
    """An array of the charmaps of the face."""

    generic: FT_Generic = ...
    """
    A field reserved for client uses. See the FT_Generic type description.
    """

    # The following member variables (down to `underline_thickness')
    # are only relevant to scalable outlines; cf. @FT_Bitmap_Size
    # for bitmap fonts.
    bbox: FT_BBox = ...
    """
    The font bounding box. Coordinates are expressed in font units (see
    'units_per_EM'). The box is large enough to contain any glyph from the
    font. Thus, 'bbox.yMax' can be seen as the 'maximal ascender', and
    'bbox.yMin' as the 'minimal descender'. Only relevant for scalable formats.
    
    Note that the bounding box might be off by (at least) one pixel for hinted
    fonts. See FT_Size_Metrics for further discussion.
    """

    units_per_EM: FT_UShort = ...
    """
    The number of font units per EM square for this face. This is typically
    2048 for TrueType fonts, and 1000 for Type 1 fonts. Only relevant for
    scalable formats.
    """
    ascender: FT_Short = ...
    """
    The typographic ascender of the face, expressed in font units. For font
    formats not having this information, it is set to 'bbox.yMax'. Only
    relevant for scalable formats.
    """
    descender: FT_Short = ...
    """
    The typographic descender of the face, expressed in font units. For font
    formats not having this information, it is set to 'bbox.yMin'. Note that
    this field is usually negative. Only relevant for scalable formats.
    """
    height: FT_Short = ...
    """
    The height is the vertical distance between two consecutive baselines,
    expressed in font units. It is always positive. Only relevant for scalable
    formats.
    """

    max_advance_width: FT_Short = ...
    """
    The maximal advance width, in font units, for all glyphs in this face. This
    can be used to make word wrapping computations faster. Only relevant for
    scalable formats.
    """
    max_advance_height: FT_Short = ...
    """
    The maximal advance height, in font units, for all glyphs in this face.
    This is only relevant for vertical layouts, and is set to 'height' for
    fonts that do not provide vertical metrics. Only relevant for scalable
    formats.
    """

    underline_position: FT_Short = ...
    """
    The position, in font units, of the underline line for this face. It is the
    center of the underlining stem. Only relevant for scalable formats.
    """
    underline_thickness: FT_Short = ...
    """
    The thickness, in font units, of the underline for this face. Only relevant
    for scalable formats.
    """

    glyph: FT_GlyphSlot = ...
    """The face's associated glyph slot(s)."""
    size: FT_Size = ...
    """The current active size for this face."""
    charmap: FT_Charmap = ...
    """The current active charmap for this face."""

    # private
    driver: c_void_p = ...
    memory: c_void_p = ...
    stream: c_void_p = ...
    sizes_list_head: c_void_p = ...
    sizes_list_tail: c_void_p = ...
    autohint: FT_Generic = ...
    extensions: c_void_p = ...
    internal: c_void_p = ...


FT_Face = _Pointer[FT_FaceRec]


@dataclass
class FT_Parameter(Structure):
    """
    A simple structure used to pass more or less generic parameters to
    FT_Open_Face.
    """
    tag: FT_ULong = ...
    """A four-byte identification tag."""
    data: FT_Pointer = ...
    """A pointer to the parameter data"""


FT_Parameter_p = _Pointer[FT_Parameter]


@dataclass
class FT_Open_Args(Structure):
    """
    A structure used to indicate how to open a new font file or stream. A pointer
    to such a structure can be used as a parameter for the functions FT_Open_Face
    and FT_Attach_Stream.
    """
    flags: FT_UInt = ...
    """A set of bit flags indicating how to use the structure."""
    memory_base: _Pointer[FT_Byte] = ...
    """The first byte of the file in memory."""
    memory_size: FT_Long = ...
    """The size in bytes of the file in memory."""
    pathname: FT_String_p = ...
    """A pointer to an 8-bit file pathname."""
    stream: c_void_p = ...
    """A handle to a source stream object."""
    driver: c_void_p = ...
    """
    This field is exclusively used by FT_Open_Face; it simply specifies the
    font driver to use to open the face. If set to 0, FreeType tries to load
    the face with each one of the drivers in its list.
    """
    num_params: FT_Int = ...
    """The number of extra parameters."""
    params: FT_Parameter_p = ...
    """Extra parameters passed to the font driver when opening a new face."""


@dataclass
class FT_SfntName(Structure):
    platform_id: FT_UShort = ...
    """The platform ID for `string`."""
    encoding_id: FT_UShort = ...
    """The encoding ID for `string`."""
    language_id: FT_UShort = ...
    """The language ID for `string`"""
    name_id: FT_UShort = ...
    """An identifier for `string`"""
    # this string is *not* null-terminated!
    string: _Pointer[FT_Byte] = ...
    """
    The 'name' string. Note that its format differs depending on the (platform,
    encoding) pair. It can be a Pascal String, a UTF-16 one, etc.

    Generally speaking, the string is not zero-terminated. Please refer to the
    TrueType specification for details.
    """
    string_len: FT_UInt = ...
    """The length of `string` in bytes."""


@dataclass
class FT_StrokerRec(Structure):
    """
    Opaque handler to a path stroker object.
    """
    ...


FT_Stroker = _Pointer[FT_StrokerRec]


@dataclass
class FT_BitmapGlyphRec(Structure):
    """
    A structure used for bitmap glyph images. This really is a 'sub-class' of
    FT_GlyphRec.
    """
    root: FT_GlyphRec = ...
    left: FT_Int = ...
    top: FT_Int = ...
    bitmap: FT_Bitmap = ...


FT_BitmapGlyph = _Pointer[FT_BitmapGlyphRec]


@dataclass
class FT_Var_Axis(Structure):
    """
    A structure to model a given axis in design space for Multiple Masters,
    TrueType GX, and OpenType variation fonts.
    """
    name: FT_String_p = ...
    minimum: FT_Fixed = ...
    default: FT_Fixed = ...
    maximum: FT_Fixed = ...
    tag: FT_ULong = ...
    strid: FT_UInt = ...


@dataclass
class FT_Var_Named_Style(Structure):
    """
    A structure to model a named instance in a TrueType GX or OpenType
    variation font.
    """
    coords: _Pointer[FT_Fixed] = ...
    strid: FT_UInt = ...
    psid: FT_UInt = ...


@dataclass
class FT_MM_Var(Structure):
    """
    A structure to model the axes and space of an Adobe MM, TrueType GX,
    or OpenType variation font.
    Some fields are specific to one format and not to the others.
    """
    num_axis: FT_UInt = ...
    num_designs: FT_UInt = ...
    num_namedstyles: FT_UInt = ...
    axis: _Pointer[FT_Var_Axis] = ...
    namedstyle: _Pointer[FT_Var_Named_Style] = ...


SVG_Lib_Init_Func = _FuncPointer
""">>> CFUNCTYPE(c_int, _Pointer[py_object])"""
SVG_Lib_Free_Func = _FuncPointer
""">>> CFUNCTYPE(None, _Pointer[py_object])"""
SVG_Lib_Render_Func = _FuncPointer
""">>> CFUNCTYPE(c_int, FT_GlyphSlot, _Pointer[py_object])"""
SVG_Lib_Preset_Slot_Func = _FuncPointer
""">>> CFUNCTYPE(c_int, FT_GlyphSlot, FT_Bool, _Pointer[py_object])"""


@dataclass
class SVG_RendererHooks(Structure):
    svg_init: SVG_Lib_Init_Func = ...
    svg_free: SVG_Lib_Free_Func = ...
    svg_render: SVG_Lib_Render_Func = ...
    svg_preset_slot: SVG_Lib_Preset_Slot_Func = ...


@dataclass
class FT_SVG_DocumentRec(Structure):
    svg_document: _Pointer[FT_Byte] = ...
    svg_document_length: FT_ULong = ...
    metrics: FT_Size_Metrics = ...
    units_per_EM: FT_UShort = ...
    start_glyph_id: FT_UShort = ...
    end_glyph_id: FT_UShort = ...
    transform: FT_Matrix = ...
    delta: FT_Vector = ...


FT_SVG_Document = _Pointer[FT_SVG_DocumentRec]


@dataclass
class FT_OpaquePaint(Structure):
    p: _Pointer[FT_Byte] = ...
    insert_root_transform: FT_Bool = ...


@dataclass
class FT_LayerIterator(Structure):
    num_layers: FT_UInt = ...
    layer: FT_UInt = ...
    p: _Pointer[FT_Byte] = ...