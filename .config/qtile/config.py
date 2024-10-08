#   ___ _____ ___ _     _____    ____             __ _       
#  / _ \_   _|_ _| |   | ____|  / ___|___  _ __  / _(_) __ _ 
# | | | || |  | || |   |  _|   | |   / _ \| '_ \| |_| |/ _` |
# | |_| || |  | || |___| |___  | |__| (_) | | | |  _| | (_| |
#  \__\_\|_| |___|_____|_____|  \____\___/|_| |_|_| |_|\__, |
#                                                      |___/ 
# config by insidesources

import os
import subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
# Make sure 'qtile-extras' is installed or this config will not work.
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
#from qtile_extras.widget import StatusNotifier
import colors

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "brave"     # My browser of choice
myMenu = "rofi -show run" # Shows rofi
myObsidian = "obsidian" # Launches obsidian

# Allows you to input a name when adding treetab section.
@lazy.layout.function
def add_treetab_section(layout):
    prompt = qtile.widgets_map["prompt"]
    prompt.start_input("Section name: ", layout.cmd_add_section)

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

# A list of available commands that can be bound to keys can be found
# at https://docs.qtile.org/en/latest/manual/config/lazy.html
keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod, "shift"], "Return", lazy.spawn("dm-run"), desc='Run Launcher'),
    Key([mod], "b", lazy.spawn(myBrowser), desc='Web browser'),
    Key([mod], "o", lazy.spawn(myObsidian), desc='Obsidian'),
    Key([mod], "l", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.spawn("dm-logout"), desc="Logout menu"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.spawn(myMenu), desc="spawn rofi to run an application"),

    # Switch between windows
    # Some layouts like 'monadtall' only need to use j/k to move
    # through the stack, but other layouts like 'columns' will
    # require all four directions h/j/k/l to move around.
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "tab", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left",
        lazy.layout.shuffle_left(),
        lazy.layout.move_left().when(layout=["treetab"]),
        desc="Move window to the left/move tab left in treetab"),

    Key([mod, "shift"], "Right",
        lazy.layout.shuffle_right(),
        lazy.layout.move_right().when(layout=["treetab"]),
        desc="Move window to the right/move tab right in treetab"),

    Key([mod, "shift"], "Down",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down().when(layout=["treetab"]),
        desc="Move window down/move down a section in treetab"
    ),
    Key([mod, "shift"], "Up",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up().when(layout=["treetab"]),
        desc="Move window downup/move up a section in treetab"
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "space", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Treetab prompt
    Key([mod, "shift"], "a", add_treetab_section, desc='Prompt to add new section in treetab'),

    # Grow/shrink windows left/right. 
    # This is mainly for the 'monadtall' and 'monadwide' layouts
    # although it does also work in the 'bsp' and 'columns' layouts.
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),

    # Grow windows up, down, left, right.  Only works in certain layouts.
    # Works in 'bsp' and 'columns' layout.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    #Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    Key([mod], "t", lazy.window.toggle_floating(), desc='toggle floating'),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    #Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to prev monitor'),
    
    # Sound
    Key([mod], "m", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="XF86AudioMute mutes or unmutes the audio"),
    Key([mod], "j", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%"), desc="XF86AudioLowerVolume lowers the audio"),
    Key([mod], "k", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%"), desc="XF86AudioRaiseVolume raises the audio")

    # Emacs programs launched using the key chord CTRL+e followed by 'key'
    #KeyChord([mod],"e", [
    #    Key([], "e", lazy.spawn(myEmacs), desc='Emacs Dashboard'),
    #    Key([], "a", lazy.spawn(myEmacs + "--eval '(emms-play-directory-tree \"~/Music/\")'"), desc='Emacs EMMS'),
    #    Key([], "b", lazy.spawn(myEmacs + "--eval '(ibuffer)'"), desc='Emacs Ibuffer'),
    #    Key([], "d", lazy.spawn(myEmacs + "--eval '(dired nil)'"), desc='Emacs Dired'),
    #    Key([], "i", lazy.spawn(myEmacs + "--eval '(erc)'"), desc='Emacs ERC'),
    #    Key([], "s", lazy.spawn(myEmacs + "--eval '(eshell)'"), desc='Emacs Eshell'),
    #    Key([], "v", lazy.spawn(myEmacs + "--eval '(vterm)'"), desc='Emacs Vterm'),
    #    Key([], "w", lazy.spawn(myEmacs + "--eval '(eww \"distro.tube\")'"), desc='Emacs EWW'),
    #    Key([], "F4", lazy.spawn("killall emacs"),
    #                  lazy.spawn("/usr/bin/emacs --daemon"),
    #                  desc='Kill/restart the Emacs daemon')
    #]),
    
    # Dmenu scripts launched using the key chord SUPER+p followed by 'key'
#    KeyChord([mod], "p", [
#        Key([], "h", lazy.spawn("dm-hub"), desc='List all dmscripts'),
#        Key([], "a", lazy.spawn("dm-sounds"), desc='Choose ambient sound'),
#        Key([], "b", lazy.spawn("dm-setbg"), desc='Set background'),
#        Key([], "c", lazy.spawn("dtos-colorscheme"), desc='Choose color scheme'),
#        Key([], "e", lazy.spawn("dm-confedit"), desc='Choose a config file to edit'),
#        Key([], "i", lazy.spawn("dm-maim"), desc='Take a screenshot'),
#        Key([], "k", lazy.spawn("dm-kill"), desc='Kill processes '),
#        Key([], "m", lazy.spawn("dm-man"), desc='View manpages'),
#        Key([], "n", lazy.spawn("dm-note"), desc='Store and copy notes'),
#        Key([], "o", lazy.spawn("dm-bookman"), desc='Browser bookmarks'),
#        Key([], "p", lazy.spawn("passmenu -p \"Pass: \""), desc='Logout menu'),
#        Key([], "q", lazy.spawn("dm-logout"), desc='Logout menu'),
#        Key([], "r", lazy.spawn("dm-radio"), desc='Listen to online radio'),
#        Key([], "s", lazy.spawn("dm-websearch"), desc='Search various engines'),
#        Key([], "t", lazy.spawn("dm-translate"), desc='Translate text')
#    ])
    
        #spawn rofi
        #Key([mod, "p"],lazy.spawn("rofi -show run", desc='run rofi launcher')),

]
groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9","0"]

group_labels = [" term", " web", " systems", " obsidian", " code", " hack", " admin", " games", " chat", " overflow"]
#group_labels = ["1 - term", "2 - web", "3 - systems", "4 - obsidian", "5 - code", "6 - games", "7 - misc", "8 - hacking", "9 - admin",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "max", "monadtall", "monadtall"]


for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))
 
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )


### COLORSCHEME ###
# Colors are defined in a separate 'colors.py' file.
# There 10 colorschemes available to choose from:
#
# colors = colors.DoomOne
# colors = colors.Dracula
# colors = colors.GruvboxDark
# colors = colors.MonokaiPro
# colors = colors.Nord
# colors = colors.OceanicNext
# colors = colors.Palenight
# colors = colors.SolarizedDark
# colors = colors.SolarizedLight
# colors = colors.TomorrowNight
#
# It is best not manually change the colorscheme; instead run 'dtos-colorscheme'
# which is set to 'MOD + p c'

colors = colors.Nord

### LAYOUTS ###
# Some settings that I use on almost every layout, which saves us
# from having to type these out for each individual layout.
layout_theme = {"border_width": 2,
                "margin": 1,
                "border_focus": colors[16],
                "border_normal": colors[0]
                }

layouts = [
    layout.Bsp(**layout_theme),
    #layout.Floating(**layout_theme)
    layout.RatioTile(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.VerticalTile(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Max(
         border_width = 0,
         margin = 0,
         ),
    layout.Stack(**layout_theme, num_stacks=2),
    layout.Columns(**layout_theme),
    layout.TreeTab(
         font = "source code pro",
         fontsize = 11,
         border_width = 0,
         bg_color = colors[0],
         active_bg = colors[8],
         active_fg = colors[2],
         inactive_bg = colors[1],
         inactive_fg = colors[0],
         padding_left = 8,
         padding_x = 8,
         padding_y = 6,
         sections = ["first", "second", "third"],
         section_fontsize = 10,
         section_fg = colors[7],
         section_top = 15,
         section_bottom = 15,
         level_shift = 8,
         vspace = 3,
         panel_width = 240
         ),
    #layout.Zoomy(**layout_theme),
]

# Some settings that I use on almost every widget, which saves us
# from having to type these out for each individual widget.
widget_defaults = dict(
    font="source code pro",
    fontsize = 11,
    padding = 0,
    background=colors[14]
)

extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.Image(
                 filename = "~/.config/qtile/icons/archlogo.png",
                 scale = "False",
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myMenu)},
                 ),
        widget.Prompt(
                 font = "source code pro",
                 fontsize=14,
                 foreground = colors[1]
                 ),
        widget.GroupBox(
                 fontsize = 11,
                 margin_y = 3,
                 margin_x = 4,
                 padding_y = 2,
                 padding_x = 3,
                 borderwidth = 3,
                 active = colors[1],
                 inactive = colors[1],
                 rounded = False,
                 highlight_color = colors[2],
                 highlight_method = "line",
                 this_current_screen_border = colors[9],
                 this_screen_border = colors [10],
                 other_current_screen_border = colors[10],
                 other_screen_border = colors[10],
                 hide_unused = True,
                 ),
        widget.Spacer(length = 20),
        widget.WindowTabs(
                 separator = ' ',
                 foreground = colors[1],
                 scroll_fixed_width = False,
                 scroll = True,
                 #max_chars = 100,
                 width = 700,
                 decorations=[
                     BorderDecoration(
                         colour = colors[16],
                         border_width = [0, 0, 3, 0], #top right bottom left 
                     )
                 ],
                 ),
        widget.Spacer(length = bar.STRETCH),
        widget.Net(
                format='↓{down:.0f}{down_suffix} ↑{up:.0f}{up_suffix}',
                fmt = 'eth:{}',
                # width = 120,
                interface = 'eno2',
                use_bits = True,
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myBrowser + ' https://www.whatsmyip.org')},
                decorations=[
                     BorderDecoration(
                         colour = colors[9],
                         border_width = [0, 0, 3, 0],
                     )
                 ],
                ),
        widget.Spacer(length = 4),
        widget.CheckUpdates(
                 distro = 'Arch_yay',
                 display_format = '{updates} avail',
                 update_interval = 43200,
                 no_update_string = 'no updates',
                 initial_text = 'checking',
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e yay -Syu')},
                 foreground = colors[1],
                 decorations=[
                     BorderDecoration(
                         colour = colors[15],
                         border_width = [0, 0, 3, 0], #top right bottom left 
                     )
                 ],
                 ),
        widget.Spacer(length = 4),
        widget.GenPollText(
                 update_interval = 300,
                 func = lambda: subprocess.check_output("printf $(uname -r)", shell=True, text=True),
                 foreground = colors[1],
                 fmt = '{}',
                 decorations=[
                     BorderDecoration(
                         colour = colors[3],
                         border_width = [0, 0, 3, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 4),
        widget.CPU(
                 format = 'cpu:{load_percent}%',
                 foreground = colors[1],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e glances --fahrenheit')},
                 decorations=[
                     BorderDecoration(
                         colour = colors[9],
                         border_width = [0, 0, 3, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 4),
        widget.NvidiaSensors(
                format = 'gpu:{perf}',
                 foreground = colors[1],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e nvtop')},
                 decorations=[
                     BorderDecoration(
                         colour = colors[9],
                         border_width = [0, 0, 3, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 4),
        widget.Memory(
                 #widget12
                 foreground = colors[1],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e glances --fahrenheit')},
                 format = '{MemUsed:.0f}{mm}',
                 fmt = 'memory:{}',
                 measure_mem='M',
                 decorations=[
                     BorderDecoration(
                         colour = colors[12],
                         border_width = [0, 0, 3, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 4),
        widget.DF(
                 update_interval = 60,
                 foreground = colors[1],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e mc ~/')},
                 partition = '/',
                 #format = '[{p}] {uf}{m} ({r:.0f}%)',
                 format = '{uf}{m}',
                 fmt = 'root:{}',
                 visible_on_warn = False,
                 decorations=[
                     BorderDecoration(
                         colour = colors[11],
                         border_width = [0, 0, 3, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 4),
        widget.DF(
                 update_interval = 60,
                 foreground=colors[1],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e mc /secondary')},
                 partition='/secondary',
                 # format='[{p}] {uf}{m} ({r:.0f}%)',
                 format='{uf}{m}',
                 fmt='secondary:{}',
                 visible_on_warn=False,
                 decorations=[
                     BorderDecoration(
                         colour=colors[11],
                         border_width=[0, 0, 3, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 4),        
        widget.Volume(
                 foreground = colors[1],
                 fmt = 'vol:{}',
                 decorations=[
                     BorderDecoration(
                         colour = colors[7],
                         border_width = [0, 0, 3, 0],
                     )
                 ],
                  volume_app = 'pavucontrol',
                 ),
        widget.Spacer(length = 4),
        widget.Clock(
                 foreground = colors[1],
                 format = "%A, %B %d %Y %l:%M%p",
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('proton-mail')},
                 decorations=[
                     BorderDecoration(
                         colour = colors[6],
                         border_width = [0, 0, 3, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 4),
        widget.TextBox(
                #widget22
                text="power menu",
                foreground = colors[1],
                mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('rofi -show power-menu -modi power-menu:rofi-power-menu')},
                decorations=[
                     BorderDecoration(
                         colour = colors[13],
                         border_width = [0, 0, 3, 0],
                     )
                 ],
                ),
        widget.Spacer(length = 2),
        #widget.Systray(padding = 3),
        #widget.Spacer(length = 2),
        ]
    return widgets_list

# Monitor 1 will display ALL widgets in widgets_list. It is important that this
# is the only monitor that displays all widgets because the systray widget will
# crash if you try to run multiple instances of it.
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1 

# All other monitors' bars will display everything but widgets 22 (systray) and 23 (spacer).
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    #del widgets_screen2[22]
    del widgets_screen2[21]
    del widgets_screen2[20]
    del widgets_screen2[19]
    del widgets_screen2[18]
    del widgets_screen2[17]
    del widgets_screen2[16]
    del widgets_screen2[15]
    del widgets_screen2[14]
    del widgets_screen2[13]
    del widgets_screen2[12]
    del widgets_screen2[11]
    del widgets_screen2[10]
    del widgets_screen2[9]
    del widgets_screen2[8]
    del widgets_screen2[7]
    del widgets_screen2[6]
    #del widgets_screen2[5]
    #del widgets_screen2[4]
    #del widgets_screen2[3] spacer widget between groups and widgets
    
    
    return widgets_screen2

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), background="#00000000", size=25)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), background="#00000000", size=25))]
            #Screen(top=bar.Bar(widgets=init_widgets_screen1(), background="#00000000", size=25))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[9],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class='kdenlive'),       # kdenlive
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="notification"),   # notifications
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(wm_class="toolbar"),        # toolbars
        Match(wm_class="Yad"),            # yad boxes
        Match(title="branchdialog"),      # gitk
        Match(title='Confirmation'),      # tastyworks exit box
        Match(title='Qalculate!'),        # qalculate-gtk
        Match(title="pinentry"),          # GPG key password entry
        Match(title="tastycharts"),       # tastytrade pop-out charts
        Match(title="tastytrade"),        # tastytrade pop-out side gutter
        Match(title="tastytrade - Portfolio Report"), # tastytrade pop-out allocation
        Match(wm_class="tasty.javafx.launcher.LauncherFxApp"), # tastytrade settings
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"
