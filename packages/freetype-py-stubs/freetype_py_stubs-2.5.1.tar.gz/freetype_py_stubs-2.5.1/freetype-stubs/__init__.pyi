import sys
from ctypes import c_void_p

from freetype.ft_structs import (
    FT_BBox,
    FT_Bitmap,
    FT_Bitmap_Size,
    FT_BitmapGlyphRec,
    FT_CharmapRec,
    FT_FaceRec,
    FT_Glyph_Metrics,
    FT_GlyphRec,
    FT_GlyphSlotRec,
    FT_LibraryRec,
    FT_Matrix,
    FT_MM_Var,
    FT_Outline,
    FT_SfntName,
    FT_Size_Metrics,
    FT_StrokerRec,
    FT_Var_Axis,
    FT_Vector,
)
from freetype.raw import filename
from typing_extensions import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Callable,
    Generator,
    Iterable,
    Self,
    TypeVar,
    override,
)

if sys.version_info >= (3,):
    # Hack to get unicode class in python3
    unicode = str

if TYPE_CHECKING:
    # use TYPE_CHECKING here because they doesn't exist actually.
    # intentionally annotate with a pseudo type.
    from ctypes import _FuncPointer, _Pointer  # pyright: ignore[reportPrivateUsage]

    from freetype.ft_types import (
        _Encoding,  # pyright: ignore[reportPrivateUsage]
        _F26Dot6,  # pyright: ignore[reportPrivateUsage]
        _Fixed,  # pyright: ignore[reportPrivateUsage]
        _Pos,  # pyright: ignore[reportPrivateUsage]
    )

    CharLike = int | str

def unmake_tag(i: int) -> str: ...

class _FT_Library_Wrapper(_Pointer[FT_LibraryRec]):
    """Subclass of FT_Library to help with calling FT_Done_FreeType"""

    def __del__(self) -> None: ...

_handle: _FT_Library_Wrapper
FT_Library_filename = filename

def _init_freetype() -> None: ...
def get_handle() -> _FT_Library_Wrapper:
    """Get unique FT_Library handle"""
    ...

def version() -> tuple[int, int, int]:
    """
    Return the version of the FreeType library being used as a tuple of
    (major version number, minor version number, patch version number)
    """
    ...

def set_lcd_filter(filt: int) -> None:
    """
    This function is used to apply color filtering to LCD decimated bitmaps,
    like the ones used when calling FT_Render_Glyph with FT_RENDER_MODE_LCD or
    FT_RENDER_MODE_LCD_V.

    **Note**

    This feature is always disabled by default. Clients must make an explicit
    call to this function with a 'filter' value other than FT_LCD_FILTER_NONE
    in order to enable it.

    Due to PATENTS covering subpixel rendering, this function doesn't do
    anything except returning 'FT_Err_Unimplemented_Feature' if the
    configuration macro FT_CONFIG_OPTION_SUBPIXEL_RENDERING is not defined in
    your build of the library, which should correspond to all default builds of
    FreeType.

    The filter affects glyph bitmaps rendered through FT_Render_Glyph,
    FT_Outline_Get_Bitmap, FT_Load_Glyph, and FT_Load_Char.

    It does not affect the output of FT_Outline_Render and
    FT_Outline_Get_Bitmap.

    If this feature is activated, the dimensions of LCD glyph bitmaps are
    either larger or taller than the dimensions of the corresponding outline
    with regards to the pixel grid. For example, for FT_RENDER_MODE_LCD, the
    filter adds up to 3 pixels to the left, and up to 3 pixels to the right.

    The bitmap offset values are adjusted correctly, so clients shouldn't need
    to modify their layout and glyph positioning code when enabling the filter.
    """
    ...

def set_lcd_filter_weights(a: int, b: int, c: int, d: int, e: int) -> None:
    """
    Use this function to override the filter weights selected by
    FT_Library_SetLcdFilter. By default, FreeType uses the quintuple (0x00,
    0x55, 0x56, 0x55, 0x00) for FT_LCD_FILTER_LIGHT, and (0x10, 0x40, 0x70,
    0x40, 0x10) for FT_LCD_FILTER_DEFAULT and FT_LCD_FILTER_LEGACY.

    **Note**

    Only available if version > 2.4.0
    """
    ...

def _encode_filename(filename: str) -> bytes: ...

Vector = FT_Vector
Matrix = FT_Matrix

def FT_Done_MM_Var_func(p: _Pointer[FT_MM_Var]) -> None: ...

class BBox:
    """
    FT_BBox wrapper.

    A structure used to hold an outline's bounding box, i.e., the coordinates
    of its extrema in the horizontal and vertical directions.

    **Note**

    The bounding box is specified with the coordinates of the lower left and
    the upper right corner. In PostScript, those values are often called
    (llx,lly) and (urx,ury), respectively.

    If 'yMin' is negative, this value gives the glyph's descender. Otherwise,
    the glyph doesn't descend below the baseline. Similarly, if 'ymax' is
    positive, this value gives the glyph's ascender.

    'xMin' gives the horizontal distance from the glyph's origin to the left
    edge of the glyph's bounding box. If 'xMin' is negative, the glyph
    extends to the left of the origin.
    """

    _FT_BBox: FT_BBox

    def __init__(self, bbox: FT_BBox | tuple[_Pos, _Pos, _Pos, _Pos]) -> None:
        """
        Create a new BBox object.

        :param bbox: a FT_BBox or a tuple of 4 values
        """
        ...

    @property
    def xMin(self) -> _Pos:
        """The horizontal minimum (left-most)."""
        ...

    @property
    def yMin(self) -> _Pos:
        """The vertical minimum (bottom-most)."""
        ...

    @property
    def xMax(self) -> _Pos:
        """The horizontal maximum (right-most)."""
        ...

    @property
    def yMax(self) -> _Pos:
        """The vertical maximum (top-most)."""
        ...

class GlyphMetrics:
    """
    A structure used to model the metrics of a single glyph. The values are
    expressed in 26.6 fractional pixel format; if the flag FT_LOAD_NO_SCALE has
    been used while loading the glyph, values are expressed in font units
    instead.

    **Note**

    If not disabled with FT_LOAD_NO_HINTING, the values represent dimensions of
    the hinted glyph (in case hinting is applicable).

    Stroking a glyph with an outside border does not increase ‘horiAdvance’ or
    ‘vertAdvance’; you have to manually adjust these values to account for the
    added width and height.
    """

    _FT_Glyph_Metrics: FT_Glyph_Metrics

    def __init__(self, metrics: FT_Glyph_Metrics) -> None:
        """
        Create a new GlyphMetrics object.

        :param metrics: a FT_Glyph_Metrics
        """
        ...

    @property
    def width(self) -> _Pos:
        """The glyph's width."""
        ...

    @property
    def height(self) -> _Pos:
        """The glyph's height."""
        ...

    @property
    def horiBearingX(self) -> _Pos:
        """Left side bearing for horizontal layout."""
        ...

    @property
    def horiBearingY(self) -> _Pos:
        """Top side bearing for horizontal layout."""
        ...

    @property
    def horiAdvance(self) -> _Pos:
        """Advance width for horizontal layout."""
        ...

    @property
    def vertBearingX(self) -> _Pos:
        """Left side bearing for vertical layout."""
        ...

    @property
    def vertBearingY(self) -> _Pos:
        """
        Top side bearing for vertical layout. Larger positive values mean
        further below the vertical glyph origin.
        """
        ...

    @property
    def vertAdvance(self) -> _Pos:
        """
        Advance height for vertical layout. Positive values mean the glyph has
        a positive advance downward.
        """
        ...

class SizeMetrics:
    """
    The size metrics structure gives the metrics of a size object.

    **Note**

    The scaling values, if relevant, are determined first during a size
    changing operation. The remaining fields are then set by the driver. For
    scalable formats, they are usually set to scaled values of the
    corresponding fields in Face.

    Note that due to glyph hinting, these values might not be exact for certain
    fonts. Thus they must be treated as unreliable with an error margin of at
    least one pixel!

    Indeed, the only way to get the exact metrics is to render all glyphs. As
    this would be a definite performance hit, it is up to client applications
    to perform such computations.

    The SizeMetrics structure is valid for bitmap fonts also.
    """

    _FT_Size_Metrics: FT_Size_Metrics

    def __init__(self, metrics: FT_Size_Metrics) -> None:
        """
        Create a new SizeMetrics object.

        :param metrics: a FT_SizeMetrics
        """
        ...

    @property
    def x_ppem(self) -> int:
        """
        The width of the scaled EM square in pixels, hence the term 'ppem'
        (pixels per EM). It is also referred to as 'nominal width'.
        """
        ...

    @property
    def y_ppem(self) -> int:
        """
        The height of the scaled EM square in pixels, hence the term 'ppem'
        (pixels per EM). It is also referred to as 'nominal height'.
        """
        ...

    @property
    def x_scale(self) -> _Fixed:
        """
        A 16.16 fractional scaling value used to convert horizontal metrics
        from font units to 26.6 fractional pixels. Only relevant for scalable
        font formats.
        """
        ...

    @property
    def y_scale(self) -> _Fixed:
        """
        A 16.16 fractional scaling value used to convert vertical metrics from
        font units to 26.6 fractional pixels. Only relevant for scalable font
        formats.
        """
        ...

    @property
    def ascender(self) -> _Pos:
        """
        The ascender in 26.6 fractional pixels. See Face for the details.
        """
        ...

    @property
    def descender(self) -> _Pos:
        """
        The descender in 26.6 fractional pixels. See Face for the details.
        """
        ...

    @property
    def height(self) -> _Pos:
        """The height in 26.6 fractional pixels. See Face for the details."""
        ...

    @property
    def max_advance(self) -> _Pos:
        """
        The maximal advance width in 26.6 fractional pixels. See Face for the
        details.
        """
        ...

class BitmapSize:
    """
    FT_Bitmap_Size wrapper

    This structure models the metrics of a bitmap strike (i.e., a set of glyphs
    for a given point size and resolution) in a bitmap font. It is used for the
    'available_sizes' field of Face.

    **Note**

    Windows FNT: The nominal size given in a FNT font is not reliable. Thus
    when the driver finds it incorrect, it sets 'size' to some calculated
    values and sets 'x_ppem' and 'y_ppem' to the pixel width and height given
    in the font, respectively.

    TrueType embedded bitmaps: 'size', 'width', and 'height' values are not
    contained in the bitmap strike itself. They are computed from the global
    font parameters.
    """

    _FT_Bitmap_Size: FT_Bitmap_Size

    def __init__(self, size: FT_Bitmap_Size) -> None:
        """
        Create a new SizeMetrics object.

        :param size: a FT_Bitmap_Size
        """
        ...

    @property
    def height(self) -> int:
        """
        The vertical distance, in pixels, between two consecutive baselines.
        It is always positive.
        """
        ...

    @property
    def width(self) -> int:
        """The average width, in pixels, of all glyphs in the strike."""
        ...

    @property
    def size(self) -> _Pos:
        """
        The nominal size of the strike in 26.6 fractional points. This field
        is not very useful.
        """
        ...

    @property
    def x_ppem(self) -> _Pos:
        """The horizontal ppem (nominal width) in 26.6 fractional pixels."""
        ...

    @property
    def y_ppem(self) -> _Pos:
        """The vertical ppem (nominal width) in 26.6 fractional pixels."""
        ...

class Bitmap(object):
    """
    FT_Bitmap wrapper

    A structure used to describe a bitmap or pixmap to the raster. Note that we
    now manage pixmaps of various depths through the 'pixel_mode' field.

    *Note*:

      For now, the only pixel modes supported by FreeType are mono and
      grays. However, drivers might be added in the future to support more
      'colorful' options.
    """

    _FT_Bitmap: FT_Bitmap

    def __init__(self, bitmap: _Pointer[FT_Bitmap]) -> None:
        """
        Create a new Bitmap object.

        :param bitmap: a FT_Bitmap
        """
        ...

    @property
    def rows(self) -> int:
        """The number of bitmap rows."""
        ...

    @property
    def width(self) -> int:
        """The number of pixels in bitmap row."""
        ...

    @property
    def pitch(self) -> int:
        """
        The pitch's absolute value is the number of bytes taken by one bitmap
        row, including padding. However, the pitch is positive when the bitmap
        has a 'down' flow, and negative when it has an 'up' flow. In all
        cases, the pitch is an offset to add to a bitmap pointer in order to
        go down one row.

        Note that 'padding' means the alignment of a bitmap to a byte border,
        and FreeType functions normally align to the smallest possible integer
        value.

        For the B/W rasterizer, 'pitch' is always an even number.

        To change the pitch of a bitmap (say, to make it a multiple of 4), use
        FT_Bitmap_Convert. Alternatively, you might use callback functions to
        directly render to the application's surface; see the file
        'example2.py' in the tutorial for a demonstration.
        """
        ...

    @property
    def buffer(self) -> list[int]:
        """
        A typeless pointer to the bitmap buffer. This value should be aligned
        on 32-bit boundaries in most cases.
        """
        ...

    @property
    def num_grays(self) -> int:
        """
        This field is only used with FT_PIXEL_MODE_GRAY; it gives the number
        of gray levels used in the bitmap.
        """
        ...

    @property
    def pixel_mode(self) -> int:
        """
        The pixel mode, i.e., how pixel bits are stored. See FT_Pixel_Mode for
        possible values.
        """
        ...

    @property
    def palette_mode(self) -> bytes:
        """
        This field is intended for paletted pixel modes; it indicates how the
        palette is stored. Not used currently.
        """
        ...

    @property
    def palette(self) -> c_void_p:
        """
        A typeless pointer to the bitmap palette; this field is intended for
        paletted pixel modes. Not used currently.
        """
        ...

class Charmap:
    """
    FT_Charmap wrapper.

    A handle to a given character map. A charmap is used to translate character
    codes in a given encoding into glyph indexes for its parent's face. Some
    font formats may provide several charmaps per font.

    Each face object owns zero or more charmaps, but only one of them can be
    'active' and used by FT_Get_Char_Index or FT_Load_Char.

    The list of available charmaps in a face is available through the
    'face.num_charmaps' and 'face.charmaps' fields of FT_FaceRec.

    The currently active charmap is available as 'face.charmap'. You should
    call FT_Set_Charmap to change it.

    **Note**:

      When a new face is created (either through FT_New_Face or FT_Open_Face),
      the library looks for a Unicode charmap within the list and automatically
      activates it.

    **See also**:

      See FT_CharMapRec for the publicly accessible fields of a given character
      map.
    """

    _FT_Charmap: _Pointer[FT_CharmapRec]

    def __init__(self, charmap: _Pointer[FT_CharmapRec]) -> None:
        """
        Create a new Charmap object.

        Parameters:
        -----------
        charmap : a FT_Charmap
        """
        ...

    @property
    def encoding(self) -> _Encoding:
        """
        An FT_Encoding tag identifying the charmap. Use this with
        FT_Select_Charmap.
        """
        ...

    @property
    def platform_id(self) -> int:
        """
        An ID number describing the platform for the following encoding ID.
        This comes directly from the TrueType specification and should be
        emulated for other formats.
        """
        ...

    @property
    def encoding_id(self) -> int:
        """
        A platform specific encoding number. This also comes from the TrueType
        specification and should be emulated similarly.
        """
        ...

    @property
    def encoding_name(self) -> str:
        """
        A platform specific encoding name. This also comes from the TrueType
        specification and should be emulated similarly.
        """
        ...

    @property
    def index(self) -> int:
        """
        The index into the array of character maps within the face to which
        'charmap' belongs. If an error occurs, -1 is returned.
        """
        ...

    @property
    def cmap_language_id(self) -> int:
        """
        The language ID of 'charmap'. If 'charmap' doesn't belong to a
        TrueType/sfnt face, just return 0 as the default value.
        """
        ...

    @property
    def cmap_format(self) -> int:
        """
        The format of 'charmap'. If 'charmap' doesn't belong to a
        TrueType/sfnt face, return -1.
        """
        ...

if TYPE_CHECKING:
    # use TYPE_CHECKING here because they doesn't exist actually.
    _CBContextT = TypeVar("_CBContextT")
    _MoveToCallback = Callable[[_Pointer[FT_Vector], _CBContextT], int | None]
    _LineToCallback = Callable[[_Pointer[FT_Vector], _CBContextT], int | None]
    _ConicToCallback = Callable[
        [_Pointer[FT_Vector], _Pointer[FT_Vector], _CBContextT], int | None
    ]
    _CubicToCallback = Callable[
        [_Pointer[FT_Vector], _Pointer[FT_Vector], _Pointer[FT_Vector], _CBContextT],
        int | None,
    ]

class Outline:
    """
    FT_Outline wrapper.

    This structure is used to describe an outline to the scan-line converter.
    """

    _FT_Outline: FT_Outline

    def __init__(self, outline: FT_Outline) -> None:
        """
        Create a new Outline object.

        :param charmap: a FT_Outline
        """
        ...

    @property
    def n_contours(self) -> int: ...
    @property
    def contours(self) -> list[int]:
        """The number of contours in the outline."""
        ...

    @property
    def n_points(self) -> int: ...
    @property
    def points(self) -> list[tuple[int, int]]:
        """The number of points in the outline."""
        ...

    @property
    def tags(self) -> list[int]:
        """A list of 'n_points' chars, giving each outline point's type.

        If bit 0 is unset, the point is 'off' the curve, i.e., a Bezier
        control point, while it is 'on' if set.

        Bit 1 is meaningful for 'off' points only. If set, it indicates a
        third-order Bezier arc control point; and a second-order control
        point if unset.

        If bit 2 is set, bits 5-7 contain the drop-out mode (as defined
        in the OpenType specification; the value is the same as the
        argument to the SCANMODE instruction).

        Bits 3 and 4 are reserved for internal purposes."""
        ...

    @property
    def flags(self) -> int:
        """
        A set of bit flags used to characterize the outline and give hints to
        the scan-converter and hinter on how to convert/grid-fit it.
        See FT_OUTLINE_FLAGS.
        """
        ...

    def get_inside_border(self) -> int:
        """
        Retrieve the FT_StrokerBorder value corresponding to the 'inside'
        borders of a given outline.

        :return: The border index. FT_STROKER_BORDER_RIGHT for empty or invalid
                 outlines.
        """
        ...

    def get_outside_border(self) -> int:
        """
        Retrieve the FT_StrokerBorder value corresponding to the 'outside'
        borders of a given outline.

        :return: The border index. FT_STROKER_BORDER_RIGHT for empty or invalid
                 outlines.
        """
        ...

    def get_bbox(self) -> BBox:
        """
        Compute the exact bounding box of an outline. This is slower than
        computing the control box. However, it uses an advanced algorithm which
        returns very quickly when the two boxes coincide. Otherwise, the
        outline Bezier arcs are traversed to extract their extrema.
        """
        ...

    def get_cbox(self) -> BBox:
        """
        Return an outline's 'control box'. The control box encloses all the
        outline's points, including Bezier control points. Though it coincides
        with the exact bounding box for most glyphs, it can be slightly larger
        in some situations (like when rotating an outline which contains Bezier
        outside arcs).

        Computing the control box is very fast, while getting the bounding box
        can take much more time as it needs to walk over all segments and arcs
        in the outline. To get the latter, you can use the 'ftbbox' component
        which is dedicated to this single task.
        """
        ...
    _od_move_to_noop: _FuncPointer
    def _od_move_to_builder(self, cb: _MoveToCallback[Any] | None) -> _FuncPointer: ...

    _od_line_to_noop: _FuncPointer
    def _od_line_to_builder(self, cb: _LineToCallback[Any] | None) -> _FuncPointer: ...

    _od_conic_to_noop: _FuncPointer
    def _od_conic_to_builder(self, cb: _ConicToCallback[Any] | None) -> _FuncPointer: ...

    _od_cubic_to_noop: _FuncPointer
    def _od_cubic_to_builder(self, cb: _CubicToCallback[Any] | None) -> _FuncPointer: ...
    def decompose(
        self,
        context: _CBContextT = None,
        move_to: _MoveToCallback[_CBContextT] | None = None,
        line_to: _LineToCallback[_CBContextT] | None = None,
        conic_to: _ConicToCallback[_CBContextT] | None = None,
        cubic_to: _CubicToCallback[_CBContextT] | None = None,
        shift: int = 0,
        delta: int = 0,
    ) -> None:
        """
        Decompose the outline into a sequence of move, line, conic, and
        cubic segments.

        :param context: Arbitrary contextual object which will be passed as
                        the last parameter of all callbacks. Typically an
                        object to be drawn to, but can be anything.

        :param move_to: Callback which will be passed an `FT_Vector`
                        control point and the context. Called when outline
                        needs to jump to a new path component.

        :param line_to: Callback which will be passed an `FT_Vector`
                        control point and the context. Called to draw a
                        straight line from the current position to the
                        control point.

        :param conic_to: Callback which will be passed two `FT_Vector`
                         control points and the context. Called to draw a
                         second-order Bézier curve from the current
                         position using the passed control points.

        :param curve_to: Callback which will be passed three `FT_Vector`
                         control points and the context. Called to draw a
                         third-order Bézier curve from the current position
                         using the passed control points.

        :param shift: Passed to FreeType which will transform vectors via
                      `x = (x << shift) - delta` and `y = (y << shift) - delta`

        :param delta: Passed to FreeType which will transform vectors via
                      `x = (x << shift) - delta` and `y = (y << shift) - delta`

        :since: 1.3
        """
        ...

class Glyph:
    """
    FT_Glyph wrapper.

    The root glyph structure contains a given glyph image plus its advance
    width in 16.16 fixed float format.
    """

    _FT_Glyph: _Pointer[FT_GlyphRec]

    def __init__(self, glyph: _Pointer[FT_GlyphRec]) -> None:
        """
        Create Glyph object from an FT glyph.

        :param glyph: valid FT_Glyph object
        """
        ...

    def __del__(self) -> None:
        """Destroy glyph."""
        ...

    @property
    def format(self) -> int:
        """The format of the glyph's image."""
        ...

    def stroke(self, stroker: Stroker, destroy: bool = False) -> None:
        """
        Stroke a given outline glyph object with a given stroker.

        :param stroker: A stroker handle.

        :param destroy: A Boolean. If 1, the source glyph object is destroyed on
                        success.

        **Note**:

          The source glyph is untouched in case of error.
        """
        ...

    def to_bitmap(
        self, mode: int, origin: FT_Vector | _Pointer[FT_Vector], destroy: bool = False
    ) -> BitmapGlyph:
        """
        Convert a given glyph object to a bitmap glyph object.

        :param mode: An enumeration that describes how the data is rendered.

        :param origin: A pointer to a vector used to translate the glyph image
                       before rendering. Can be 0 (if no translation). The origin is
                       expressed in 26.6 pixels.

                       We also detect a plain vector and make a pointer out of it,
                       if that's the case.

        :param destroy: A boolean that indicates that the original glyph image
                        should be destroyed by this function. It is never destroyed
                        in case of error.

        **Note**:

          This function does nothing if the glyph format isn't scalable.

          The glyph image is translated with the 'origin' vector before
          rendering.

          The first parameter is a pointer to an FT_Glyph handle, that will be
          replaced by this function (with newly allocated data). Typically, you
          would use (omitting error handling):
        """
        ...

    def get_cbox(self, bbox_mode: int) -> BBox:
        """
        Return an outline's 'control box'. The control box encloses all the
        outline's points, including Bezier control points. Though it coincides
        with the exact bounding box for most glyphs, it can be slightly larger
        in some situations (like when rotating an outline which contains Bezier
        outside arcs).

        Computing the control box is very fast, while getting the bounding box
        can take much more time as it needs to walk over all segments and arcs
        in the outline. To get the latter, you can use the 'ftbbox' component
        which is dedicated to this single task.

        :param mode: The mode which indicates how to interpret the returned
                     bounding box values.

        **Note**:

          Coordinates are relative to the glyph origin, using the y upwards
          convention.

          If the glyph has been loaded with FT_LOAD_NO_SCALE, 'bbox_mode' must be
          set to FT_GLYPH_BBOX_UNSCALED to get unscaled font units in 26.6 pixel
          format. The value FT_GLYPH_BBOX_SUBPIXELS is another name for this
          constant.

          Note that the maximum coordinates are exclusive, which means that one
          can compute the width and height of the glyph image (be it in integer
          or 26.6 pixels) as:

          width  = bbox.xMax - bbox.xMin;
          height = bbox.yMax - bbox.yMin;

          Note also that for 26.6 coordinates, if 'bbox_mode' is set to
          FT_GLYPH_BBOX_GRIDFIT, the coordinates will also be grid-fitted, which
          corresponds to:

          bbox.xMin = FLOOR(bbox.xMin);
          bbox.yMin = FLOOR(bbox.yMin);
          bbox.xMax = CEILING(bbox.xMax);
          bbox.yMax = CEILING(bbox.yMax);

          To get the bbox in pixel coordinates, set 'bbox_mode' to
          FT_GLYPH_BBOX_TRUNCATE.

          To get the bbox in grid-fitted pixel coordinates, set 'bbox_mode' to
          FT_GLYPH_BBOX_PIXELS.
        """
        ...

class BitmapGlyph:
    """
    FT_BitmapGlyph wrapper.

    A structure used for bitmap glyph images. This really is a 'sub-class' of
    FT_GlyphRec.
    """

    _FT_BitmapGlyph: _Pointer[FT_BitmapGlyphRec]

    def __init__(self, glyph: _Pointer[FT_GlyphRec]) -> None:
        """
        Create Glyph object from an FT glyph.

        Parameters:
        -----------
          glyph: valid FT_Glyph object
        """
        ...
    # def __del__( self ):
    #     """
    #     Destroy glyph.
    #     """
    #     FT_Done_Glyph( cast(self._FT_BitmapGlyph, FT_Glyph) )

    @property
    def format(self) -> int:
        """The format of the glyph's image."""
        ...

    @property
    def bitmap(self) -> Bitmap:
        """A descriptor for the bitmap."""
        ...

    @property
    def left(self) -> int:
        """
        The left-side bearing, i.e., the horizontal distance from the current
        pen position to the left border of the glyph bitmap.
        """
        ...

    @property
    def top(self) -> int:
        """
        The top-side bearing, i.e., the vertical distance from the current pen
        position to the top border of the glyph bitmap. This distance is
        positive for upwards y!
        """
        ...

class GlyphSlot:
    """
    FT_GlyphSlot wrapper.

    FreeType root glyph slot class structure. A glyph slot is a container where
    individual glyphs can be loaded, be they in outline or bitmap format.
    """

    _FT_GlyphSlot: _Pointer[FT_GlyphSlotRec]

    def __init__(self, slot: _Pointer[FT_GlyphSlotRec]) -> None:
        """
        Create GlyphSlot object from an FT glyph slot.

        Parameters:
        -----------
          glyph: valid FT_GlyphSlot object
        """
        ...

    def render(self, render_mode: int) -> None:
        """
        Convert a given glyph image to a bitmap. It does so by inspecting the
        glyph image format, finding the relevant renderer, and invoking it.

        :param render_mode: The render mode used to render the glyph image into
                            a bitmap. See FT_Render_Mode for a list of possible
                            values.

                            If FT_RENDER_MODE_NORMAL is used, a previous call
                            of FT_Load_Glyph with flag FT_LOAD_COLOR makes
                            FT_Render_Glyph provide a default blending of
                            colored glyph layers associated with the current
                            glyph slot (provided the font contains such layers)
                            instead of rendering the glyph slot's outline.
                            This is an experimental feature; see FT_LOAD_COLOR
                            for more information.

        **Note**:

          To get meaningful results, font scaling values must be set with
          functions like FT_Set_Char_Size before calling FT_Render_Glyph.

          When FreeType outputs a bitmap of a glyph, it really outputs an alpha
          coverage map. If a pixel is completely covered by a filled-in
          outline, the bitmap contains 0xFF at that pixel, meaning that
          0xFF/0xFF fraction of that pixel is covered, meaning the pixel is
          100% black (or 0% bright). If a pixel is only 50% covered
          (value 0x80), the pixel is made 50% black (50% bright or a middle
          shade of grey). 0% covered means 0% black (100% bright or white).

          On high-DPI screens like on smartphones and tablets, the pixels are
          so small that their chance of being completely covered and therefore
          completely black are fairly good. On the low-DPI screens, however,
          the situation is different. The pixels are too large for most of the
          details of a glyph and shades of gray are the norm rather than the
          exception.

          This is relevant because all our screens have a second problem: they
          are not linear. 1 + 1 is not 2. Twice the value does not result in
          twice the brightness. When a pixel is only 50% covered, the coverage
          map says 50% black, and this translates to a pixel value of 128 when
          you use 8 bits per channel (0-255). However, this does not translate
          to 50% brightness for that pixel on our sRGB and gamma 2.2 screens.
          Due to their non-linearity, they dwell longer in the darks and only a
          pixel value of about 186 results in 50% brightness – 128 ends up too
          dark on both bright and dark backgrounds. The net result is that dark
          text looks burnt-out, pixely and blotchy on bright background, bright
          text too frail on dark backgrounds, and colored text on colored
          background (for example, red on green) seems to have dark halos or
          ‘dirt’ around it. The situation is especially ugly for diagonal stems
          like in ‘w’ glyph shapes where the quality of FreeType's
          anti-aliasing depends on the correct display of grays. On high-DPI
          screens where smaller, fully black pixels reign supreme, this doesn't
          matter, but on our low-DPI screens with all the gray shades, it does.
          0% and 100% brightness are the same things in linear and non-linear
          space, just all the shades in-between aren't.

          The blending function for placing text over a background is

          dst = alpha * src + (1 - alpha) * dst

          which is known as the OVER operator.

          To correctly composite an anti-aliased pixel of a glyph onto a
          surface, take the foreground and background colors (e.g., in sRGB
          space) and apply gamma to get them in a linear space, use OVER to
          blend the two linear colors using the glyph pixel as the alpha value
          (remember, the glyph bitmap is an alpha coverage bitmap), and apply
          inverse gamma to the blended pixel and write it back to the image.

          Internal testing at Adobe found that a target inverse gamma of 1.8
          for step 3 gives good results across a wide range of displays with
          an sRGB gamma curve or a similar one.

          This process can cost performance. There is an approximation that
          does not need to know about the background color; see
          https://bel.fi/alankila/lcd/ and
          https://bel.fi/alankila/lcd/alpcor.html for details.

          **ATTENTION:** Linear blending is even more important when dealing
          with subpixel-rendered glyphs to prevent color-fringing! A
          subpixel-rendered glyph must first be filtered with a filter that
          gives equal weight to the three color primaries and does not exceed a
          sum of 0x100, see section ‘Subpixel Rendering’. Then the only
          difference to gray linear blending is that subpixel-rendered linear
          blending is done 3 times per pixel: red foreground subpixel to red
          background subpixel and so on for green and blue.
        """
        ...

    def get_glyph(self) -> Glyph:
        """
        A function used to extract a glyph image from a slot. Note that the
        created FT_Glyph object must be released with FT_Done_Glyph.
        """
        ...

    @property
    def bitmap(self) -> Bitmap:
        """
        This field is used as a bitmap descriptor when the slot format is
        FT_GLYPH_FORMAT_BITMAP. Note that the address and content of the
        bitmap buffer can change between calls of FT_Load_Glyph and a few
        other functions.
        """
        ...

    @property
    def metrics(self) -> GlyphMetrics:
        """
        The metrics of the last loaded glyph in the slot. The returned values
        depend on the last load flags (see the FT_Load_Glyph API function) and
        can be expressed either in 26.6 fractional pixels or font units. Note
        that even when the glyph image is transformed, the metrics are not.
        """
        ...

    @property
    def next(self) -> GlyphSlot:
        """
        In some cases (like some font tools), several glyph slots per face
        object can be a good thing. As this is rare, the glyph slots are
        listed through a direct, single-linked list using its 'next' field.
        """
        ...

    @property
    def advance(self) -> FT_Vector:
        """
        This shorthand is, depending on FT_LOAD_IGNORE_TRANSFORM, the
        transformed advance width for the glyph (in 26.6 fractional pixel
        format). As specified with FT_LOAD_VERTICAL_LAYOUT, it uses either the
        'horiAdvance' or the 'vertAdvance' value of 'metrics' field.
        """
        ...

    @property
    def outline(self) -> Outline:
        """
        The outline descriptor for the current glyph image if its format is
        FT_GLYPH_FORMAT_OUTLINE. Once a glyph is loaded, 'outline' can be
        transformed, distorted, embolded, etc. However, it must not be freed.
        """
        ...

    @property
    def format(self) -> int:
        """
        This field indicates the format of the image contained in the glyph
        slot. Typically FT_GLYPH_FORMAT_BITMAP, FT_GLYPH_FORMAT_OUTLINE,
        or FT_GLYPH_FORMAT_COMPOSITE, but others are possible.
        """
        ...

    @property
    def bitmap_top(self) -> int:
        """
        This is the bitmap's top bearing expressed in integer pixels. Remember
        that this is the distance from the baseline to the top-most glyph
        scanline, upwards y coordinates being positive.
        """
        ...

    @property
    def bitmap_left(self) -> int:
        """
        This is the bitmap's left bearing expressed in integer pixels. Of
        course, this is only valid if the format is FT_GLYPH_FORMAT_BITMAP.
        """
        ...

    @property
    def linearHoriAdvance(self) -> _Fixed:
        """
        The advance width of the unhinted glyph. Its value is expressed in
        16.16 fractional pixels, unless FT_LOAD_LINEAR_DESIGN is set when
        loading the glyph. This field can be important to perform correct
        WYSIWYG layout. Only relevant for outline glyphs.
        """
        ...

    @property
    def linearVertAdvance(self) -> _Fixed:
        """
        The advance height of the unhinted glyph. Its value is expressed in
        16.16 fractional pixels, unless FT_LOAD_LINEAR_DESIGN is set when
        loading the glyph. This field can be important to perform correct
        WYSIWYG layout. Only relevant for outline glyphs.
        """
        ...

class Face:
    """
    FT_Face wrapper

    FreeType root face class structure. A face object models a typeface in a
    font file.
    """

    _FT_Face: _Pointer[FT_FaceRec]
    _filebodys: list[bytes]
    _index: int
    _name_strings: dict[tuple[int, int, int, int], bytes]

    def __init__(self, path_or_stream: str | BinaryIO, index: int = 0) -> None:
        """
        Build a new Face

        :param Union[str, typing.BinaryIO] path_or_stream:
            A path to the font file or an io.BytesIO stream.

        :param int index:
               The index of the face within the font.
               The first face has index 0.
        """
        ...

    def _init_from_file(
        self,
        library: _FT_Library_Wrapper,
        face: _Pointer[FT_FaceRec],
        index: int,
        path: str,
    ) -> int: ...
    def _init_from_memory(
        self,
        library: _FT_Library_Wrapper,
        face: _Pointer[FT_FaceRec],
        index: int,
        byte_stream: bytes,
    ) -> int: ...
    def _init_name_string_map(self) -> None: ...
    @classmethod
    def from_bytes(cls, bytes_: bytes, index: int = 0) -> Self: ...
    def __del__(self) -> None:
        """
        Discard face object, as well as all of its child slots and sizes.
        """
        ...

    def attach_file(self, filename: str) -> None:
        """
        Attach data to a face object. Normally, this is used to read
        additional information for the face object. For example, you can attach
        an AFM file that comes with a Type 1 font to get the kerning values and
        other metrics.

        :param filename: Filename to attach

        **Note**

        The meaning of the 'attach' (i.e., what really happens when the new
        file is read) is not fixed by FreeType itself. It really depends on the
        font format (and thus the font driver).

        Client applications are expected to know what they are doing when
        invoking this function. Most drivers simply do not implement file
        attachments.
        """
        ...

    def set_char_size(
        self,
        width: _F26Dot6 = 0,
        height: _F26Dot6 = 0,
        hres: float = 72,
        vres: float = 72,
    ) -> None:
        """
        This function calls FT_Request_Size to request the nominal size (in
        points).

        :param float width: The nominal width, in 26.6 fractional points.

        :param float height: The nominal height, in 26.6 fractional points.

        :param float hres: The horizontal resolution in dpi.

        :param float vres: The vertical resolution in dpi.

        **Note**

        If either the character width or height is zero, it is set equal to the
        other value.

        If either the horizontal or vertical resolution is zero, it is set
        equal to the other value.

        A character width or height smaller than 1pt is set to 1pt; if both
        resolution values are zero, they are set to 72dpi.

        Don't use this function if you are using the FreeType cache API.
        """
        ...

    def set_pixel_sizes(self, width: int, height: int) -> None:
        """
        This function calls FT_Request_Size to request the nominal size (in
        pixels).

        :param width: The nominal width, in pixels.

        :param height: The nominal height, in pixels.
        """
        ...

    def select_charmap(self, encoding: int) -> None:
        """
        Select a given charmap by its encoding tag (as listed in 'freetype.h').

        **Note**:

          This function returns an error if no charmap in the face corresponds to
          the encoding queried here.

          Because many fonts contain more than a single cmap for Unicode
          encoding, this function has some special code to select the one which
          covers Unicode best ('best' in the sense that a UCS-4 cmap is preferred
          to a UCS-2 cmap). It is thus preferable to FT_Set_Charmap in this case.
        """
        ...

    def set_charmap(self, charmap: Charmap) -> None:
        """
        Select a given charmap for character code to glyph index mapping.

        :param charmap: A handle to the selected charmap, or an index to face->charmaps[]
        """
        ...

    def get_char_index(self, charcode: CharLike) -> int:
        """
        Return the glyph index of a given character code. This function uses a
        charmap object to do the mapping.

        :param charcode: The character code.

        **Note**:

          If you use FreeType to manipulate the contents of font files directly,
          be aware that the glyph index returned by this function doesn't always
          correspond to the internal indices used within the file. This is done
          to ensure that value 0 always corresponds to the 'missing glyph'.
        """
        ...

    def get_glyph_name(self, agindex: int, buffer_max: int = 64) -> bytes:
        """
        This function is used to return the glyph name for the given charcode.

        :param agindex: The glyph index.

        :param buffer_max: The maximum number of bytes to use to store the
            glyph name.

        :param glyph_name: The glyph name, possibly truncated.

        """
        ...

    def get_chars(self) -> Generator[tuple[int, int], Any, Any]:
        """
        This generator function is used to return all unicode character
        codes in the current charmap of a given face. For each character it
        also returns the corresponding glyph index.

        :return: character code, glyph index

        **Note**:
          Note that 'agindex' is set to 0 if the charmap is empty. The
          character code itself can be 0 in two cases: if the charmap is empty
          or if the value 0 is the first valid character code.
        """
        ...

    def get_first_char(self) -> tuple[int, int]:
        """
        This function is used to return the first character code in the current
        charmap of a given face. It also returns the corresponding glyph index.

        :return: Glyph index of first character code. 0 if charmap is empty.

        **Note**:

          You should use this function with get_next_char to be able to parse
          all character codes available in a given charmap. The code should look
          like this:

          Note that 'agindex' is set to 0 if the charmap is empty. The result
          itself can be 0 in two cases: if the charmap is empty or if the value 0
          is the first valid character code.
        """
        ...

    def get_next_char(self, charcode: int, agindex: int) -> tuple[int, int]:
        """
        This function is used to return the next character code in the current
        charmap of a given face following the value 'charcode', as well as the
        corresponding glyph index.

        :param charcode: The starting character code.

        :param agindex: Glyph index of next character code. 0 if charmap is empty.

        **Note**:

          You should use this function with FT_Get_First_Char to walk over all
          character codes available in a given charmap. See the note for this
          function for a simple code example.

          Note that 'agindex' is set to 0 when there are no more codes in the
          charmap.
        """
        ...

    def get_name_index(self, name: bytes) -> int:
        """
        Return the glyph index of a given glyph name. This function uses driver
        specific objects to do the translation.

        :param name: The glyph name.
        """
        ...

    def set_transform(self, matrix: FT_Matrix, delta: FT_Vector) -> None:
        """
        A function used to set the transformation that is applied to glyph
        images when they are loaded into a glyph slot through FT_Load_Glyph.

        :param matrix: A pointer to the transformation's 2x2 matrix.
                       Use 0 for the identity matrix.

        :parm delta: A pointer to the translation vector.
                     Use 0 for the null vector.

        **Note**:

          The transformation is only applied to scalable image formats after the
          glyph has been loaded. It means that hinting is unaltered by the
          transformation and is performed on the character size given in the last
          call to FT_Set_Char_Size or FT_Set_Pixel_Sizes.

          Note that this also transforms the 'face.glyph.advance' field, but
          not the values in 'face.glyph.metrics'.
        """
        ...

    def select_size(self, strike_index: int) -> None:
        """
        Select a bitmap strike.

        :param strike_index: The index of the bitmap strike in the
                             'available_sizes' field of Face object.
        """
        ...

    def load_glyph(self, index: int, flags: int = ...) -> None:
        """
        A function used to load a single glyph into the glyph slot of a face
        object.

        :param index: The index of the glyph in the font file. For CID-keyed
                      fonts (either in PS or in CFF format) this argument
                      specifies the CID value.

        :param flags: A flag indicating what to load for this glyph. The FT_LOAD_XXX
                      constants can be used to control the glyph loading process
                      (e.g., whether the outline should be scaled, whether to load
                      bitmaps or not, whether to hint the outline, etc).

        **Note**:

          The loaded glyph may be transformed. See FT_Set_Transform for the
          details.

          For subsetted CID-keyed fonts, 'FT_Err_Invalid_Argument' is returned
          for invalid CID values (this is, for CID values which don't have a
          corresponding glyph in the font). See the discussion of the
          FT_FACE_FLAG_CID_KEYED flag for more details.
        """
        ...

    def load_char(self, char: CharLike, flags: int = ...) -> None:
        """
        A function used to load a single glyph into the glyph slot of a face
        object, according to its character code.

        :param char: The glyph's character code, according to the current
                     charmap used in the face.

        :param flags: A flag indicating what to load for this glyph. The
                      FT_LOAD_XXX constants can be used to control the glyph
                      loading process (e.g., whether the outline should be
                      scaled, whether to load bitmaps or not, whether to hint
                      the outline, etc).

        **Note**:

          This function simply calls FT_Get_Char_Index and FT_Load_Glyph.
        """
        ...

    def get_advance(self, gindex: int, flags: int) -> int:
        """
        Retrieve the advance value of a given glyph outline in an FT_Face. By
        default, the unhinted advance is returned in font units.

        :param gindex: The glyph index.

        :param flags: A set of bit flags similar to those used when calling
                      FT_Load_Glyph, used to determine what kind of advances
                      you need.

        :return: The advance value, in either font units or 16.16 format.

                 If FT_LOAD_VERTICAL_LAYOUT is set, this is the vertical
                 advance corresponding to a vertical layout. Otherwise, it is
                 the horizontal advance in a horizontal layout.
        """
        ...

    def get_kerning(
        self, left: CharLike, right: CharLike, mode: int = ...
    ) -> FT_Vector:
        """
        Return the kerning vector between two glyphs of a same face.

        :param left: The index of the left glyph in the kern pair.

        :param right: The index of the right glyph in the kern pair.

        :param mode: See FT_Kerning_Mode for more information. Determines the scale
                     and dimension of the returned kerning vector.

        **Note**:

          Only horizontal layouts (left-to-right & right-to-left) are supported
          by this method. Other layouts, or more sophisticated kernings, are out
          of the scope of this API function -- they can be implemented through
          format-specific interfaces.
        """
        ...

    def get_format(self) -> bytes:
        """
        Return a string describing the format of a given face, using values
        which can be used as an X11 FONT_PROPERTY. Possible values are
        'TrueType', 'Type 1', 'BDF', ‘PCF', ‘Type 42', ‘CID Type 1', ‘CFF',
        'PFR', and ‘Windows FNT'.
        """
        ...

    def get_fstype(self) -> tuple[str, int]:
        """
        Return the fsType flags for a font (embedding permissions).

        The return value is a tuple containing the freetype enum name
        as a string and the actual flag as an int
        """
        ...

    @property
    def sfnt_name_count(self) -> int:
        """Number of name strings in the SFNT 'name' table."""
        ...

    def get_sfnt_name(self, index: int) -> SfntName:
        """
        Retrieve a string of the SFNT 'name' table for a given index

        :param index: The index of the 'name' string.

        **Note**:

          The 'string' array returned in the 'aname' structure is not
          null-terminated. The application should deallocate it if it is no
          longer in use.

          Use FT_Get_Sfnt_Name_Count to get the total number of available
          'name' table entries, then do a loop until you get the right
          platform, encoding, and name ID.
        """
        ...

    def get_best_name_string(
        self,
        nameID: int,
        default_string: str = "",
        preferred_order: Iterable[tuple[int, int, int]] | None = None,
    ) -> str:
        """
        Retrieve a name string given nameID. Searches available font names
        matching nameID and returns the decoded bytes of the best match.
        "Best" is defined as a preferred list of platform/encoding/languageIDs
        which can be overridden by supplying a preferred_order matching the
        scheme of 'sort_order' (see below).

        The routine will attempt to decode the string's bytes to a Python str, when the
        platform/encoding[/langID] are known (Windows, Mac, or Unicode platforms).

        If you prefer more control over name string selection and decoding than
        this routine provides:
            - call self._init_name_string_map()
            - use (nameID, platformID, encodingID, languageID) as a key into
              the self._name_strings dict
        """
        ...

    def get_variation_info(self) -> VariationSpaceInfo:
        """Retrieves variation space information for the current face."""
        ...

    def get_var_blend_coords(self) -> tuple[float, ...]:
        """Get the current blend coordinates (-1.0..+1.0)"""
        ...

    def set_var_blend_coords(
        self, coords: tuple[float, ...], reset: bool = False
    ) -> None:
        """
        Set blend coords. Using reset=True will set all axes to their default
        coordinates.
        """
        ...

    def get_var_design_coords(self) -> tuple[float, ...]:
        """Get the current design coordinates"""
        ...

    def set_var_design_coords(
        self, coords: tuple[float, ...], reset: bool = False
    ) -> None:
        """
        Set design coords. Using reset=True will set all axes to their default
        coordinates.
        """
        ...

    def set_var_named_instance(self, instance_name: str) -> None:
        """
        Set instance by name. This will work with any FreeType with variable support
        (for our purposes: v2.8.1 or later). If the actual FT_Set_Named_Instance()
        function is available (v2.9.1 or later), we use it (which, despite what you might
        expect from its name, sets instances by *index*). Otherwise we just use the coords
        of the named instance (if found) and call self.set_var_design_coords.
        """
        ...

    @property
    def postscript_name(self) -> bytes:
        """
        ASCII PostScript name of face, if available. This only works with
        PostScript and TrueType fonts.
        """
        ...

    @property
    def has_horizontal(self) -> bool:
        """
        True whenever a face object contains horizontal metrics (this is true
        for all font formats though).
        """
        ...

    @property
    def has_vertical(self) -> bool:
        """True whenever a face object contains vertical metrics."""
        ...

    @property
    def has_kerning(self) -> bool:
        """
        True whenever a face object contains kerning data that can be accessed
        with FT_Get_Kerning.
        """
        ...

    @property
    def is_scalable(self) -> bool:
        """
        true whenever a face object contains a scalable font face (true for
        TrueType, Type 1, Type 42, CID, OpenType/CFF, and PFR font formats.
        """
        ...

    @property
    def is_sfnt(self) -> bool:
        """
        true whenever a face object contains a font whose format is based on
        the SFNT storage scheme. This usually means: TrueType fonts, OpenType
        fonts, as well as SFNT-based embedded bitmap fonts.

        If this macro is true, all functions defined in FT_SFNT_NAMES_H and
        FT_TRUETYPE_TABLES_H are available.
        """
        ...

    @property
    def is_fixed_width(self) -> bool:
        """
        True whenever a face object contains a font face that contains
        fixed-width (or 'monospace', 'fixed-pitch', etc.) glyphs.
        """
        ...

    @property
    def has_fixed_sizes(self) -> bool:
        """
        True whenever a face object contains some embedded bitmaps. See the
        'available_sizes' field of the FT_FaceRec structure.
        """
        ...

    @property
    def has_glyph_names(self) -> bool:
        """
        True whenever a face object contains some glyph names that can be
        accessed through FT_Get_Glyph_Name.
        """
        ...

    @property
    def has_multiple_masters(self) -> bool:
        """
        True whenever a face object contains some multiple masters. The
        functions provided by FT_MULTIPLE_MASTERS_H are then available to
        choose the exact design you want.
        """
        ...

    @property
    def is_cid_keyed(self) -> bool:
        """
        True whenever a face object contains a CID-keyed font. See the
        discussion of FT_FACE_FLAG_CID_KEYED for more details.

        If this macro is true, all functions defined in FT_CID_H are available.
        """
        ...

    @property
    def is_tricky(self) -> bool:
        """
        True whenever a face represents a 'tricky' font. See the discussion of
        FT_FACE_FLAG_TRICKY for more details.
        """
        ...

    @property
    def num_faces(self) -> int:
        """
        The number of faces in the font file. Some font formats can have
        multiple faces in a font file.
        """
        ...

    @property
    def face_index(self) -> int:
        """
        The index of the face in the font file. It is set to 0 if there is only
        one face in the font file.
        """
        ...

    @property
    def face_flags(self) -> int:
        """
        A set of bit flags that give important information about the face; see
        FT_FACE_FLAG_XXX for the details.
        """
        ...

    @property
    def style_flags(self) -> int:
        """
        A set of bit flags indicating the style of the face; see
        FT_STYLE_FLAG_XXX for the details.
        """
        ...

    @property
    def num_glyphs(self) -> int:
        """
        The number of glyphs in the face. If the face is scalable and has sbits
        (see 'num_fixed_sizes'), it is set to the number of outline glyphs.

        For CID-keyed fonts, this value gives the highest CID used in the font.
        """
        ...

    @property
    def family_name(self) -> bytes:
        """
        The face's family name. This is an ASCII string, usually in English,
        which describes the typeface's family (like 'Times New Roman',
        'Bodoni', 'Garamond', etc). This is a least common denominator used to
        list fonts. Some formats (TrueType & OpenType) provide localized and
        Unicode versions of this string. Applications should use the format
        specific interface to access them. Can be NULL (e.g., in fonts embedded
        in a PDF file).
        """
        ...

    @property
    def style_name(self) -> bytes:
        """
        The face's style name. This is an ASCII string, usually in English,
        which describes the typeface's style (like 'Italic', 'Bold',
        'Condensed', etc). Not all font formats provide a style name, so this
        field is optional, and can be set to NULL. As for 'family_name', some
        formats provide localized and Unicode versions of this string.
        Applications should use the format specific interface to access them.
        """
        ...

    @property
    def num_fixed_sizes(self) -> int:
        """
        The number of bitmap strikes in the face. Even if the face is
        scalable, there might still be bitmap strikes, which are called
        'sbits' in that case.
        """
        ...

    @property
    def available_sizes(self) -> list[BitmapSize]:
        """
        A list of FT_Bitmap_Size for all bitmap strikes in the face. It is set
        to NULL if there is no bitmap strike.
        """
        ...

    @property
    def num_charmaps(self) -> int: ...
    @property
    def charmaps(self) -> list[Charmap]:
        """A list of the charmaps of the face."""
        ...

    @property
    def bbox(self) -> BBox:
        """
        The font bounding box. Coordinates are expressed in font units (see
        'units_per_EM'). The box is large enough to contain any glyph from the
        font. Thus, 'bbox.yMax' can be seen as the 'maximal ascender', and
        'bbox.yMin' as the 'minimal descender'. Only relevant for scalable
        formats.

        Note that the bounding box might be off by (at least) one pixel for
        hinted fonts. See FT_Size_Metrics for further discussion.
        """
        ...

    @property
    def units_per_EM(self) -> int:
        """
        The number of font units per EM square for this face. This is
        typically 2048 for TrueType fonts, and 1000 for Type 1 fonts. Only
        relevant for scalable formats.
        """
        ...

    @property
    def ascender(self) -> int:
        """
        The typographic ascender of the face, expressed in font units. For
        font formats not having this information, it is set to 'bbox.yMax'.
        Only relevant for scalable formats.
        """
        ...

    @property
    def descender(self) -> int:
        """
        The typographic descender of the face, expressed in font units. For
        font formats not having this information, it is set to 'bbox.yMin'.
        Note that this field is usually negative. Only relevant for scalable
        formats.
        """
        ...

    @property
    def height(self) -> int:
        """
        The height is the vertical distance between two consecutive baselines,
        expressed in font units. It is always positive. Only relevant for
        scalable formats.
        """
        ...

    @property
    def max_advance_width(self) -> int:
        """
        The maximal advance width, in font units, for all glyphs in this face.
        This can be used to make word wrapping computations faster. Only
        relevant for scalable formats.
        """
        ...

    @property
    def max_advance_height(self) -> int:
        """
        The maximal advance height, in font units, for all glyphs in this
        face. This is only relevant for vertical layouts, and is set to
        'height' for fonts that do not provide vertical metrics. Only relevant
        for scalable formats.
        """
        ...

    @property
    def underline_position(self) -> int:
        """
        The position, in font units, of the underline line for this face. It
        is the center of the underlining stem. Only relevant for scalable
        formats.
        """
        ...

    @property
    def underline_thickness(self) -> int:
        """
        The thickness, in font units, of the underline for this face. Only
        relevant for scalable formats.
        """
        ...

    @property
    def glyph(self) -> GlyphSlot:
        """The face's associated glyph slot(s)."""
        ...

    @property
    def size(self) -> SizeMetrics:
        """The current active size for this face."""
        ...

    @property
    def charmap(self) -> Charmap:
        """The current active charmap for this face."""
        ...

class SfntName:
    """
    SfntName wrapper

    A structure used to model an SFNT 'name' table entry.
    """

    _FT_SfntName: FT_SfntName

    def __init__(self, name: FT_SfntName) -> None:
        """
        Create a new SfntName object.

        :param name : SFNT 'name' table entry.

        """
        ...

    @property
    def platform_id(self) -> int:
        """The platform ID for 'string'."""
        ...

    @property
    def encoding_id(self) -> int:
        """The encoding ID for 'string'."""
        ...

    @property
    def language_id(self) -> int:
        """The language ID for 'string'."""
        ...

    @property
    def name_id(self) -> int:
        """An identifier for 'string'."""
        ...

    @property
    def string_len(self) -> int:
        """The length of 'string' in bytes."""
        ...

    @property
    def string(self) -> bytes:
        """
        The 'name' string. Note that its format differs depending on the
        (platform, encoding) pair. It can be a Pascal String, a UTF-16 one,
        etc.

        Generally speaking, the string is not zero-terminated. Please refer to
        the TrueType specification for details.
        """
        ...

class Stroker:
    """
    FT_Stroker wrapper

    This component generates stroked outlines of a given vectorial glyph. It
    also allows you to retrieve the 'outside' and/or the 'inside' borders of
    the stroke.

    This can be useful to generate 'bordered' glyph, i.e., glyphs displayed
    with a coloured (and anti-aliased) border around their shape.
    """

    _FT_Stroker: _Pointer[FT_StrokerRec]

    def __init__(self) -> None:
        """
        Create a new Stroker object.
        """
        ...

    def __del__(self) -> None:
        """
        Destroy object.
        """
        ...

    def set(
        self, radius: _Fixed, line_cap: int, line_join: int, miter_limit: _Fixed
    ) -> None:
        """
        Reset a stroker object's attributes.

        :param radius: The border radius.

        :param line_cap: The line cap style.

        :param line_join: The line join style.

        :param miter_limit: The miter limit for the FT_STROKER_LINEJOIN_MITER
                            style, expressed as 16.16 fixed point value.

        **Note**:

          The radius is expressed in the same units as the outline coordinates.
        """
        ...

    def rewind(self) -> None:
        """
        Reset a stroker object without changing its attributes. You should call
        this function before beginning a new series of calls to
        FT_Stroker_BeginSubPath or FT_Stroker_EndSubPath.
        """
        ...

    def parse_outline(self, outline: Outline, opened: bool) -> None:
        """
        A convenience function used to parse a whole outline with the stroker.
        The resulting outline(s) can be retrieved later by functions like
        FT_Stroker_GetCounts and FT_Stroker_Export.

        :param outline: The source outline.

        :pram opened: A boolean. If 1, the outline is treated as an open path
                      instead of a closed one.

        **Note**:

          If 'opened' is 0 (the default), the outline is treated as a closed
          path, and the stroker generates two distinct 'border' outlines.

          If 'opened' is 1, the outline is processed as an open path, and the
          stroker generates a single 'stroke' outline.

          This function calls 'rewind' automatically.
        """
        ...

    def begin_subpath(self, to: _Pointer[FT_Vector], _open: bool) -> None:
        """
        Start a new sub-path in the stroker.

        :param to: A pointer to the start vector.

        :param _open: A boolean. If 1, the sub-path is treated as an open one.

        **Note**:

          This function is useful when you need to stroke a path that is not
          stored as an 'Outline' object.
        """
        ...

    def end_subpath(self) -> None:
        """
        Close the current sub-path in the stroker.

        **Note**:

          You should call this function after 'begin_subpath'. If the subpath
          was not 'opened', this function 'draws' a single line segment to the
          start position when needed.
        """
        ...

    def line_to(self, to: _Pointer[FT_Vector]) -> None:
        """
        'Draw' a single line segment in the stroker's current sub-path, from
        the last position.

        :param to: A pointer to the destination point.

        **Note**:

          You should call this function between 'begin_subpath' and
          'end_subpath'.
        """
        ...

    def conic_to(self, control: _Pointer[FT_Vector], to: _Pointer[FT_Vector]) -> None:
        """
        'Draw' a single quadratic Bezier in the stroker's current sub-path,
        from the last position.

        :param control: A pointer to a Bezier control point.

        :param to: A pointer to the destination point.

        **Note**:

          You should call this function between 'begin_subpath' and
          'end_subpath'.
        """
        ...

    def cubic_to(
        self,
        control1: _Pointer[FT_Vector],
        control2: _Pointer[FT_Vector],
        to: _Pointer[FT_Vector],
    ) -> None:
        """
        'Draw' a single quadratic Bezier in the stroker's current sub-path,
        from the last position.

        :param control1: A pointer to the first Bezier control point.

        :param control2: A pointer to second Bezier control point.

        :param to: A pointer to the destination point.

        **Note**:

          You should call this function between 'begin_subpath' and
          'end_subpath'.
        """
        ...

    def get_border_counts(self, border: int) -> tuple[int, int]:
        """
        Call this function once you have finished parsing your paths with the
        stroker. It returns the number of points and contours necessary to
        export one of the 'border' or 'stroke' outlines generated by the
        stroker.

        :param border: The border index.

        :return: number of points, number of contours
        """
        ...

    def export_border(self, border: int, outline: Outline) -> None:
        """
        Call this function after 'get_border_counts' to export the
        corresponding border to your own 'Outline' structure.

        Note that this function appends the border points and contours to your
        outline, but does not try to resize its arrays.

        :param border:  The border index.

        :param outline: The target outline.

        **Note**:

          Always call this function after get_border_counts to get sure that
          there is enough room in your 'Outline' object to receive all new
          data.

          When an outline, or a sub-path, is 'closed', the stroker generates two
          independent 'border' outlines, named 'left' and 'right'

          When the outline, or a sub-path, is 'opened', the stroker merges the
          'border' outlines with caps. The 'left' border receives all points,
          while the 'right' border becomes empty.

          Use the function export instead if you want to retrieve all borders
          at once.
        """
        ...

    def get_counts(self) -> tuple[int, int]:
        """
        Call this function once you have finished parsing your paths with the
        stroker. It returns the number of points and contours necessary to
        export all points/borders from the stroked outline/path.

        :return: number of points, number of contours
        """
        ...

    def export(self, outline: Outline) -> None:
        """
        Call this function after get_border_counts to export all borders to
        your own 'Outline' structure.

        Note that this function appends the border points and contours to your
        outline, but does not try to resize its arrays.

        :param outline: The target outline.
        """
        ...

class VariationAxis(object):
    tag: str | None = None
    coords: tuple[float, ...] = tuple()
    name: str
    minimum: _Fixed
    default: _Fixed
    maximum: _Fixed
    strid: int

    def __init__(self, ftvaraxis: FT_Var_Axis) -> None: ...
    @override
    def __repr__(self) -> str: ...

class VariationInstance(object):
    name: str
    psname: str
    coords: tuple[_Fixed, ...]

    def __init__(self, name: str, psname: str, coords: tuple[_Fixed, ...]) -> None: ...
    @override
    def __repr__(self) -> str: ...

class VariationSpaceInfo(object):
    """
    VF info (axes & instances).
    """

    axes: tuple[VariationAxis, ...]
    instances: tuple[VariationInstance, ...]

    def __init__(self, face: Face, p_ftmmvar: _Pointer[FT_MM_Var]) -> None:
        """
        Build a VariationSpaceInfo object given face (freetype.Face) and
        p_ftmmvar (pointer to FT_MM_Var).
        """
        ...
