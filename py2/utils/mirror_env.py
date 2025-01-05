# coding: utf-8
from maya import cmds


class MIRROR_CONFIG(object):
    def __init__(self, l="L", r="R"):
        self.l = l
        self.r = r
        self.current_pair = (self.l, self.r)

    def exchange(self, name):
        """交换名称中的左右标识符

        Args:
            name: 输入的名称或名称列表

        Returns:
            list[str]: 交换后的名称列表

        Examples:
            >>> self.exchange("L_arm")
            return: ["R_arm"]
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

    @staticmethod
    def _show_message(pair):
        message = "<hl> {0} </hl>".format(pair)
        cmds.inViewMessage(amg=message, pos='botRight', fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)

    def __repr__(self):
        return str(self.current_pair)


def mirror_selected(add=False):
    exchange_list = mirror_config.exchange(cmds.ls(sl=1))
    cmds.select(exchange_list, add=add)
    mirror_config._show_message(mirror_config)
    mirror_config._show_message("Mirror Selected Done")


global mirror_config
mirror_config = MIRROR_CONFIG()
