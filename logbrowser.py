# logbrowser.py

import znc
import os
from glob import glob


class logbrowser(znc.Module):
    module_types = [znc.CModInfo.UserModule]
    description = "Web based log viewer for the log module"

    def GetWebMenuTitle(self):
        return "Log browser"

    def OnWebRequest(self, sock, page, tmpl):
        if str(page) == 'log':
            return self._OnLogRequest(sock, page, tmpl)
        else:
            return self._OnIndexRequest(sock, page, tmpl)

    def _OnLogRequest(self, sock, page, tmpl):
        return True

    def _OnIndexRequest(self, sock, page, tmpl):
        network_param = str(sock.GetParam('network', False))
        channel_param = str(sock.GetParam('channel', False))
        networks = self._GetNetworks(sock)
        if len(networks) == 1:
            network = networks[0]
        elif network_param in networks:
            network = network_param
        else:
            network = ''
        tmpl["Network"] = str(network)
        for network_name in networks:
            row = tmpl.AddRow("Networks")
            row["Name"] = str(network_name)
            row["Selected"] = str(str(network_name) == network)
        # load channels for network
        if network != '':
            channels = self._GetChannels(sock, network)
            if len(channels) == 1:
                channel = channels[0]
            elif channel_param in channels:
                channel = channel_param
            else:
                channel = ''
            tmpl["Channel"] = str(channel)
            for channel_name in channels:
                row = tmpl.AddRow("Channels")
                row["Name"] = str(channel_name)
                row["Selected"] = str(str(channel_name) == channel)
                row["Network"] = network
        # load days for channel
        if network != '' and channel != '':
            days = self._GetDays(sock, network, channel)
            for day in days:
                row = tmpl.AddRow("Days")
                row["Name"] = str(day)
                row["Network"] = network
                row["Channel"] = channel
        return True

    def _GetNetworks(self, sock):
        dirs = map(self._GetLastDir, glob(self._GetLogPath(sock) + '*/'))
        return list(dirs)

    def _GetChannels(self, sock, network):
        dirs = map(self._GetLastDir,
                   glob(self._GetLogPath(sock) + network + '/*/'))
        return list(dirs)

    def _GetDays(self, sock, network, channel):
        files = map(
            self._GetLogName,
            glob(self._GetLogPath(sock) + network + '/' + channel + '/*'))
        return files

    def _GetLastDir(self, dir):
        return dir.split('/')[-2]

    def _GetLogName(self, logPath):
        return logPath.split('/')[-1].split('.')[0]

    def _GetLogPath(self, sock):
        # wtf is happening here? this works but y? TODO FIXME
        return sock.GetSession().GetUser().GetUserPath(
        ) + '/moddata/log/' + sock.GetSession().GetUser().GetUserPath(
        ) + '/moddata/log/'