import maya.cmds as cmds
from face.fn.showMessage import showMessage


class MIRROR_BASE:
    MIRROR_PAIRS = [("L", "R"),
                    ("Left", "Right")]

    def __init__(self):
        self._current_index = 0

    @property
    def current_pair(self):
        return self.MIRROR_PAIRS[self._current_index % len(self.MIRROR_PAIRS)]

    @property
    def l(self):
        return self.current_pair[0]

    @property
    def r(self):
        return self.current_pair[1]

    def switch_mode(self):
        self._current_index += 1
        pair = self.current_pair
        showMessage(pair)
        return pair

    def exchange(self, name):
        if isinstance(name, basestring):
            name = [name]

        exchange_list = []
        for n in name:
            org_cases = [s.isupper() for s in n]

            l_upper = self.l.upper()
            r_upper = self.r.upper()
            name_upper = n.upper()
            name_upper_split = name_upper.split("_")

            for i in range(len(name_upper_split)):
                if name_upper_split[i] == l_upper:
                    name_upper_split[i] = r_upper
                    if l_upper == "left".upper():
                        org_cases.insert(4, org_cases[3])
                    continue
                elif name_upper_split[i] == r_upper:
                    name_upper_split[i] = l_upper
                    if r_upper == "right".upper():
                        del org_cases[4]
                    continue
            exchanged_name = list("_".join(name_upper_split))

            for char_index in range(len(exchanged_name)):
                if org_cases[char_index] is False:
                    exchanged_name[char_index] = exchanged_name[char_index].lower()
            exchanged_name = "".join(exchanged_name)
            exchange_list.append(exchanged_name)
        return exchange_list

    def __repr__(self):
        return str(self.current_pair)


def mirror_selected(add=False):
    exchange_list = MIRROR_CONFIG.exchange(cmds.ls(sl=1))
    cmds.select(exchange_list, add=add)
    showMessage(MIRROR_CONFIG)
    showMessage("Mirror Selected Done")


MIRROR_CONFIG = MIRROR_BASE()
