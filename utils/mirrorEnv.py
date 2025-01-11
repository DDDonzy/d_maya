import maya.cmds as cmds
from utils.showMessage import showMessage


class MIRROR_BASE:
    MIRROR_PAIRS = [("L", "R"),
                    ("Left", "Right")]

    def __init__(self):
        self._current_index: int = 0
        showMessage(self.current_pair)

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

    def exchange(self, name: list) -> list:
        """Exchange left/right identifiers in names

        Args:
            name (str|list): Input name or list of names to process

        Returns:
            list[str]: List of names with left/right identifiers swapped

        Examples:
            >>> self.exchange("L_arm")
            return: ["R_arm"]
            >>> self.exchange(["L_arm", "R_leg"])
            return: ["R_arm", "L_leg"]
        """
        if isinstance(name, str):
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
                    continue
                elif name_upper_split[i] == r_upper:
                    name_upper_split[i] = l_upper
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


global MIRROR_CONFIG
MIRROR_CONFIG = MIRROR_BASE()

