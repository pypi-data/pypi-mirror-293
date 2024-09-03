# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
'''
Freetype enum types
-------------------

FT_CURVE_TAGS: An enumeration type for each point on an outline to indicate
               whether it describes a point used to control a line segment
               or an arc.

FT_PIXEL_MODES: An enumeration type used to describe the format of pixels in a
                given bitmap. Note that additional formats may be added in the
                future.

FT_GLYPH_BBOX_MODES: The mode how the values of FT_Glyph_Get_CBox are returned.

FT_GLYPH_FORMATS: An enumeration type used to describe the format of a given
                  glyph image. Note that this version of FreeType only supports
                  two image formats, even though future font drivers will be
                  able to register their own format.

FT_ENCODINGS: An enumeration used to specify character sets supported by
              charmaps. Used in the FT_Select_Charmap API function.

FT_RENDER_MODES: An enumeration type that lists the render modes supported by
                 FreeType 2. Each mode corresponds to a specific type of
                 scanline conversion performed on the outline.

FT_LOAD_TARGETS: A list of values that are used to select a specific hinting
                 algorithm to use by the hinter. You should OR one of these
                 values to your 'load_flags' when calling FT_Load_Glyph.

FT_LOAD_FLAGS: A list of bit-field constants used with FT_Load_Glyph to
               indicate what kind of operations to perform during glyph
               loading.

FT_STYLE_FLAGS: A list of bit-flags used to indicate the style of a given
                face. These are used in the 'style_flags' field of FT_FaceRec.

FT_FSTYPES: A list of bit flags that inform client applications of embedding
            and subsetting restrictions associated with a font.

FT_FACE_FLAGS: A list of bit flags used in the 'face_flags' field of the
               FT_FaceRec structure. They inform client applications of
               properties of the corresponding face.

FT_OUTLINE_FLAGS: A list of bit-field constants use for the flags in an
                  outline's 'flags' field.

FT_OPEN_MODES: A list of bit-field constants used within the 'flags' field of
               the FT_Open_Args structure.

FT_KERNING_MODES: An enumeration used to specify which kerning values to return
                  in FT_Get_Kerning.

FT_STROKER_LINEJOINS: These values determine how two joining lines are rendered
                      in a stroker.

FT_STROKER_LINECAPS: These values determine how the end of opened sub-paths are
                     rendered in a stroke.

FT_STROKER_BORDERS: These values are used to select a given stroke border in
                    FT_Stroker_GetBorderCounts and FT_Stroker_ExportBorder.

FT_LCD_FILTERS: A list of values to identify various types of LCD filters.

TT_PLATFORMS: A list of valid values for the 'platform_id' identifier code in
              FT_CharMapRec and FT_SfntName structures.

TT_APPLE_IDS: A list of valid values for the 'encoding_id' for
              TT_PLATFORM_APPLE_UNICODE charmaps and name entries.

TT_MAC_IDS: A list of valid values for the 'encoding_id' for
            TT_PLATFORM_MACINTOSH charmaps and name entries.

TT_MS_IDS: A list of valid values for the 'encoding_id' for
           TT_PLATFORM_MICROSOFT charmaps and name entries.

TT_ADOBE_IDS: A list of valid values for the 'encoding_id' for
              TT_PLATFORM_ADOBE charmaps. This is a FreeType-specific
              extension!

TT_MAC_LANGIDS: Possible values of the language identifier field in the name
                records of the TTF `name' table if the `platform' identifier
                code is TT_PLATFORM_MACINTOSH.

TT_MS_LANGIDS: Possible values of the language identifier field in the name
               records of the TTF `name' table if the `platform' identifier
               code is TT_PLATFORM_MICROSOFT.

TT_NAME_IDS: Possible values of the `name' identifier field in the name
             records of the TTF `name' table.  These values are platform
             independent.
'''
from .ft_color_root_transform import (
    FT_COLOR_INCLUDE_ROOT_TRANSFORM as FT_COLOR_INCLUDE_ROOT_TRANSFORM,
)
from .ft_color_root_transform import (
    FT_COLOR_NO_ROOT_TRANSFORM as FT_COLOR_NO_ROOT_TRANSFORM,
)
from .ft_color_root_transform import (
    FT_COLOR_ROOT_TRANSFORM_MAX as FT_COLOR_ROOT_TRANSFORM_MAX,
)
from .ft_color_root_transform import FT_Color_Root_Transform as FT_Color_Root_Transform
from .ft_curve_tags import FT_CURVE_TAG as FT_CURVE_TAG
from .ft_curve_tags import FT_CURVE_TAG_CONIC as FT_CURVE_TAG_CONIC
from .ft_curve_tags import FT_CURVE_TAG_CUBIC as FT_CURVE_TAG_CUBIC
from .ft_curve_tags import FT_CURVE_TAG_ON as FT_CURVE_TAG_ON
from .ft_curve_tags import FT_CURVE_TAGS as FT_CURVE_TAGS
from .ft_curve_tags import FT_Curve_Tag as FT_Curve_Tag
from .ft_curve_tags import FT_Curve_Tag_Conic as FT_Curve_Tag_Conic
from .ft_curve_tags import FT_Curve_Tag_Cubic as FT_Curve_Tag_Cubic
from .ft_curve_tags import FT_Curve_Tag_On as FT_Curve_Tag_On
from .ft_encodings import FT_ENCODING_ADOBE_CUSTOM as FT_ENCODING_ADOBE_CUSTOM
from .ft_encodings import FT_ENCODING_ADOBE_EXPERT as FT_ENCODING_ADOBE_EXPERT
from .ft_encodings import FT_ENCODING_ADOBE_LATIN1 as FT_ENCODING_ADOBE_LATIN1
from .ft_encodings import FT_ENCODING_ADOBE_STANDARD as FT_ENCODING_ADOBE_STANDARD
from .ft_encodings import FT_ENCODING_APPLE_ROMAN as FT_ENCODING_APPLE_ROMAN
from .ft_encodings import FT_ENCODING_BIG5 as FT_ENCODING_BIG5
from .ft_encodings import FT_ENCODING_JOHAB as FT_ENCODING_JOHAB
from .ft_encodings import FT_ENCODING_MS_SYMBOL as FT_ENCODING_MS_SYMBOL
from .ft_encodings import FT_ENCODING_NONE as FT_ENCODING_NONE
from .ft_encodings import FT_ENCODING_OLD_LATIN2 as FT_ENCODING_OLD_LATIN2
from .ft_encodings import FT_ENCODING_PRC as FT_ENCODING_PRC
from .ft_encodings import FT_ENCODING_SJIS as FT_ENCODING_SJIS
from .ft_encodings import FT_ENCODING_UNICODE as FT_ENCODING_UNICODE
from .ft_encodings import FT_ENCODING_WANSUNG as FT_ENCODING_WANSUNG
from .ft_encodings import FT_ENCODINGS as FT_ENCODINGS
from .ft_face_flags import FT_FACE_FLAG_CID_KEYED as FT_FACE_FLAG_CID_KEYED
from .ft_face_flags import FT_FACE_FLAG_EXTERNAL_STREAM as FT_FACE_FLAG_EXTERNAL_STREAM
from .ft_face_flags import FT_FACE_FLAG_FAST_GLYPHS as FT_FACE_FLAG_FAST_GLYPHS
from .ft_face_flags import FT_FACE_FLAG_FIXED_SIZES as FT_FACE_FLAG_FIXED_SIZES
from .ft_face_flags import FT_FACE_FLAG_FIXED_WIDTH as FT_FACE_FLAG_FIXED_WIDTH
from .ft_face_flags import FT_FACE_FLAG_GLYPH_NAMES as FT_FACE_FLAG_GLYPH_NAMES
from .ft_face_flags import FT_FACE_FLAG_HINTER as FT_FACE_FLAG_HINTER
from .ft_face_flags import FT_FACE_FLAG_HORIZONTAL as FT_FACE_FLAG_HORIZONTAL
from .ft_face_flags import FT_FACE_FLAG_KERNING as FT_FACE_FLAG_KERNING
from .ft_face_flags import (
    FT_FACE_FLAG_MULTIPLE_MASTERS as FT_FACE_FLAG_MULTIPLE_MASTERS,
)
from .ft_face_flags import FT_FACE_FLAG_SCALABLE as FT_FACE_FLAG_SCALABLE
from .ft_face_flags import FT_FACE_FLAG_SFNT as FT_FACE_FLAG_SFNT
from .ft_face_flags import FT_FACE_FLAG_TRICKY as FT_FACE_FLAG_TRICKY
from .ft_face_flags import FT_FACE_FLAG_VERTICAL as FT_FACE_FLAG_VERTICAL
from .ft_face_flags import FT_FACE_FLAGS as FT_FACE_FLAGS
from .ft_fstypes import (
    FT_FSTYPE_BITMAP_EMBEDDING_ONLY as FT_FSTYPE_BITMAP_EMBEDDING_ONLY,
)
from .ft_fstypes import FT_FSTYPE_EDITABLE_EMBEDDING as FT_FSTYPE_EDITABLE_EMBEDDING
from .ft_fstypes import (
    FT_FSTYPE_INSTALLABLE_EMBEDDING as FT_FSTYPE_INSTALLABLE_EMBEDDING,
)
from .ft_fstypes import FT_FSTYPE_NO_SUBSETTING as FT_FSTYPE_NO_SUBSETTING
from .ft_fstypes import (
    FT_FSTYPE_PREVIEW_AND_PRINT_EMBEDDING as FT_FSTYPE_PREVIEW_AND_PRINT_EMBEDDING,
)
from .ft_fstypes import (
    FT_FSTYPE_RESTRICTED_LICENSE_EMBEDDING as FT_FSTYPE_RESTRICTED_LICENSE_EMBEDDING,
)
from .ft_fstypes import FT_FSTYPES as FT_FSTYPES
from .ft_fstypes import (
    ft_fstype_bitmap_embedding_only as ft_fstype_bitmap_embedding_only,
)
from .ft_fstypes import ft_fstype_editable_embedding as ft_fstype_editable_embedding
from .ft_fstypes import (
    ft_fstype_installable_embedding as ft_fstype_installable_embedding,
)
from .ft_fstypes import ft_fstype_no_subsetting as ft_fstype_no_subsetting
from .ft_fstypes import (
    ft_fstype_preview_and_print_embedding as ft_fstype_preview_and_print_embedding,
)
from .ft_fstypes import (
    ft_fstype_restricted_license_embedding as ft_fstype_restricted_license_embedding,
)
from .ft_glyph_bbox_modes import FT_GLYPH_BBOX_GRIDFIT as FT_GLYPH_BBOX_GRIDFIT
from .ft_glyph_bbox_modes import FT_GLYPH_BBOX_MODES as FT_GLYPH_BBOX_MODES
from .ft_glyph_bbox_modes import FT_GLYPH_BBOX_PIXELS as FT_GLYPH_BBOX_PIXELS
from .ft_glyph_bbox_modes import FT_GLYPH_BBOX_SUBPIXELS as FT_GLYPH_BBOX_SUBPIXELS
from .ft_glyph_bbox_modes import FT_GLYPH_BBOX_TRUNCATE as FT_GLYPH_BBOX_TRUNCATE
from .ft_glyph_bbox_modes import FT_GLYPH_BBOX_UNSCALED as FT_GLYPH_BBOX_UNSCALED
from .ft_glyph_formats import FT_GLYPH_FORMAT_BITMAP as FT_GLYPH_FORMAT_BITMAP
from .ft_glyph_formats import FT_GLYPH_FORMAT_COMPOSITE as FT_GLYPH_FORMAT_COMPOSITE
from .ft_glyph_formats import FT_GLYPH_FORMAT_NONE as FT_GLYPH_FORMAT_NONE
from .ft_glyph_formats import FT_GLYPH_FORMAT_OUTLINE as FT_GLYPH_FORMAT_OUTLINE
from .ft_glyph_formats import FT_GLYPH_FORMAT_PLOTTER as FT_GLYPH_FORMAT_PLOTTER
from .ft_glyph_formats import FT_GLYPH_FORMAT_SVG as FT_GLYPH_FORMAT_SVG
from .ft_glyph_formats import FT_GLYPH_FORMATS as FT_GLYPH_FORMATS
from .ft_glyph_formats import ft_glyph_format_bitmap as ft_glyph_format_bitmap
from .ft_glyph_formats import ft_glyph_format_composite as ft_glyph_format_composite
from .ft_glyph_formats import ft_glyph_format_none as ft_glyph_format_none
from .ft_glyph_formats import ft_glyph_format_outline as ft_glyph_format_outline
from .ft_glyph_formats import ft_glyph_format_plotter as ft_glyph_format_plotter
from .ft_glyph_formats import ft_glyph_format_svg as ft_glyph_format_svg
from .ft_kerning_modes import FT_KERNING_DEFAULT as FT_KERNING_DEFAULT
from .ft_kerning_modes import FT_KERNING_MODES as FT_KERNING_MODES
from .ft_kerning_modes import FT_KERNING_UNFITTED as FT_KERNING_UNFITTED
from .ft_kerning_modes import FT_KERNING_UNSCALED as FT_KERNING_UNSCALED
from .ft_lcd_filters import FT_LCD_FILTER_DEFAULT as FT_LCD_FILTER_DEFAULT
from .ft_lcd_filters import FT_LCD_FILTER_LEGACY as FT_LCD_FILTER_LEGACY
from .ft_lcd_filters import FT_LCD_FILTER_LIGHT as FT_LCD_FILTER_LIGHT
from .ft_lcd_filters import FT_LCD_FILTER_NONE as FT_LCD_FILTER_NONE
from .ft_lcd_filters import FT_LCD_FILTERS as FT_LCD_FILTERS
from .ft_load_flags import FT_LOAD_ADVANCE_ONLY as FT_LOAD_ADVANCE_ONLY
from .ft_load_flags import FT_LOAD_BITMAP_METRICS_ONLY as FT_LOAD_BITMAP_METRICS_ONLY
from .ft_load_flags import FT_LOAD_COLOR as FT_LOAD_COLOR
from .ft_load_flags import FT_LOAD_COMPUTE_METRICS as FT_LOAD_COMPUTE_METRICS
from .ft_load_flags import FT_LOAD_CROP_BITMAP as FT_LOAD_CROP_BITMAP
from .ft_load_flags import FT_LOAD_DEFAULT as FT_LOAD_DEFAULT
from .ft_load_flags import FT_LOAD_FLAGS as FT_LOAD_FLAGS
from .ft_load_flags import FT_LOAD_FORCE_AUTOHINT as FT_LOAD_FORCE_AUTOHINT
from .ft_load_flags import (
    FT_LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH as FT_LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH,
)
from .ft_load_flags import FT_LOAD_IGNORE_TRANSFORM as FT_LOAD_IGNORE_TRANSFORM
from .ft_load_flags import FT_LOAD_LINEAR_DESIGN as FT_LOAD_LINEAR_DESIGN
from .ft_load_flags import FT_LOAD_MONOCHROME as FT_LOAD_MONOCHROME
from .ft_load_flags import FT_LOAD_NO_AUTOHINT as FT_LOAD_NO_AUTOHINT
from .ft_load_flags import FT_LOAD_NO_BITMAP as FT_LOAD_NO_BITMAP
from .ft_load_flags import FT_LOAD_NO_HINTING as FT_LOAD_NO_HINTING
from .ft_load_flags import FT_LOAD_NO_RECURSE as FT_LOAD_NO_RECURSE
from .ft_load_flags import FT_LOAD_NO_SCALE as FT_LOAD_NO_SCALE
from .ft_load_flags import FT_LOAD_NO_SVG as FT_LOAD_NO_SVG
from .ft_load_flags import FT_LOAD_PEDANTIC as FT_LOAD_PEDANTIC
from .ft_load_flags import FT_LOAD_RENDER as FT_LOAD_RENDER
from .ft_load_flags import FT_LOAD_SBITS_ONLY as FT_LOAD_SBITS_ONLY
from .ft_load_flags import FT_LOAD_VERTICAL_LAYOUT as FT_LOAD_VERTICAL_LAYOUT
from .ft_load_targets import FT_LOAD_TARGET_LCD as FT_LOAD_TARGET_LCD
from .ft_load_targets import FT_LOAD_TARGET_LCD_V as FT_LOAD_TARGET_LCD_V
from .ft_load_targets import FT_LOAD_TARGET_LIGHT as FT_LOAD_TARGET_LIGHT
from .ft_load_targets import FT_LOAD_TARGET_MONO as FT_LOAD_TARGET_MONO
from .ft_load_targets import FT_LOAD_TARGET_NORMAL as FT_LOAD_TARGET_NORMAL
from .ft_load_targets import FT_LOAD_TARGETS as FT_LOAD_TARGETS
from .ft_open_modes import FT_OPEN_DRIVER as FT_OPEN_DRIVER
from .ft_open_modes import FT_OPEN_MEMORY as FT_OPEN_MEMORY
from .ft_open_modes import FT_OPEN_MODES as FT_OPEN_MODES
from .ft_open_modes import FT_OPEN_PARAMS as FT_OPEN_PARAMS
from .ft_open_modes import FT_OPEN_PATHNAME as FT_OPEN_PATHNAME
from .ft_open_modes import FT_OPEN_STREAM as FT_OPEN_STREAM
from .ft_outline_flags import FT_OUTLINE_EVEN_ODD_FILL as FT_OUTLINE_EVEN_ODD_FILL
from .ft_outline_flags import FT_OUTLINE_FLAGS as FT_OUTLINE_FLAGS
from .ft_outline_flags import FT_OUTLINE_HIGH_PRECISION as FT_OUTLINE_HIGH_PRECISION
from .ft_outline_flags import FT_OUTLINE_IGNORE_DROPOUTS as FT_OUTLINE_IGNORE_DROPOUTS
from .ft_outline_flags import FT_OUTLINE_INCLUDE_STUBS as FT_OUTLINE_INCLUDE_STUBS
from .ft_outline_flags import FT_OUTLINE_NONE as FT_OUTLINE_NONE
from .ft_outline_flags import FT_OUTLINE_OWNER as FT_OUTLINE_OWNER
from .ft_outline_flags import FT_OUTLINE_REVERSE_FILL as FT_OUTLINE_REVERSE_FILL
from .ft_outline_flags import FT_OUTLINE_SINGLE_PASS as FT_OUTLINE_SINGLE_PASS
from .ft_outline_flags import FT_OUTLINE_SMART_DROPOUTS as FT_OUTLINE_SMART_DROPOUTS
from .ft_pixel_modes import FT_PIXEL_MODE_BGRA as FT_PIXEL_MODE_BGRA
from .ft_pixel_modes import FT_PIXEL_MODE_GRAY as FT_PIXEL_MODE_GRAY
from .ft_pixel_modes import FT_PIXEL_MODE_GRAY2 as FT_PIXEL_MODE_GRAY2
from .ft_pixel_modes import FT_PIXEL_MODE_GRAY4 as FT_PIXEL_MODE_GRAY4
from .ft_pixel_modes import FT_PIXEL_MODE_LCD as FT_PIXEL_MODE_LCD
from .ft_pixel_modes import FT_PIXEL_MODE_LCD_V as FT_PIXEL_MODE_LCD_V
from .ft_pixel_modes import FT_PIXEL_MODE_MAX as FT_PIXEL_MODE_MAX
from .ft_pixel_modes import FT_PIXEL_MODE_MONO as FT_PIXEL_MODE_MONO
from .ft_pixel_modes import FT_PIXEL_MODE_NONE as FT_PIXEL_MODE_NONE
from .ft_pixel_modes import FT_PIXEL_MODES as FT_PIXEL_MODES
from .ft_pixel_modes import ft_pixel_mode_grays as ft_pixel_mode_grays
from .ft_pixel_modes import ft_pixel_mode_mono as ft_pixel_mode_mono
from .ft_pixel_modes import ft_pixel_mode_none as ft_pixel_mode_none
from .ft_pixel_modes import ft_pixel_mode_pal2 as ft_pixel_mode_pal2
from .ft_pixel_modes import ft_pixel_mode_pal4 as ft_pixel_mode_pal4
from .ft_render_modes import FT_RENDER_MODE_LCD as FT_RENDER_MODE_LCD
from .ft_render_modes import FT_RENDER_MODE_LCD_V as FT_RENDER_MODE_LCD_V
from .ft_render_modes import FT_RENDER_MODE_LIGHT as FT_RENDER_MODE_LIGHT
from .ft_render_modes import FT_RENDER_MODE_MONO as FT_RENDER_MODE_MONO
from .ft_render_modes import FT_RENDER_MODE_NORMAL as FT_RENDER_MODE_NORMAL
from .ft_render_modes import FT_RENDER_MODE_SDF as FT_RENDER_MODE_SDF
from .ft_render_modes import FT_RENDER_MODES as FT_RENDER_MODES
from .ft_stroker_borders import FT_STROKER_BORDER_LEFT as FT_STROKER_BORDER_LEFT
from .ft_stroker_borders import FT_STROKER_BORDER_RIGHT as FT_STROKER_BORDER_RIGHT
from .ft_stroker_borders import FT_STROKER_BORDERS as FT_STROKER_BORDERS
from .ft_stroker_linecaps import FT_STROKER_LINECAP_BUTT as FT_STROKER_LINECAP_BUTT
from .ft_stroker_linecaps import FT_STROKER_LINECAP_ROUND as FT_STROKER_LINECAP_ROUND
from .ft_stroker_linecaps import FT_STROKER_LINECAP_SQUARE as FT_STROKER_LINECAP_SQUARE
from .ft_stroker_linecaps import FT_STROKER_LINECAPS as FT_STROKER_LINECAPS
from .ft_stroker_linejoins import FT_STROKER_LINEJOIN_BEVEL as FT_STROKER_LINEJOIN_BEVEL
from .ft_stroker_linejoins import FT_STROKER_LINEJOIN_MITER as FT_STROKER_LINEJOIN_MITER
from .ft_stroker_linejoins import FT_STROKER_LINEJOIN_ROUND as FT_STROKER_LINEJOIN_ROUND
from .ft_stroker_linejoins import FT_STROKER_LINEJOINS as FT_STROKER_LINEJOINS
from .ft_style_flags import FT_STYLE_FLAG_BOLD as FT_STYLE_FLAG_BOLD
from .ft_style_flags import FT_STYLE_FLAG_ITALIC as FT_STYLE_FLAG_ITALIC
from .ft_style_flags import FT_STYLE_FLAGS as FT_STYLE_FLAGS
from .tt_adobe_ids import TT_ADOBE_ID_CUSTOM as TT_ADOBE_ID_CUSTOM
from .tt_adobe_ids import TT_ADOBE_ID_EXPERT as TT_ADOBE_ID_EXPERT
from .tt_adobe_ids import TT_ADOBE_ID_LATIN_1 as TT_ADOBE_ID_LATIN_1
from .tt_adobe_ids import TT_ADOBE_ID_STANDARD as TT_ADOBE_ID_STANDARD
from .tt_adobe_ids import TT_ADOBE_IDS as TT_ADOBE_IDS
from .tt_apple_ids import TT_APPLE_ID_DEFAULT as TT_APPLE_ID_DEFAULT
from .tt_apple_ids import TT_APPLE_ID_ISO_10646 as TT_APPLE_ID_ISO_10646
from .tt_apple_ids import TT_APPLE_ID_UNICODE_1_1 as TT_APPLE_ID_UNICODE_1_1
from .tt_apple_ids import TT_APPLE_ID_UNICODE_2_0 as TT_APPLE_ID_UNICODE_2_0
from .tt_apple_ids import TT_APPLE_ID_UNICODE_32 as TT_APPLE_ID_UNICODE_32
from .tt_apple_ids import TT_APPLE_ID_VARIANT_SELECTOR as TT_APPLE_ID_VARIANT_SELECTOR
from .tt_apple_ids import TT_APPLE_IDS as TT_APPLE_IDS
from .tt_mac_ids import TT_MAC_ID_ARABIC as TT_MAC_ID_ARABIC
from .tt_mac_ids import TT_MAC_ID_ARMENIAN as TT_MAC_ID_ARMENIAN
from .tt_mac_ids import TT_MAC_ID_BENGALI as TT_MAC_ID_BENGALI
from .tt_mac_ids import TT_MAC_ID_BURMESE as TT_MAC_ID_BURMESE
from .tt_mac_ids import TT_MAC_ID_DEVANAGARI as TT_MAC_ID_DEVANAGARI
from .tt_mac_ids import TT_MAC_ID_GEEZ as TT_MAC_ID_GEEZ
from .tt_mac_ids import TT_MAC_ID_GEORGIAN as TT_MAC_ID_GEORGIAN
from .tt_mac_ids import TT_MAC_ID_GREEK as TT_MAC_ID_GREEK
from .tt_mac_ids import TT_MAC_ID_GUJARATI as TT_MAC_ID_GUJARATI
from .tt_mac_ids import TT_MAC_ID_GURMUKHI as TT_MAC_ID_GURMUKHI
from .tt_mac_ids import TT_MAC_ID_HEBREW as TT_MAC_ID_HEBREW
from .tt_mac_ids import TT_MAC_ID_JAPANESE as TT_MAC_ID_JAPANESE
from .tt_mac_ids import TT_MAC_ID_KANNADA as TT_MAC_ID_KANNADA
from .tt_mac_ids import TT_MAC_ID_KHMER as TT_MAC_ID_KHMER
from .tt_mac_ids import TT_MAC_ID_KOREAN as TT_MAC_ID_KOREAN
from .tt_mac_ids import TT_MAC_ID_LAOTIAN as TT_MAC_ID_LAOTIAN
from .tt_mac_ids import TT_MAC_ID_MALAYALAM as TT_MAC_ID_MALAYALAM
from .tt_mac_ids import TT_MAC_ID_MALDIVIAN as TT_MAC_ID_MALDIVIAN
from .tt_mac_ids import TT_MAC_ID_MONGOLIAN as TT_MAC_ID_MONGOLIAN
from .tt_mac_ids import TT_MAC_ID_ORIYA as TT_MAC_ID_ORIYA
from .tt_mac_ids import TT_MAC_ID_ROMAN as TT_MAC_ID_ROMAN
from .tt_mac_ids import TT_MAC_ID_RSYMBOL as TT_MAC_ID_RSYMBOL
from .tt_mac_ids import TT_MAC_ID_RUSSIAN as TT_MAC_ID_RUSSIAN
from .tt_mac_ids import TT_MAC_ID_SIMPLIFIED_CHINESE as TT_MAC_ID_SIMPLIFIED_CHINESE
from .tt_mac_ids import TT_MAC_ID_SINDHI as TT_MAC_ID_SINDHI
from .tt_mac_ids import TT_MAC_ID_SINHALESE as TT_MAC_ID_SINHALESE
from .tt_mac_ids import TT_MAC_ID_SLAVIC as TT_MAC_ID_SLAVIC
from .tt_mac_ids import TT_MAC_ID_TAMIL as TT_MAC_ID_TAMIL
from .tt_mac_ids import TT_MAC_ID_TELUGU as TT_MAC_ID_TELUGU
from .tt_mac_ids import TT_MAC_ID_THAI as TT_MAC_ID_THAI
from .tt_mac_ids import TT_MAC_ID_TIBETAN as TT_MAC_ID_TIBETAN
from .tt_mac_ids import TT_MAC_ID_TRADITIONAL_CHINESE as TT_MAC_ID_TRADITIONAL_CHINESE
from .tt_mac_ids import TT_MAC_ID_UNINTERP as TT_MAC_ID_UNINTERP
from .tt_mac_ids import TT_MAC_ID_VIETNAMESE as TT_MAC_ID_VIETNAMESE
from .tt_mac_ids import TT_MAC_IDS as TT_MAC_IDS
from .tt_mac_langids import TT_MAC_LANGID_AFRIKAANS as TT_MAC_LANGID_AFRIKAANS
from .tt_mac_langids import TT_MAC_LANGID_ALBANIAN as TT_MAC_LANGID_ALBANIAN
from .tt_mac_langids import TT_MAC_LANGID_AMHARIC as TT_MAC_LANGID_AMHARIC
from .tt_mac_langids import TT_MAC_LANGID_ARABIC as TT_MAC_LANGID_ARABIC
from .tt_mac_langids import TT_MAC_LANGID_ARMENIAN as TT_MAC_LANGID_ARMENIAN
from .tt_mac_langids import TT_MAC_LANGID_ASSAMESE as TT_MAC_LANGID_ASSAMESE
from .tt_mac_langids import TT_MAC_LANGID_AYMARA as TT_MAC_LANGID_AYMARA
from .tt_mac_langids import TT_MAC_LANGID_AZERBAIJANI as TT_MAC_LANGID_AZERBAIJANI
from .tt_mac_langids import (
    TT_MAC_LANGID_AZERBAIJANI_ARABIC_SCRIPT as TT_MAC_LANGID_AZERBAIJANI_ARABIC_SCRIPT,
)
from .tt_mac_langids import (
    TT_MAC_LANGID_AZERBAIJANI_CYRILLIC_SCRIPT as TT_MAC_LANGID_AZERBAIJANI_CYRILLIC_SCRIPT,
)
from .tt_mac_langids import (
    TT_MAC_LANGID_AZERBAIJANI_ROMAN_SCRIPT as TT_MAC_LANGID_AZERBAIJANI_ROMAN_SCRIPT,
)
from .tt_mac_langids import TT_MAC_LANGID_BASQUE as TT_MAC_LANGID_BASQUE
from .tt_mac_langids import TT_MAC_LANGID_BENGALI as TT_MAC_LANGID_BENGALI
from .tt_mac_langids import TT_MAC_LANGID_BRETON as TT_MAC_LANGID_BRETON
from .tt_mac_langids import TT_MAC_LANGID_BULGARIAN as TT_MAC_LANGID_BULGARIAN
from .tt_mac_langids import TT_MAC_LANGID_BURMESE as TT_MAC_LANGID_BURMESE
from .tt_mac_langids import TT_MAC_LANGID_BYELORUSSIAN as TT_MAC_LANGID_BYELORUSSIAN
from .tt_mac_langids import TT_MAC_LANGID_CATALAN as TT_MAC_LANGID_CATALAN
from .tt_mac_langids import TT_MAC_LANGID_CHEWA as TT_MAC_LANGID_CHEWA
from .tt_mac_langids import (
    TT_MAC_LANGID_CHINESE_SIMPLIFIED as TT_MAC_LANGID_CHINESE_SIMPLIFIED,
)
from .tt_mac_langids import (
    TT_MAC_LANGID_CHINESE_TRADITIONAL as TT_MAC_LANGID_CHINESE_TRADITIONAL,
)
from .tt_mac_langids import TT_MAC_LANGID_CROATIAN as TT_MAC_LANGID_CROATIAN
from .tt_mac_langids import TT_MAC_LANGID_CZECH as TT_MAC_LANGID_CZECH
from .tt_mac_langids import TT_MAC_LANGID_DANISH as TT_MAC_LANGID_DANISH
from .tt_mac_langids import TT_MAC_LANGID_DUTCH as TT_MAC_LANGID_DUTCH
from .tt_mac_langids import TT_MAC_LANGID_DZONGKHA as TT_MAC_LANGID_DZONGKHA
from .tt_mac_langids import TT_MAC_LANGID_ENGLISH as TT_MAC_LANGID_ENGLISH
from .tt_mac_langids import TT_MAC_LANGID_ESPERANTO as TT_MAC_LANGID_ESPERANTO
from .tt_mac_langids import TT_MAC_LANGID_ESTONIAN as TT_MAC_LANGID_ESTONIAN
from .tt_mac_langids import TT_MAC_LANGID_FAEROESE as TT_MAC_LANGID_FAEROESE
from .tt_mac_langids import TT_MAC_LANGID_FARSI as TT_MAC_LANGID_FARSI
from .tt_mac_langids import TT_MAC_LANGID_FINNISH as TT_MAC_LANGID_FINNISH
from .tt_mac_langids import TT_MAC_LANGID_FLEMISH as TT_MAC_LANGID_FLEMISH
from .tt_mac_langids import TT_MAC_LANGID_FRENCH as TT_MAC_LANGID_FRENCH
from .tt_mac_langids import TT_MAC_LANGID_GALICIAN as TT_MAC_LANGID_GALICIAN
from .tt_mac_langids import TT_MAC_LANGID_GALLA as TT_MAC_LANGID_GALLA
from .tt_mac_langids import TT_MAC_LANGID_GEORGIAN as TT_MAC_LANGID_GEORGIAN
from .tt_mac_langids import TT_MAC_LANGID_GERMAN as TT_MAC_LANGID_GERMAN
from .tt_mac_langids import TT_MAC_LANGID_GREEK as TT_MAC_LANGID_GREEK
from .tt_mac_langids import (
    TT_MAC_LANGID_GREEK_POLYTONIC as TT_MAC_LANGID_GREEK_POLYTONIC,
)
from .tt_mac_langids import TT_MAC_LANGID_GREELANDIC as TT_MAC_LANGID_GREELANDIC
from .tt_mac_langids import TT_MAC_LANGID_GUARANI as TT_MAC_LANGID_GUARANI
from .tt_mac_langids import TT_MAC_LANGID_GUJARATI as TT_MAC_LANGID_GUJARATI
from .tt_mac_langids import TT_MAC_LANGID_HEBREW as TT_MAC_LANGID_HEBREW
from .tt_mac_langids import TT_MAC_LANGID_HINDI as TT_MAC_LANGID_HINDI
from .tt_mac_langids import TT_MAC_LANGID_HUNGARIAN as TT_MAC_LANGID_HUNGARIAN
from .tt_mac_langids import TT_MAC_LANGID_ICELANDIC as TT_MAC_LANGID_ICELANDIC
from .tt_mac_langids import TT_MAC_LANGID_INDONESIAN as TT_MAC_LANGID_INDONESIAN
from .tt_mac_langids import TT_MAC_LANGID_INUKTITUT as TT_MAC_LANGID_INUKTITUT
from .tt_mac_langids import TT_MAC_LANGID_IRISH as TT_MAC_LANGID_IRISH
from .tt_mac_langids import TT_MAC_LANGID_IRISH_GAELIC as TT_MAC_LANGID_IRISH_GAELIC
from .tt_mac_langids import TT_MAC_LANGID_ITALIAN as TT_MAC_LANGID_ITALIAN
from .tt_mac_langids import TT_MAC_LANGID_JAPANESE as TT_MAC_LANGID_JAPANESE
from .tt_mac_langids import TT_MAC_LANGID_JAVANESE as TT_MAC_LANGID_JAVANESE
from .tt_mac_langids import TT_MAC_LANGID_KANNADA as TT_MAC_LANGID_KANNADA
from .tt_mac_langids import TT_MAC_LANGID_KASHMIRI as TT_MAC_LANGID_KASHMIRI
from .tt_mac_langids import TT_MAC_LANGID_KAZAKH as TT_MAC_LANGID_KAZAKH
from .tt_mac_langids import TT_MAC_LANGID_KHMER as TT_MAC_LANGID_KHMER
from .tt_mac_langids import TT_MAC_LANGID_KIRGHIZ as TT_MAC_LANGID_KIRGHIZ
from .tt_mac_langids import TT_MAC_LANGID_KOREAN as TT_MAC_LANGID_KOREAN
from .tt_mac_langids import TT_MAC_LANGID_KURDISH as TT_MAC_LANGID_KURDISH
from .tt_mac_langids import TT_MAC_LANGID_LAO as TT_MAC_LANGID_LAO
from .tt_mac_langids import TT_MAC_LANGID_LATIN as TT_MAC_LANGID_LATIN
from .tt_mac_langids import TT_MAC_LANGID_LETTISH as TT_MAC_LANGID_LETTISH
from .tt_mac_langids import TT_MAC_LANGID_LITHUANIAN as TT_MAC_LANGID_LITHUANIAN
from .tt_mac_langids import TT_MAC_LANGID_MACEDONIAN as TT_MAC_LANGID_MACEDONIAN
from .tt_mac_langids import TT_MAC_LANGID_MALAGASY as TT_MAC_LANGID_MALAGASY
from .tt_mac_langids import (
    TT_MAC_LANGID_MALAY_ARABIC_SCRIPT as TT_MAC_LANGID_MALAY_ARABIC_SCRIPT,
)
from .tt_mac_langids import (
    TT_MAC_LANGID_MALAY_ROMAN_SCRIPT as TT_MAC_LANGID_MALAY_ROMAN_SCRIPT,
)
from .tt_mac_langids import TT_MAC_LANGID_MALAYALAM as TT_MAC_LANGID_MALAYALAM
from .tt_mac_langids import TT_MAC_LANGID_MALTESE as TT_MAC_LANGID_MALTESE
from .tt_mac_langids import TT_MAC_LANGID_MANX_GAELIC as TT_MAC_LANGID_MANX_GAELIC
from .tt_mac_langids import TT_MAC_LANGID_MARATHI as TT_MAC_LANGID_MARATHI
from .tt_mac_langids import TT_MAC_LANGID_MOLDAVIAN as TT_MAC_LANGID_MOLDAVIAN
from .tt_mac_langids import TT_MAC_LANGID_MONGOLIAN as TT_MAC_LANGID_MONGOLIAN
from .tt_mac_langids import (
    TT_MAC_LANGID_MONGOLIAN_CYRILLIC_SCRIPT as TT_MAC_LANGID_MONGOLIAN_CYRILLIC_SCRIPT,
)
from .tt_mac_langids import (
    TT_MAC_LANGID_MONGOLIAN_MONGOLIAN_SCRIPT as TT_MAC_LANGID_MONGOLIAN_MONGOLIAN_SCRIPT,
)
from .tt_mac_langids import TT_MAC_LANGID_NEPALI as TT_MAC_LANGID_NEPALI
from .tt_mac_langids import TT_MAC_LANGID_NORWEGIAN as TT_MAC_LANGID_NORWEGIAN
from .tt_mac_langids import TT_MAC_LANGID_ORIYA as TT_MAC_LANGID_ORIYA
from .tt_mac_langids import TT_MAC_LANGID_PASHTO as TT_MAC_LANGID_PASHTO
from .tt_mac_langids import TT_MAC_LANGID_POLISH as TT_MAC_LANGID_POLISH
from .tt_mac_langids import TT_MAC_LANGID_PORTUGUESE as TT_MAC_LANGID_PORTUGUESE
from .tt_mac_langids import TT_MAC_LANGID_PUNJABI as TT_MAC_LANGID_PUNJABI
from .tt_mac_langids import TT_MAC_LANGID_QUECHUA as TT_MAC_LANGID_QUECHUA
from .tt_mac_langids import TT_MAC_LANGID_ROMANIAN as TT_MAC_LANGID_ROMANIAN
from .tt_mac_langids import TT_MAC_LANGID_RUANDA as TT_MAC_LANGID_RUANDA
from .tt_mac_langids import TT_MAC_LANGID_RUNDI as TT_MAC_LANGID_RUNDI
from .tt_mac_langids import TT_MAC_LANGID_RUSSIAN as TT_MAC_LANGID_RUSSIAN
from .tt_mac_langids import TT_MAC_LANGID_SAAMISK as TT_MAC_LANGID_SAAMISK
from .tt_mac_langids import TT_MAC_LANGID_SANSKRIT as TT_MAC_LANGID_SANSKRIT
from .tt_mac_langids import (
    TT_MAC_LANGID_SCOTTISH_GAELIC as TT_MAC_LANGID_SCOTTISH_GAELIC,
)
from .tt_mac_langids import TT_MAC_LANGID_SERBIAN as TT_MAC_LANGID_SERBIAN
from .tt_mac_langids import TT_MAC_LANGID_SINDHI as TT_MAC_LANGID_SINDHI
from .tt_mac_langids import TT_MAC_LANGID_SINHALESE as TT_MAC_LANGID_SINHALESE
from .tt_mac_langids import TT_MAC_LANGID_SLOVAK as TT_MAC_LANGID_SLOVAK
from .tt_mac_langids import TT_MAC_LANGID_SLOVENIAN as TT_MAC_LANGID_SLOVENIAN
from .tt_mac_langids import TT_MAC_LANGID_SOMALI as TT_MAC_LANGID_SOMALI
from .tt_mac_langids import TT_MAC_LANGID_SPANISH as TT_MAC_LANGID_SPANISH
from .tt_mac_langids import TT_MAC_LANGID_SUNDANESE as TT_MAC_LANGID_SUNDANESE
from .tt_mac_langids import TT_MAC_LANGID_SWAHILI as TT_MAC_LANGID_SWAHILI
from .tt_mac_langids import TT_MAC_LANGID_SWEDISH as TT_MAC_LANGID_SWEDISH
from .tt_mac_langids import TT_MAC_LANGID_TAGALOG as TT_MAC_LANGID_TAGALOG
from .tt_mac_langids import TT_MAC_LANGID_TAJIKI as TT_MAC_LANGID_TAJIKI
from .tt_mac_langids import TT_MAC_LANGID_TAMIL as TT_MAC_LANGID_TAMIL
from .tt_mac_langids import TT_MAC_LANGID_TATAR as TT_MAC_LANGID_TATAR
from .tt_mac_langids import TT_MAC_LANGID_TELUGU as TT_MAC_LANGID_TELUGU
from .tt_mac_langids import TT_MAC_LANGID_THAI as TT_MAC_LANGID_THAI
from .tt_mac_langids import TT_MAC_LANGID_TIBETAN as TT_MAC_LANGID_TIBETAN
from .tt_mac_langids import TT_MAC_LANGID_TIGRINYA as TT_MAC_LANGID_TIGRINYA
from .tt_mac_langids import TT_MAC_LANGID_TONGAN as TT_MAC_LANGID_TONGAN
from .tt_mac_langids import TT_MAC_LANGID_TURKISH as TT_MAC_LANGID_TURKISH
from .tt_mac_langids import TT_MAC_LANGID_TURKMEN as TT_MAC_LANGID_TURKMEN
from .tt_mac_langids import TT_MAC_LANGID_UIGHUR as TT_MAC_LANGID_UIGHUR
from .tt_mac_langids import TT_MAC_LANGID_UKRAINIAN as TT_MAC_LANGID_UKRAINIAN
from .tt_mac_langids import TT_MAC_LANGID_URDU as TT_MAC_LANGID_URDU
from .tt_mac_langids import TT_MAC_LANGID_UZBEK as TT_MAC_LANGID_UZBEK
from .tt_mac_langids import TT_MAC_LANGID_VIETNAMESE as TT_MAC_LANGID_VIETNAMESE
from .tt_mac_langids import TT_MAC_LANGID_WELSH as TT_MAC_LANGID_WELSH
from .tt_mac_langids import TT_MAC_LANGID_YIDDISH as TT_MAC_LANGID_YIDDISH
from .tt_ms_ids import TT_MS_ID_BIG_5 as TT_MS_ID_BIG_5
from .tt_ms_ids import TT_MS_ID_JOHAB as TT_MS_ID_JOHAB
from .tt_ms_ids import TT_MS_ID_PRC as TT_MS_ID_PRC
from .tt_ms_ids import TT_MS_ID_SJIS as TT_MS_ID_SJIS
from .tt_ms_ids import TT_MS_ID_SYMBOL_CS as TT_MS_ID_SYMBOL_CS
from .tt_ms_ids import TT_MS_ID_UCS_4 as TT_MS_ID_UCS_4
from .tt_ms_ids import TT_MS_ID_UNICODE_CS as TT_MS_ID_UNICODE_CS
from .tt_ms_ids import TT_MS_ID_WANSUNG as TT_MS_ID_WANSUNG
from .tt_ms_ids import TT_MS_IDS as TT_MS_IDS
from .tt_ms_langids import (
    TT_MS_LANGID_AFRIKAANS_SOUTH_AFRICA as TT_MS_LANGID_AFRIKAANS_SOUTH_AFRICA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ALBANIAN_ALBANIA as TT_MS_LANGID_ALBANIAN_ALBANIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_AMHARIC_ETHIOPIA as TT_MS_LANGID_AMHARIC_ETHIOPIA,
)
from .tt_ms_langids import TT_MS_LANGID_ARABIC_ALGERIA as TT_MS_LANGID_ARABIC_ALGERIA
from .tt_ms_langids import TT_MS_LANGID_ARABIC_BAHRAIN as TT_MS_LANGID_ARABIC_BAHRAIN
from .tt_ms_langids import TT_MS_LANGID_ARABIC_EGYPT as TT_MS_LANGID_ARABIC_EGYPT
from .tt_ms_langids import TT_MS_LANGID_ARABIC_GENERAL as TT_MS_LANGID_ARABIC_GENERAL
from .tt_ms_langids import TT_MS_LANGID_ARABIC_IRAQ as TT_MS_LANGID_ARABIC_IRAQ
from .tt_ms_langids import TT_MS_LANGID_ARABIC_JORDAN as TT_MS_LANGID_ARABIC_JORDAN
from .tt_ms_langids import TT_MS_LANGID_ARABIC_KUWAIT as TT_MS_LANGID_ARABIC_KUWAIT
from .tt_ms_langids import TT_MS_LANGID_ARABIC_LEBANON as TT_MS_LANGID_ARABIC_LEBANON
from .tt_ms_langids import TT_MS_LANGID_ARABIC_LIBYA as TT_MS_LANGID_ARABIC_LIBYA
from .tt_ms_langids import TT_MS_LANGID_ARABIC_MOROCCO as TT_MS_LANGID_ARABIC_MOROCCO
from .tt_ms_langids import TT_MS_LANGID_ARABIC_OMAN as TT_MS_LANGID_ARABIC_OMAN
from .tt_ms_langids import TT_MS_LANGID_ARABIC_QATAR as TT_MS_LANGID_ARABIC_QATAR
from .tt_ms_langids import (
    TT_MS_LANGID_ARABIC_SAUDI_ARABIA as TT_MS_LANGID_ARABIC_SAUDI_ARABIA,
)
from .tt_ms_langids import TT_MS_LANGID_ARABIC_SYRIA as TT_MS_LANGID_ARABIC_SYRIA
from .tt_ms_langids import TT_MS_LANGID_ARABIC_TUNISIA as TT_MS_LANGID_ARABIC_TUNISIA
from .tt_ms_langids import TT_MS_LANGID_ARABIC_UAE as TT_MS_LANGID_ARABIC_UAE
from .tt_ms_langids import TT_MS_LANGID_ARABIC_YEMEN as TT_MS_LANGID_ARABIC_YEMEN
from .tt_ms_langids import (
    TT_MS_LANGID_ARMENIAN_ARMENIA as TT_MS_LANGID_ARMENIAN_ARMENIA,
)
from .tt_ms_langids import TT_MS_LANGID_ASSAMESE_INDIA as TT_MS_LANGID_ASSAMESE_INDIA
from .tt_ms_langids import (
    TT_MS_LANGID_AZERI_AZERBAIJAN_CYRILLIC as TT_MS_LANGID_AZERI_AZERBAIJAN_CYRILLIC,
)
from .tt_ms_langids import (
    TT_MS_LANGID_AZERI_AZERBAIJAN_LATIN as TT_MS_LANGID_AZERI_AZERBAIJAN_LATIN,
)
from .tt_ms_langids import TT_MS_LANGID_BASQUE_SPAIN as TT_MS_LANGID_BASQUE_SPAIN
from .tt_ms_langids import (
    TT_MS_LANGID_BELARUSIAN_BELARUS as TT_MS_LANGID_BELARUSIAN_BELARUS,
)
from .tt_ms_langids import (
    TT_MS_LANGID_BENGALI_BANGLADESH as TT_MS_LANGID_BENGALI_BANGLADESH,
)
from .tt_ms_langids import TT_MS_LANGID_BENGALI_INDIA as TT_MS_LANGID_BENGALI_INDIA
from .tt_ms_langids import (
    TT_MS_LANGID_BOSNIAN_BOSNIA_HERZEGOVINA as TT_MS_LANGID_BOSNIAN_BOSNIA_HERZEGOVINA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_BULGARIAN_BULGARIA as TT_MS_LANGID_BULGARIAN_BULGARIA,
)
from .tt_ms_langids import TT_MS_LANGID_BURMESE_MYANMAR as TT_MS_LANGID_BURMESE_MYANMAR
from .tt_ms_langids import TT_MS_LANGID_CATALAN_SPAIN as TT_MS_LANGID_CATALAN_SPAIN
from .tt_ms_langids import (
    TT_MS_LANGID_CHEROKEE_UNITED_STATES as TT_MS_LANGID_CHEROKEE_UNITED_STATES,
)
from .tt_ms_langids import TT_MS_LANGID_CHINESE_GENERAL as TT_MS_LANGID_CHINESE_GENERAL
from .tt_ms_langids import (
    TT_MS_LANGID_CHINESE_HONG_KONG as TT_MS_LANGID_CHINESE_HONG_KONG,
)
from .tt_ms_langids import TT_MS_LANGID_CHINESE_MACAU as TT_MS_LANGID_CHINESE_MACAU
from .tt_ms_langids import TT_MS_LANGID_CHINESE_PRC as TT_MS_LANGID_CHINESE_PRC
from .tt_ms_langids import (
    TT_MS_LANGID_CHINESE_SINGAPORE as TT_MS_LANGID_CHINESE_SINGAPORE,
)
from .tt_ms_langids import TT_MS_LANGID_CHINESE_TAIWAN as TT_MS_LANGID_CHINESE_TAIWAN
from .tt_ms_langids import (
    TT_MS_LANGID_CLASSIC_LITHUANIAN_LITHUANIA as TT_MS_LANGID_CLASSIC_LITHUANIAN_LITHUANIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_CROATIAN_BOSNIA_HERZEGOVINA as TT_MS_LANGID_CROATIAN_BOSNIA_HERZEGOVINA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_CROATIAN_CROATIA as TT_MS_LANGID_CROATIAN_CROATIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_CZECH_CZECH_REPUBLIC as TT_MS_LANGID_CZECH_CZECH_REPUBLIC,
)
from .tt_ms_langids import TT_MS_LANGID_DANISH_DENMARK as TT_MS_LANGID_DANISH_DENMARK
from .tt_ms_langids import (
    TT_MS_LANGID_DHIVEHI_MALDIVES as TT_MS_LANGID_DHIVEHI_MALDIVES,
)
from .tt_ms_langids import TT_MS_LANGID_DIVEHI_MALDIVES as TT_MS_LANGID_DIVEHI_MALDIVES
from .tt_ms_langids import TT_MS_LANGID_DUTCH_BELGIUM as TT_MS_LANGID_DUTCH_BELGIUM
from .tt_ms_langids import (
    TT_MS_LANGID_DUTCH_NETHERLANDS as TT_MS_LANGID_DUTCH_NETHERLANDS,
)
from .tt_ms_langids import TT_MS_LANGID_DZONGHKA_BHUTAN as TT_MS_LANGID_DZONGHKA_BHUTAN
from .tt_ms_langids import TT_MS_LANGID_EDO_NIGERIA as TT_MS_LANGID_EDO_NIGERIA
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_AUSTRALIA as TT_MS_LANGID_ENGLISH_AUSTRALIA,
)
from .tt_ms_langids import TT_MS_LANGID_ENGLISH_BELIZE as TT_MS_LANGID_ENGLISH_BELIZE
from .tt_ms_langids import TT_MS_LANGID_ENGLISH_CANADA as TT_MS_LANGID_ENGLISH_CANADA
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_CARIBBEAN as TT_MS_LANGID_ENGLISH_CARIBBEAN,
)
from .tt_ms_langids import TT_MS_LANGID_ENGLISH_GENERAL as TT_MS_LANGID_ENGLISH_GENERAL
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_HONG_KONG as TT_MS_LANGID_ENGLISH_HONG_KONG,
)
from .tt_ms_langids import TT_MS_LANGID_ENGLISH_INDIA as TT_MS_LANGID_ENGLISH_INDIA
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_INDONESIA as TT_MS_LANGID_ENGLISH_INDONESIA,
)
from .tt_ms_langids import TT_MS_LANGID_ENGLISH_IRELAND as TT_MS_LANGID_ENGLISH_IRELAND
from .tt_ms_langids import TT_MS_LANGID_ENGLISH_JAMAICA as TT_MS_LANGID_ENGLISH_JAMAICA
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_MALAYSIA as TT_MS_LANGID_ENGLISH_MALAYSIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_NEW_ZEALAND as TT_MS_LANGID_ENGLISH_NEW_ZEALAND,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_PHILIPPINES as TT_MS_LANGID_ENGLISH_PHILIPPINES,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_SINGAPORE as TT_MS_LANGID_ENGLISH_SINGAPORE,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_SOUTH_AFRICA as TT_MS_LANGID_ENGLISH_SOUTH_AFRICA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_TRINIDAD as TT_MS_LANGID_ENGLISH_TRINIDAD,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_UNITED_KINGDOM as TT_MS_LANGID_ENGLISH_UNITED_KINGDOM,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_UNITED_STATES as TT_MS_LANGID_ENGLISH_UNITED_STATES,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ENGLISH_ZIMBABWE as TT_MS_LANGID_ENGLISH_ZIMBABWE,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ESTONIAN_ESTONIA as TT_MS_LANGID_ESTONIAN_ESTONIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_FAEROESE_FAEROE_ISLANDS as TT_MS_LANGID_FAEROESE_FAEROE_ISLANDS,
)
from .tt_ms_langids import TT_MS_LANGID_FARSI_IRAN as TT_MS_LANGID_FARSI_IRAN
from .tt_ms_langids import (
    TT_MS_LANGID_FILIPINO_PHILIPPINES as TT_MS_LANGID_FILIPINO_PHILIPPINES,
)
from .tt_ms_langids import TT_MS_LANGID_FINNISH_FINLAND as TT_MS_LANGID_FINNISH_FINLAND
from .tt_ms_langids import TT_MS_LANGID_FRENCH_BELGIUM as TT_MS_LANGID_FRENCH_BELGIUM
from .tt_ms_langids import TT_MS_LANGID_FRENCH_CAMEROON as TT_MS_LANGID_FRENCH_CAMEROON
from .tt_ms_langids import TT_MS_LANGID_FRENCH_CANADA as TT_MS_LANGID_FRENCH_CANADA
from .tt_ms_langids import TT_MS_LANGID_FRENCH_CONGO as TT_MS_LANGID_FRENCH_CONGO
from .tt_ms_langids import (
    TT_MS_LANGID_FRENCH_COTE_D_IVOIRE as TT_MS_LANGID_FRENCH_COTE_D_IVOIRE,
)
from .tt_ms_langids import TT_MS_LANGID_FRENCH_FRANCE as TT_MS_LANGID_FRENCH_FRANCE
from .tt_ms_langids import TT_MS_LANGID_FRENCH_HAITI as TT_MS_LANGID_FRENCH_HAITI
from .tt_ms_langids import (
    TT_MS_LANGID_FRENCH_LUXEMBOURG as TT_MS_LANGID_FRENCH_LUXEMBOURG,
)
from .tt_ms_langids import TT_MS_LANGID_FRENCH_MALI as TT_MS_LANGID_FRENCH_MALI
from .tt_ms_langids import TT_MS_LANGID_FRENCH_MONACO as TT_MS_LANGID_FRENCH_MONACO
from .tt_ms_langids import TT_MS_LANGID_FRENCH_MOROCCO as TT_MS_LANGID_FRENCH_MOROCCO
from .tt_ms_langids import (
    TT_MS_LANGID_FRENCH_NORTH_AFRICA as TT_MS_LANGID_FRENCH_NORTH_AFRICA,
)
from .tt_ms_langids import TT_MS_LANGID_FRENCH_REUNION as TT_MS_LANGID_FRENCH_REUNION
from .tt_ms_langids import TT_MS_LANGID_FRENCH_SENEGAL as TT_MS_LANGID_FRENCH_SENEGAL
from .tt_ms_langids import (
    TT_MS_LANGID_FRENCH_SWITZERLAND as TT_MS_LANGID_FRENCH_SWITZERLAND,
)
from .tt_ms_langids import (
    TT_MS_LANGID_FRENCH_WEST_INDIES as TT_MS_LANGID_FRENCH_WEST_INDIES,
)
from .tt_ms_langids import (
    TT_MS_LANGID_FRISIAN_NETHERLANDS as TT_MS_LANGID_FRISIAN_NETHERLANDS,
)
from .tt_ms_langids import (
    TT_MS_LANGID_FULFULDE_NIGERIA as TT_MS_LANGID_FULFULDE_NIGERIA,
)
from .tt_ms_langids import TT_MS_LANGID_GALICIAN_SPAIN as TT_MS_LANGID_GALICIAN_SPAIN
from .tt_ms_langids import (
    TT_MS_LANGID_GEORGIAN_GEORGIA as TT_MS_LANGID_GEORGIAN_GEORGIA,
)
from .tt_ms_langids import TT_MS_LANGID_GERMAN_AUSTRIA as TT_MS_LANGID_GERMAN_AUSTRIA
from .tt_ms_langids import TT_MS_LANGID_GERMAN_GERMANY as TT_MS_LANGID_GERMAN_GERMANY
from .tt_ms_langids import (
    TT_MS_LANGID_GERMAN_LIECHTENSTEI as TT_MS_LANGID_GERMAN_LIECHTENSTEI,
)
from .tt_ms_langids import (
    TT_MS_LANGID_GERMAN_LUXEMBOURG as TT_MS_LANGID_GERMAN_LUXEMBOURG,
)
from .tt_ms_langids import (
    TT_MS_LANGID_GERMAN_SWITZERLAND as TT_MS_LANGID_GERMAN_SWITZERLAND,
)
from .tt_ms_langids import TT_MS_LANGID_GREEK_GREECE as TT_MS_LANGID_GREEK_GREECE
from .tt_ms_langids import (
    TT_MS_LANGID_GUARANI_PARAGUAY as TT_MS_LANGID_GUARANI_PARAGUAY,
)
from .tt_ms_langids import TT_MS_LANGID_GUJARATI_INDIA as TT_MS_LANGID_GUJARATI_INDIA
from .tt_ms_langids import TT_MS_LANGID_HAUSA_NIGERIA as TT_MS_LANGID_HAUSA_NIGERIA
from .tt_ms_langids import (
    TT_MS_LANGID_HAWAIIAN_UNITED_STATES as TT_MS_LANGID_HAWAIIAN_UNITED_STATES,
)
from .tt_ms_langids import TT_MS_LANGID_HEBREW_ISRAEL as TT_MS_LANGID_HEBREW_ISRAEL
from .tt_ms_langids import TT_MS_LANGID_HINDI_INDIA as TT_MS_LANGID_HINDI_INDIA
from .tt_ms_langids import (
    TT_MS_LANGID_HUNGARIAN_HUNGARY as TT_MS_LANGID_HUNGARIAN_HUNGARY,
)
from .tt_ms_langids import TT_MS_LANGID_IBIBIO_NIGERIA as TT_MS_LANGID_IBIBIO_NIGERIA
from .tt_ms_langids import (
    TT_MS_LANGID_ICELANDIC_ICELAND as TT_MS_LANGID_ICELANDIC_ICELAND,
)
from .tt_ms_langids import TT_MS_LANGID_IGBO_NIGERIA as TT_MS_LANGID_IGBO_NIGERIA
from .tt_ms_langids import (
    TT_MS_LANGID_INDONESIAN_INDONESIA as TT_MS_LANGID_INDONESIAN_INDONESIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_INUKTITUT_CANADA as TT_MS_LANGID_INUKTITUT_CANADA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_IRISH_GAELIC_IRELAND as TT_MS_LANGID_IRISH_GAELIC_IRELAND,
)
from .tt_ms_langids import TT_MS_LANGID_ITALIAN_ITALY as TT_MS_LANGID_ITALIAN_ITALY
from .tt_ms_langids import (
    TT_MS_LANGID_ITALIAN_SWITZERLAND as TT_MS_LANGID_ITALIAN_SWITZERLAND,
)
from .tt_ms_langids import TT_MS_LANGID_JAPANESE_JAPAN as TT_MS_LANGID_JAPANESE_JAPAN
from .tt_ms_langids import TT_MS_LANGID_KANNADA_INDIA as TT_MS_LANGID_KANNADA_INDIA
from .tt_ms_langids import TT_MS_LANGID_KANURI_NIGERIA as TT_MS_LANGID_KANURI_NIGERIA
from .tt_ms_langids import TT_MS_LANGID_KASHMIRI_INDIA as TT_MS_LANGID_KASHMIRI_INDIA
from .tt_ms_langids import (
    TT_MS_LANGID_KASHMIRI_PAKISTAN as TT_MS_LANGID_KASHMIRI_PAKISTAN,
)
from .tt_ms_langids import TT_MS_LANGID_KASHMIRI_SASIA as TT_MS_LANGID_KASHMIRI_SASIA
from .tt_ms_langids import TT_MS_LANGID_KAZAK_KAZAKSTAN as TT_MS_LANGID_KAZAK_KAZAKSTAN
from .tt_ms_langids import TT_MS_LANGID_KHMER_CAMBODIA as TT_MS_LANGID_KHMER_CAMBODIA
from .tt_ms_langids import (
    TT_MS_LANGID_KIRGHIZ_KIRGHIZ_REPUBLIC as TT_MS_LANGID_KIRGHIZ_KIRGHIZ_REPUBLIC,
)
from .tt_ms_langids import (
    TT_MS_LANGID_KIRGHIZ_KIRGHIZSTAN as TT_MS_LANGID_KIRGHIZ_KIRGHIZSTAN,
)
from .tt_ms_langids import TT_MS_LANGID_KONKANI_INDIA as TT_MS_LANGID_KONKANI_INDIA
from .tt_ms_langids import (
    TT_MS_LANGID_KOREAN_EXTENDED_WANSUNG_KOREA as TT_MS_LANGID_KOREAN_EXTENDED_WANSUNG_KOREA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_KOREAN_JOHAB_KOREA as TT_MS_LANGID_KOREAN_JOHAB_KOREA,
)
from .tt_ms_langids import TT_MS_LANGID_LAO_LAOS as TT_MS_LANGID_LAO_LAOS
from .tt_ms_langids import TT_MS_LANGID_LATIN as TT_MS_LANGID_LATIN
from .tt_ms_langids import TT_MS_LANGID_LATVIAN_LATVIA as TT_MS_LANGID_LATVIAN_LATVIA
from .tt_ms_langids import (
    TT_MS_LANGID_LITHUANIAN_LITHUANIA as TT_MS_LANGID_LITHUANIAN_LITHUANIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_MACEDONIAN_MACEDONIA as TT_MS_LANGID_MACEDONIAN_MACEDONIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_MALAY_BRUNEI_DARUSSALAM as TT_MS_LANGID_MALAY_BRUNEI_DARUSSALAM,
)
from .tt_ms_langids import TT_MS_LANGID_MALAY_MALAYSIA as TT_MS_LANGID_MALAY_MALAYSIA
from .tt_ms_langids import TT_MS_LANGID_MALAYALAM_INDIA as TT_MS_LANGID_MALAYALAM_INDIA
from .tt_ms_langids import TT_MS_LANGID_MALTESE_MALTA as TT_MS_LANGID_MALTESE_MALTA
from .tt_ms_langids import TT_MS_LANGID_MANIPURI_INDIA as TT_MS_LANGID_MANIPURI_INDIA
from .tt_ms_langids import (
    TT_MS_LANGID_MAORI_NEW_ZEALAND as TT_MS_LANGID_MAORI_NEW_ZEALAND,
)
from .tt_ms_langids import TT_MS_LANGID_MARATHI_INDIA as TT_MS_LANGID_MARATHI_INDIA
from .tt_ms_langids import (
    TT_MS_LANGID_MOLDAVIAN_MOLDAVIA as TT_MS_LANGID_MOLDAVIAN_MOLDAVIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_MONGOLIAN_MONGOLIA as TT_MS_LANGID_MONGOLIAN_MONGOLIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_MONGOLIAN_MONGOLIA_MONGOLIAN as TT_MS_LANGID_MONGOLIAN_MONGOLIA_MONGOLIAN,
)
from .tt_ms_langids import TT_MS_LANGID_NEPALI_INDIA as TT_MS_LANGID_NEPALI_INDIA
from .tt_ms_langids import TT_MS_LANGID_NEPALI_NEPAL as TT_MS_LANGID_NEPALI_NEPAL
from .tt_ms_langids import (
    TT_MS_LANGID_NORWEGIAN_NORWAY_BOKMAL as TT_MS_LANGID_NORWEGIAN_NORWAY_BOKMAL,
)
from .tt_ms_langids import (
    TT_MS_LANGID_NORWEGIAN_NORWAY_NYNORSK as TT_MS_LANGID_NORWEGIAN_NORWAY_NYNORSK,
)
from .tt_ms_langids import TT_MS_LANGID_ORIYA_INDIA as TT_MS_LANGID_ORIYA_INDIA
from .tt_ms_langids import TT_MS_LANGID_OROMO_ETHIOPIA as TT_MS_LANGID_OROMO_ETHIOPIA
from .tt_ms_langids import (
    TT_MS_LANGID_PAPIAMENTU_NETHERLANDS_ANTILLES as TT_MS_LANGID_PAPIAMENTU_NETHERLANDS_ANTILLES,
)
from .tt_ms_langids import (
    TT_MS_LANGID_PASHTO_AFGHANISTAN as TT_MS_LANGID_PASHTO_AFGHANISTAN,
)
from .tt_ms_langids import TT_MS_LANGID_POLISH_POLAND as TT_MS_LANGID_POLISH_POLAND
from .tt_ms_langids import (
    TT_MS_LANGID_PORTUGUESE_BRAZIL as TT_MS_LANGID_PORTUGUESE_BRAZIL,
)
from .tt_ms_langids import (
    TT_MS_LANGID_PORTUGUESE_PORTUGAL as TT_MS_LANGID_PORTUGUESE_PORTUGAL,
)
from .tt_ms_langids import (
    TT_MS_LANGID_PUNJABI_ARABIC_PAKISTAN as TT_MS_LANGID_PUNJABI_ARABIC_PAKISTAN,
)
from .tt_ms_langids import TT_MS_LANGID_PUNJABI_INDIA as TT_MS_LANGID_PUNJABI_INDIA
from .tt_ms_langids import TT_MS_LANGID_QUECHUA_BOLIVIA as TT_MS_LANGID_QUECHUA_BOLIVIA
from .tt_ms_langids import TT_MS_LANGID_QUECHUA_ECUADOR as TT_MS_LANGID_QUECHUA_ECUADOR
from .tt_ms_langids import TT_MS_LANGID_QUECHUA_PERU as TT_MS_LANGID_QUECHUA_PERU
from .tt_ms_langids import (
    TT_MS_LANGID_RHAETO_ROMANIC_SWITZERLAND as TT_MS_LANGID_RHAETO_ROMANIC_SWITZERLAND,
)
from .tt_ms_langids import (
    TT_MS_LANGID_ROMANIAN_ROMANIA as TT_MS_LANGID_ROMANIAN_ROMANIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_RUSSIAN_MOLDAVIA as TT_MS_LANGID_RUSSIAN_MOLDAVIA,
)
from .tt_ms_langids import TT_MS_LANGID_RUSSIAN_RUSSIA as TT_MS_LANGID_RUSSIAN_RUSSIA
from .tt_ms_langids import TT_MS_LANGID_SAAMI_LAPONIA as TT_MS_LANGID_SAAMI_LAPONIA
from .tt_ms_langids import (
    TT_MS_LANGID_SAMI_INARI_FINLAND as TT_MS_LANGID_SAMI_INARI_FINLAND,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SAMI_LULE_NORWAY as TT_MS_LANGID_SAMI_LULE_NORWAY,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SAMI_LULE_SWEDEN as TT_MS_LANGID_SAMI_LULE_SWEDEN,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SAMI_NORTHERN_FINLAND as TT_MS_LANGID_SAMI_NORTHERN_FINLAND,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SAMI_NORTHERN_NORWAY as TT_MS_LANGID_SAMI_NORTHERN_NORWAY,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SAMI_NORTHERN_SWEDEN as TT_MS_LANGID_SAMI_NORTHERN_SWEDEN,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SAMI_SKOLT_FINLAND as TT_MS_LANGID_SAMI_SKOLT_FINLAND,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SAMI_SOUTHERN_NORWAY as TT_MS_LANGID_SAMI_SOUTHERN_NORWAY,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SAMI_SOUTHERN_SWEDEN as TT_MS_LANGID_SAMI_SOUTHERN_SWEDEN,
)
from .tt_ms_langids import TT_MS_LANGID_SANSKRIT_INDIA as TT_MS_LANGID_SANSKRIT_INDIA
from .tt_ms_langids import (
    TT_MS_LANGID_SCOTTISH_GAELIC_UNITED_KINGDOM as TT_MS_LANGID_SCOTTISH_GAELIC_UNITED_KINGDOM,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SEPEDI_SOUTH_AFRICA as TT_MS_LANGID_SEPEDI_SOUTH_AFRICA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SERBIAN_BOSNIA_HERZ_CYRILLIC as TT_MS_LANGID_SERBIAN_BOSNIA_HERZ_CYRILLIC,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SERBIAN_BOSNIA_HERZ_LATIN as TT_MS_LANGID_SERBIAN_BOSNIA_HERZ_LATIN,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SERBIAN_SERBIA_CYRILLIC as TT_MS_LANGID_SERBIAN_SERBIA_CYRILLIC,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SERBIAN_SERBIA_LATIN as TT_MS_LANGID_SERBIAN_SERBIA_LATIN,
)
from .tt_ms_langids import TT_MS_LANGID_SINDHI_INDIA as TT_MS_LANGID_SINDHI_INDIA
from .tt_ms_langids import TT_MS_LANGID_SINDHI_PAKISTAN as TT_MS_LANGID_SINDHI_PAKISTAN
from .tt_ms_langids import (
    TT_MS_LANGID_SINHALESE_SRI_LANKA as TT_MS_LANGID_SINHALESE_SRI_LANKA,
)
from .tt_ms_langids import TT_MS_LANGID_SLOVAK_SLOVAKIA as TT_MS_LANGID_SLOVAK_SLOVAKIA
from .tt_ms_langids import (
    TT_MS_LANGID_SLOVENE_SLOVENIA as TT_MS_LANGID_SLOVENE_SLOVENIA,
)
from .tt_ms_langids import TT_MS_LANGID_SOMALI_SOMALIA as TT_MS_LANGID_SOMALI_SOMALIA
from .tt_ms_langids import TT_MS_LANGID_SORBIAN_GERMANY as TT_MS_LANGID_SORBIAN_GERMANY
from .tt_ms_langids import (
    TT_MS_LANGID_SOTHO_SOUTHERN_SOUTH_AFRICA as TT_MS_LANGID_SOTHO_SOUTHERN_SOUTH_AFRICA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_ARGENTINA as TT_MS_LANGID_SPANISH_ARGENTINA,
)
from .tt_ms_langids import TT_MS_LANGID_SPANISH_BOLIVIA as TT_MS_LANGID_SPANISH_BOLIVIA
from .tt_ms_langids import TT_MS_LANGID_SPANISH_CHILE as TT_MS_LANGID_SPANISH_CHILE
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_COLOMBIA as TT_MS_LANGID_SPANISH_COLOMBIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_COSTA_RICA as TT_MS_LANGID_SPANISH_COSTA_RICA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_DOMINICAN_REPUBLIC as TT_MS_LANGID_SPANISH_DOMINICAN_REPUBLIC,
)
from .tt_ms_langids import TT_MS_LANGID_SPANISH_ECUADOR as TT_MS_LANGID_SPANISH_ECUADOR
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_EL_SALVADOR as TT_MS_LANGID_SPANISH_EL_SALVADOR,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_GUATEMALA as TT_MS_LANGID_SPANISH_GUATEMALA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_HONDURAS as TT_MS_LANGID_SPANISH_HONDURAS,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_LATIN_AMERICA as TT_MS_LANGID_SPANISH_LATIN_AMERICA,
)
from .tt_ms_langids import TT_MS_LANGID_SPANISH_MEXICO as TT_MS_LANGID_SPANISH_MEXICO
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_NICARAGUA as TT_MS_LANGID_SPANISH_NICARAGUA,
)
from .tt_ms_langids import TT_MS_LANGID_SPANISH_PANAMA as TT_MS_LANGID_SPANISH_PANAMA
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_PARAGUAY as TT_MS_LANGID_SPANISH_PARAGUAY,
)
from .tt_ms_langids import TT_MS_LANGID_SPANISH_PERU as TT_MS_LANGID_SPANISH_PERU
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_PUERTO_RICO as TT_MS_LANGID_SPANISH_PUERTO_RICO,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_SPAIN_INTERNATIONAL_SORT as TT_MS_LANGID_SPANISH_SPAIN_INTERNATIONAL_SORT,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_SPAIN_TRADITIONAL_SORT as TT_MS_LANGID_SPANISH_SPAIN_TRADITIONAL_SORT,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_UNITED_STATES as TT_MS_LANGID_SPANISH_UNITED_STATES,
)
from .tt_ms_langids import TT_MS_LANGID_SPANISH_URUGUAY as TT_MS_LANGID_SPANISH_URUGUAY
from .tt_ms_langids import (
    TT_MS_LANGID_SPANISH_VENEZUELA as TT_MS_LANGID_SPANISH_VENEZUELA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_SUTU_SOUTH_AFRICA as TT_MS_LANGID_SUTU_SOUTH_AFRICA,
)
from .tt_ms_langids import TT_MS_LANGID_SWAHILI_KENYA as TT_MS_LANGID_SWAHILI_KENYA
from .tt_ms_langids import TT_MS_LANGID_SWEDISH_FINLAND as TT_MS_LANGID_SWEDISH_FINLAND
from .tt_ms_langids import TT_MS_LANGID_SWEDISH_SWEDEN as TT_MS_LANGID_SWEDISH_SWEDEN
from .tt_ms_langids import TT_MS_LANGID_SYRIAC_SYRIA as TT_MS_LANGID_SYRIAC_SYRIA
from .tt_ms_langids import (
    TT_MS_LANGID_TAJIK_TAJIKISTAN as TT_MS_LANGID_TAJIK_TAJIKISTAN,
)
from .tt_ms_langids import (
    TT_MS_LANGID_TAMAZIGHT_MOROCCO as TT_MS_LANGID_TAMAZIGHT_MOROCCO,
)
from .tt_ms_langids import (
    TT_MS_LANGID_TAMAZIGHT_MOROCCO_LATIN as TT_MS_LANGID_TAMAZIGHT_MOROCCO_LATIN,
)
from .tt_ms_langids import TT_MS_LANGID_TAMIL_INDIA as TT_MS_LANGID_TAMIL_INDIA
from .tt_ms_langids import TT_MS_LANGID_TATAR_TATARSTAN as TT_MS_LANGID_TATAR_TATARSTAN
from .tt_ms_langids import TT_MS_LANGID_TELUGU_INDIA as TT_MS_LANGID_TELUGU_INDIA
from .tt_ms_langids import TT_MS_LANGID_THAI_THAILAND as TT_MS_LANGID_THAI_THAILAND
from .tt_ms_langids import TT_MS_LANGID_TIBETAN_BHUTAN as TT_MS_LANGID_TIBETAN_BHUTAN
from .tt_ms_langids import TT_MS_LANGID_TIBETAN_CHINA as TT_MS_LANGID_TIBETAN_CHINA
from .tt_ms_langids import (
    TT_MS_LANGID_TIGRIGNA_ERYTHREA as TT_MS_LANGID_TIGRIGNA_ERYTHREA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_TIGRIGNA_ERYTREA as TT_MS_LANGID_TIGRIGNA_ERYTREA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_TIGRIGNA_ETHIOPIA as TT_MS_LANGID_TIGRIGNA_ETHIOPIA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_TSONGA_SOUTH_AFRICA as TT_MS_LANGID_TSONGA_SOUTH_AFRICA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_TSWANA_SOUTH_AFRICA as TT_MS_LANGID_TSWANA_SOUTH_AFRICA,
)
from .tt_ms_langids import TT_MS_LANGID_TURKISH_TURKEY as TT_MS_LANGID_TURKISH_TURKEY
from .tt_ms_langids import (
    TT_MS_LANGID_TURKMEN_TURKMENISTAN as TT_MS_LANGID_TURKMEN_TURKMENISTAN,
)
from .tt_ms_langids import TT_MS_LANGID_UIGHUR_CHINA as TT_MS_LANGID_UIGHUR_CHINA
from .tt_ms_langids import (
    TT_MS_LANGID_UKRAINIAN_UKRAINE as TT_MS_LANGID_UKRAINIAN_UKRAINE,
)
from .tt_ms_langids import TT_MS_LANGID_URDU_INDIA as TT_MS_LANGID_URDU_INDIA
from .tt_ms_langids import TT_MS_LANGID_URDU_PAKISTAN as TT_MS_LANGID_URDU_PAKISTAN
from .tt_ms_langids import (
    TT_MS_LANGID_UZBEK_UZBEKISTAN_CYRILLIC as TT_MS_LANGID_UZBEK_UZBEKISTAN_CYRILLIC,
)
from .tt_ms_langids import (
    TT_MS_LANGID_UZBEK_UZBEKISTAN_LATIN as TT_MS_LANGID_UZBEK_UZBEKISTAN_LATIN,
)
from .tt_ms_langids import (
    TT_MS_LANGID_VENDA_SOUTH_AFRICA as TT_MS_LANGID_VENDA_SOUTH_AFRICA,
)
from .tt_ms_langids import (
    TT_MS_LANGID_VIETNAMESE_VIET_NAM as TT_MS_LANGID_VIETNAMESE_VIET_NAM,
)
from .tt_ms_langids import TT_MS_LANGID_WELSH_WALES as TT_MS_LANGID_WELSH_WALES
from .tt_ms_langids import (
    TT_MS_LANGID_XHOSA_SOUTH_AFRICA as TT_MS_LANGID_XHOSA_SOUTH_AFRICA,
)
from .tt_ms_langids import TT_MS_LANGID_YI_CHINA as TT_MS_LANGID_YI_CHINA
from .tt_ms_langids import TT_MS_LANGID_YIDDISH_GERMANY as TT_MS_LANGID_YIDDISH_GERMANY
from .tt_ms_langids import TT_MS_LANGID_YORUBA_NIGERIA as TT_MS_LANGID_YORUBA_NIGERIA
from .tt_ms_langids import (
    TT_MS_LANGID_ZULU_SOUTH_AFRICA as TT_MS_LANGID_ZULU_SOUTH_AFRICA,
)
from .tt_name_ids import TT_NAME_ID_CID_FINDFONT_NAME as TT_NAME_ID_CID_FINDFONT_NAME
from .tt_name_ids import TT_NAME_ID_COPYRIGHT as TT_NAME_ID_COPYRIGHT
from .tt_name_ids import TT_NAME_ID_DESCRIPTION as TT_NAME_ID_DESCRIPTION
from .tt_name_ids import TT_NAME_ID_DESIGNER as TT_NAME_ID_DESIGNER
from .tt_name_ids import TT_NAME_ID_DESIGNER_URL as TT_NAME_ID_DESIGNER_URL
from .tt_name_ids import TT_NAME_ID_FONT_FAMILY as TT_NAME_ID_FONT_FAMILY
from .tt_name_ids import TT_NAME_ID_FONT_SUBFAMILY as TT_NAME_ID_FONT_SUBFAMILY
from .tt_name_ids import TT_NAME_ID_FULL_NAME as TT_NAME_ID_FULL_NAME
from .tt_name_ids import TT_NAME_ID_LICENSE as TT_NAME_ID_LICENSE
from .tt_name_ids import TT_NAME_ID_LICENSE_URL as TT_NAME_ID_LICENSE_URL
from .tt_name_ids import TT_NAME_ID_MAC_FULL_NAME as TT_NAME_ID_MAC_FULL_NAME
from .tt_name_ids import TT_NAME_ID_MANUFACTURER as TT_NAME_ID_MANUFACTURER
from .tt_name_ids import TT_NAME_ID_PREFERRED_FAMILY as TT_NAME_ID_PREFERRED_FAMILY
from .tt_name_ids import (
    TT_NAME_ID_PREFERRED_SUBFAMILY as TT_NAME_ID_PREFERRED_SUBFAMILY,
)
from .tt_name_ids import TT_NAME_ID_PS_NAME as TT_NAME_ID_PS_NAME
from .tt_name_ids import TT_NAME_ID_SAMPLE_TEXT as TT_NAME_ID_SAMPLE_TEXT
from .tt_name_ids import TT_NAME_ID_TRADEMARK as TT_NAME_ID_TRADEMARK
from .tt_name_ids import TT_NAME_ID_UNIQUE_ID as TT_NAME_ID_UNIQUE_ID
from .tt_name_ids import TT_NAME_ID_VENDOR_URL as TT_NAME_ID_VENDOR_URL
from .tt_name_ids import TT_NAME_ID_VERSION_STRING as TT_NAME_ID_VERSION_STRING
from .tt_name_ids import TT_NAME_ID_WWS_FAMILY as TT_NAME_ID_WWS_FAMILY
from .tt_name_ids import TT_NAME_ID_WWS_SUBFAMILY as TT_NAME_ID_WWS_SUBFAMILY
from .tt_platforms import TT_PLATFORM_ADOBE as TT_PLATFORM_ADOBE
from .tt_platforms import TT_PLATFORM_APPLE_UNICODE as TT_PLATFORM_APPLE_UNICODE
from .tt_platforms import TT_PLATFORM_CUSTOM as TT_PLATFORM_CUSTOM
from .tt_platforms import TT_PLATFORM_ISO as TT_PLATFORM_ISO
from .tt_platforms import TT_PLATFORM_MACINTOSH as TT_PLATFORM_MACINTOSH
from .tt_platforms import TT_PLATFORM_MICROSOFT as TT_PLATFORM_MICROSOFT
from .tt_platforms import TT_PLATFORMS as TT_PLATFORMS
