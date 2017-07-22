# logbrowser.py

import znc
from glob import glob
from urllib import parse


class logbrowser(znc.Module):
    module_types = [znc.CModInfo.UserModule]
    description = "Web based log viewer for the log module"

    def GetWebMenuTitle(self):
        return "Log browser"

    def OnWebRequest(self, sock, page, tmpl):
        if str(page) == 'log':
            return self._OnLogRequest(sock, page, tmpl)
        elif str(page) == 'index':
            return self._OnIndexRequest(sock, page, tmpl)
        else:
            return sock.PrintNotFound()

    def _OnIndexRequest(self, sock, page, tmpl):
        network_param = str(sock.GetParam('network', False))
        channel_param = str(sock.GetParam('channel', False))
        network = ''
        channel = ''
        networks = self._GetNetworks(sock)
        if len(networks) == 1:
            network = networks[0]
        elif network_param in networks:
            network = network_param
        tmpl["Network"] = str(network)
        for network_name in networks:
            row = tmpl.AddRow("Networks")
            row["Name"] = str(network_name)
            row["Selected"] = str(str(network_name) == network)
            row['URL'] = self._GetLink(network_name)
        # load channels for network
        if network != '':
            channels = self._GetChannels(sock, network)
            if len(channels) == 1:
                channel = channels[0]
            elif channel_param in channels:
                channel = channel_param
            tmpl["Channel"] = str(channel)
            bc = tmpl.AddRow("BreadCrubs")
            for channel_name in channels:
                row = tmpl.AddRow("Channels")
                row["Name"] = str(channel_name)
                row["Selected"] = str(str(channel_name) == channel)
                row["Network"] = network
                row['URL'] = self._GetLink(network, channel_name)
        # load days for channel
        if network != '' and channel != '':
            days = self._GetDays(sock, network, channel)
            for day in days:
                row = tmpl.AddRow("Days")
                row["Name"] = str(day)
                row["Network"] = network
                row["Channel"] = channel
                row['URL'] = self._GetLink(network, channel, day)
        self._SetBreadCrumbs(tmpl, network, channel)
        return True

    def _OnLogRequest(self, sock, page, tmpl):
        network_param = str(sock.GetParam('network', False))
        channel_param = str(sock.GetParam('channel', False))
        day_param = str(sock.GetParam('day', False))
        networks = self._GetNetworks(sock)
        if not network_param in networks:
            return sock.PrintNotFound()
        channels = self._GetChannels(sock, network_param)
        if not channel_param in channels:
            return sock.PrintNotFound()
        days = self._GetDays(sock, network_param, channel_param)
        if not day_param in days:
            return sock.PrintNotFound()
        with self._OpenLog(sock, network_param, channel_param,
                           day_param) as log:
            for line in log:
                row = tmpl.AddRow("LogLines")
                row["Message"] = line
        self._SetBreadCrumbs(tmpl, network_param, channel_param, day_param)
        return True

    def _SetBreadCrumbs(self, tmpl, network, channel, day=''):
        if network != '':
            row = tmpl.AddRow("BreadCrumbs")
            row['Text'] = str(network)
            row['URL'] = self._GetLink(network)
        if network != '' and channel != '':
            row = tmpl.AddRow("BreadCrumbs")
            row['Text'] = str(channel)
            row['URL'] = self._GetLink(network, channel)
        if network != '' and channel != '' and day != '':
            row = tmpl.AddRow("BreadCrumbs")
            row['Text'] = 'Log for ' + str(day)
            row['URL'] = self._GetLink(network, channel, day)

    def _GetNetworks(self, sock):
        dirs = map(self._GetLastDir, glob(self._GetLogPath(sock) + '*/'))
        return list(dirs)

    def _GetChannels(self, sock, network):
        dirs = map(self._GetLastDir,
                   glob(self._GetLogPath(sock) + network + '/*/'))
        return list(dirs)

    def _GetLink(self, network='', channel='', day=''):
        url = '?' + parse.urlencode({
            'network': network,
            'channel': channel,
            'day': day
        })
        if day != '':
            url = 'log' + url
        url = self.GetWebPath() + url
        return url

    def _GetDays(self, sock, network, channel):
        files = map(
            self._GetLogName,
            glob(self._GetLogPath(sock) + network + '/' + channel + '/*'))
        return files

    def _OpenLog(self, sock, network, channel, day):
        return open(
            self._GetLogPath(sock) + network + '/' + channel + '/' + day +
            '.log')

    def _GetLastDir(self, dir):
        return dir.split('/')[-2]

    def _GetLogName(self, logPath):
        return logPath.split('/')[-1].split('.')[0]

    def _GetLogPath(self, sock):
        # wtf is happening here? this works but y? TODO FIXME
        return sock.GetSession().GetUser().GetUserPath(
        ) + '/moddata/log/' + sock.GetSession().GetUser().GetUserPath(
        ) + '/moddata/log/'