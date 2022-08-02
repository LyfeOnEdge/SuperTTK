# console_blue_green.tcl -
# based on black.tcl
#   Experimental!
#
#  Copyright (c) 2007-2008 Mats Bengtsson
#  Background color modified to actually be black by Andrew Spangler
# $Id: black.tcl,v 1.2 2009/10/25 19:21:30 oberdorfer Exp $

package require Tk

namespace eval ttk::theme::console_blue_green {
  variable version 0.0.1
  variable dir [file dirname [info script]]
  package provide ttk::theme::console_blue_green $version
  variable colors
  array set colors {
        -fg         "#00ffA0"
        -disabledfg "#a9a9a9"
        -frame      "#000000"
        -dark       "#222222"
        -darker     "#111111"
        -darkest    "#000000"
        -lighter    "#626262"
        -lightest   "#ffffff"
        -selectbg   "#222222"
        -selectfg   "#ffffff"
      }

  ttk::style theme create console_blue_green -parent clam -settings {

    # # -----------------------------------------------------------------
    # # Theme defaults
    # #
    ttk::style configure . \
        -background $colors(-frame) \
        -foreground $colors(-fg) \
        -bordercolor $colors(-darkest) \
        -darkcolor $colors(-dark) \
        -lightcolor $colors(-lighter) \
        -troughcolor $colors(-darker) \
        -selectbackground $colors(-selectbg) \
        -selectforeground $colors(-selectfg) \
        -selectborderwidth 0 \
        -font TkDefaultFont \
        -insertcolor $colors(-selectfg)

    ttk::style map "." \
        -background [list disabled $colors(-frame) \
        active $colors(-lighter)] \
        -foreground [list disabled $colors(-disabledfg)] \
        -selectbackground [list  !focus $colors(-darkest)] \
        -selectforeground [list  !focus $colors(-fg)]

    # ttk widgets.
    ttk::style configure TButton \
        -width -8 -padding {8 2} -relief raised -shiftrelief 2
    ttk::style configure TMenubutton \
        -width -11 -padding {5 1} -relief raised
    ttk::style configure TCheckbutton \
        -indicatorbackground "#626262" -indicatormargin {1 1 4 1}
    ttk::style configure TRadiobutton \
        -indicatorbackground "#626262" -indicatormargin {1 1 4 1}

    ttk::style configure TEntry \
        -fieldbackground #626262 \
        -foreground $colors(-fg) \
        -insertbackground $colors(-fg) \
        -padding {2 0}
    ttk::style configure TCombobox \
        -fieldbackground #626262 \
        -foreground $colors(-fg) \
        -padding {2 0}
    ttk::style configure TSpinbox \
        -fieldbackground #626262 \
        -foreground $colors(-fg)

    ttk::style configure TNotebook.Tab \
        -padding {4 2 4 2}

    # tk widgets.
    ttk::style map Menu \
        -background [list active $colors(-lighter)] \
        -foreground [list disabled $colors(-disabledfg)]

    ttk::style configure TreeCtrl \
        -background gray30 -itembackground {gray60 gray50} \
        -itemfill $colors(-fg) -itemaccentfill yellow
  }
}

# A few tricks for Tablelist.

namespace eval ::tablelist:: {

  proc console_blue_greenTheme {} {
    variable themeDefaults

    array set colors [array get ttk::theme::console_blue_green::colors]

    array set themeDefaults [list \
      -background      "#000000" \
      -foreground      $colors(-fg) \
      -disabledforeground $colors(-disabledfg) \
      -stripebackground      "#191919" \
      -selectbackground      "#4a6984" \
      -selectforeground      "#8b8b00" \
      -selectborderwidth 0 \
      -font        TkTextFont \
      -labelbackground    $colors(-frame) \
      -labeldisabledBg    "#dcdad5" \
      -labelactiveBg    "#eeebe7" \
      -labelpressedBg    "#eeebe7" \
      -labelforeground    #ffffff \
      -labeldisabledFg    "#999999" \
      -labelactiveFg    #ffffff \
      -labelpressedFg    #ffffff \
      -labelfont    TkDefaultFont \
      -labelborderwidth    2 \
      -labelpady    1 \
      -arrowcolor    "" \
      -arrowstyle    sunken10x9 \
      ]
  }
}
