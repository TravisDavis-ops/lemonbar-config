""" Script to display data to lemonbar
    Author: Zander Blasingame """

# imports
import time
import sys
import subprocess
import json
from subprocess import check_output


# PARAMETERS
SPACING_RIGHT = 3
SPACING_LEFT = 3

RIGHT_MARGIN = ' ' * 4
LEFT_MARGIN = ' ' * 4


################################################################################
#
# Functions for getting stats
#
################################################################################

# helper function
def call(cmd):
    return check_output(cmd.split()).decode('utf-8')


def clock():
    return time.strftime('%a %b %d, %T')


def battery():
    bat_str = call('acpi --battery').split()
    charging = True if bat_str[2] == 'Charging,' else False

    charge = int(bat_str[3].split('%')[0])

    if charge < 10:
        symbol = '\uf244'
    elif charge < 37:
        symbol = '\uf243'
    elif charge < 68:
        symbol = '\uf242'
    elif charge < 90:
        symbol = '\uf241'
    else:
        symbol = '\uf240'

    if charging:
        symbol += ' \uf0e7'

    return symbol + ' ' + str(charge) + '%'


def audio():
    audio_str = call('amixer get Master').split()
    mute = True if audio_str[-1] == '[off]' else False

    # get if audio jack is plugged or not
    amixer = subprocess.Popen('amixer -c 0 contents'.split(),
                              stdout=subprocess.PIPE)
    numid = subprocess.check_output(['grep', 'Headphone.*Jack'],
                                    stdin=amixer.stdout).decode('utf-8')
    numid = numid.split(',')[0]

    plugged = call('amixer -c 0 cget {}'.format(numid)).split('\n')[-2][-2:]

    headphone = '\uf025 ' if plugged == 'on' else ''

    level = int(audio_str[-3][1:-2])

    if mute:
        symbol = '\uf026'
    elif level < 50:
        symbol = '\uf027'
    else:
        symbol = '\uf028'

    return headphone + symbol + ' ' + str(level) + '%'


def workspaces():
    workspace_str = call('i3-msg -t get_workspaces')
    data = json.loads(workspace_str)

    disp = ''

    for entry in data:
        symbol = '\uf111' if entry['visible'] else '\uf10c'
        disp = '{}{:5s}'.format(disp, symbol)

    return disp


def ram():
    ram_str = call('free -m').split('\n')[1]

    used = float(ram_str.split()[2]) / 1000

    return '\uf0ae {:.1f}GB'.format(used)


def cpu():
    cpu_stats = call('mpstat').split('\n')[-2].split()

    user = float(cpu_stats[3])
    nice = float(cpu_stats[4])
    system = float(cpu_stats[5])

    return '\uf085 {:.2f}%'.format(user + nice + system)


def network():
    net_str = call('iwgetid -r')

    disp = '\uf1eb'
    disp += ' Connected' if not net_str == '' else 'Disconnected'

    return disp


def brightness():
    level = float(call('xbacklight -get'))

    return '\uf0eb {}%'.format(round(level))


def current_window():
    id = call('xprop -root _NET_ACTIVE_WINDOW').split(' ')[-1]

    try:
        content = call('xprop -id {}'.format(id)).split('\n')

    except subprocess.CalledProcessError:
        return ''

    name = next(entry for entry in content if 'WM_NAME(UTF8_STRING)' in entry)
    name = name.split('=')[-1][2:-1]

    return name 


def create_right(*args):
    right_str = '{}'

    for i in range(len(args) - 1):
        right_str += ' ' * SPACING_RIGHT + '{}'

    return right_str.format(*args)


def create_left(*args):
    left_str = '{}'

    for i in range(len(args) - 1):
        left_str += ' ' * SPACING_LEFT + '{}'

    return left_str.format(*args)


################################################################################
#
# Main function
#
################################################################################

def main():
    dispStr = '%{{l}}{}{}'.format(LEFT_MARGIN, create_left(clock(),
                                                           current_window()))

    dispStr += '%{{c}}{}'.format(workspaces())
    dispStr += '%{{r}}{}{}'.format(create_right(network(),
                                                cpu(),
                                                ram(),
                                                brightness(),
                                                audio(),
                                                battery()),
                                 RIGHT_MARGIN)

    print(dispStr)


if __name__ == '__main__':
    main()

