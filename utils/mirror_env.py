import maya.cmds as cmds

global mirror_config


class MIRROR_CONFIG:
    MIRROR_PAIRS = [("L", "R"),
                    ("Left", "Right")]

    def __init__(self):
        self._current_index: int = 0
        self._show_message(self.current_pair)

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
        self._show_message(pair)
        return pair

    def exchange(self, name: str | list[str]) -> list[str]:
        """交换名称中的左右标识符

        Args:
            name: 输入的名称或名称列表

        Returns:
            list[str]: 交换后的名称列表

        Examples:
            >>> self.exchange("L_arm")
            ["R_arm"]
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
                elif name_upper_split[i] == r_upper:
                    name_upper_split[i] = l_upper
            exchanged_name = list("_".join(name_upper_split))

            for char_index in range(len(exchanged_name)):
                if org_cases[char_index] is False:
                    exchanged_name[char_index] = exchanged_name[char_index].lower()
            exchanged_name = "".join(exchanged_name)
            exchange_list.append(exchanged_name)
        return exchange_list

    @staticmethod
    def _show_message(pair):
        message = f"<hl> {pair} </hl>"
        cmds.inViewMessage(amg=message, pos='botRight', fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)

    def __repr__(self):
        return str(self.current_pair)


def mirror_env() -> MIRROR_CONFIG:
    global mirror_config

    try:
        if not isinstance(mirror_config, MIRROR_CONFIG):
            mirror_config = MIRROR_CONFIG()
            print("yes")
    except (NameError, AttributeError):
        mirror_config = MIRROR_CONFIG()

    return mirror_config


def mirror_env_switch():
    global mirror_config
    try:
        mirror_config
        mirror_config.switch_mode()
    except NameError:
        mirror_env()


def mirror_selected(add=False):
    global mirror_config
    mirror_config = mirror_env()
    exchange_list = mirror_config.exchange(cmds.ls(sl=1))
    cmds.select(exchange_list, add=add)
    mirror_config._show_message(mirror_config)
    mirror_config._show_message("Mirror Selected Done")


mirror_env()
