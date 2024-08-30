#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2018 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
#

""" gitlab group tools for cloning all repositories"""

from urllib.request import urlopen, Request
import subprocess
import json
import os
import sys
import shlex
import getpass
import argparse


class GLClone(object):

    """ GitLab Clone all group repositories"""

    def __init__(self, options):
        """ the main program function

        :param options: parser options
        :type options: :class:`argparse.Namespace`
        """
        self.__user = options.user
        self.__grpurl = options.grpurl
        gfilters = options.args or ["tango-ds"]
        self.__filters = [gf.lower() for gf in gfilters]
        self.__token = ""
        if options.tokenfile:
            with open(options.tokenfile) as fl:
                self.__token = fl.read().strip()

    def run(self):
        """ the main program function
        """
        processes = []
        # fetch all subgroups
        groups = []
        page = 1
        found = False
        while page:
            gurl = Request("%s?page=%s" % (self.__grpurl, page))
            if self.__token:
                gurl.add_header('PRIVATE-TOKEN', self.__token)
            glst = json.loads(urlopen(gurl).read().decode())
            if glst:
                groups.extend(glst)
                page += 1
            else:
                page = 0

        for sg in groups:
            found = False
            for flt in self.__filters:
                if sg["full_path"].lower().startswith(flt):
                    found = True
            if found:
                filepath = sg["full_name"].replace(" / ", "/")
                urlpath = sg["full_name"].replace(" / ", "%2F")
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                print("checking %s" % filepath)
                projects = []
                page = 1
                while page:
                    sgurl = Request("%s/%s/projects?page=%s"
                                    % (self.__grpurl, urlpath, page))
                    if self.__token:
                        sgurl.add_header('PRIVATE-TOKEN', self.__token)
                    plst = json.loads(urlopen(sgurl).read().decode())
                    if plst:
                        projects.extend(plst)
                        page += 1
                    else:
                        page = 0
                # fetch all projects of the current subgroup
                for pr in projects:
                    purl = pr["http_url_to_repo"]
                    cwd = ''
                    if not os.path.exists("%s/%s" % (filepath, pr["name"])):
                        clonecmd = 'git clone %s %s/%s' % (
                            purl, filepath, pr["name"])

                    else:
                        cwd = '%s/%s' % (filepath, pr["name"])
                        clonecmd = 'git pull %s' % purl
                    # print("TOKEN %s" % self.__token)
                    if self.__token:
                        if not self.__user:
                            self.__user = getpass.getuser()
                        clonecmd = clonecmd.replace(
                            "://", "://%s:%s@" %
                            (self.__user, self.__token))
                    elif self.__user:
                        clonecmd = clonecmd.replace(
                            "://", "://%s@" % self.__user)
                    # print(clonecmd)
                    try:
                        command = shlex.split(clonecmd)
                        if cwd:
                            p = subprocess.Popen(command, cwd=cwd)
                        else:
                            p = subprocess.Popen(command)
                        processes.append(p)
                    except Exception as e:
                        print("Error on %s: %s" % (purl, str(e)))
            continue
        project = ""
        if not found:
            for sg in groups:
                project = ""
                for flt in self.__filters:
                    sflt = flt.split("/")
                    if sflt:
                        pr = sflt[-1]
                        flt = "/".join(sflt[:-1])
                        if sg["full_path"].lower().startswith(flt):
                            project = pr
                if project:
                    filepath = sg["full_name"].replace(" / ", "/")
                    urlpath = sg["full_name"].replace(" / ", "%2F")
                    if not os.path.exists(filepath):
                        os.makedirs(filepath)
                    print("checking %s" % filepath)
                    projects = []
                    page = 1
                    while page:
                        sgurl = Request("%s/%s/projects?page=%s"
                                        % (self.__grpurl, urlpath, page))
                        if self.__token:
                            sgurl.add_header('PRIVATE-TOKEN', self.__token)
                        plst = json.loads(urlopen(sgurl).read().decode())
                        if plst:
                            projects.extend(plst)
                            page += 1
                        else:
                            page = 0
                    # fetch all projects of the current subgroup
                    for pr in projects:
                        # print("PR", pr["name"].lower(), project.lower())
                        if pr["name"].lower() == project.lower():
                            purl = pr["http_url_to_repo"]
                            cwd = ''
                            if not os.path.exists(
                                    "%s/%s" % (filepath, pr["name"])):
                                clonecmd = 'git clone %s %s/%s' % (
                                    purl, filepath, pr["name"])
                            else:
                                cwd = '%s/%s' % (filepath, pr["name"])
                                clonecmd = 'git pull %s' % purl

                            # print("TOKEN %s" % self.__token)
                            if self.__token:
                                if not self.__user:
                                    self.__user = getpass.getuser()
                                clonecmd = clonecmd.replace(
                                    "://", "://%s:%s@" %
                                    (self.__user, self.__token))
                            elif self.__user:
                                clonecmd = clonecmd.replace(
                                    "://", "://%s@" % self.__user)
                            # print(clonecmd)
                            try:
                                command = shlex.split(clonecmd)
                                if cwd:
                                    p = subprocess.Popen(command, cwd=cwd)
                                else:
                                    p = subprocess.Popen(command)
                                processes.append(p)
                            except Exception as e:
                                print("Error on %s: %s" % (purl, str(e)))

        print("Waiting for subprocesses")
        [p.wait() for p in processes]


def main():
    """ the main program function
    """

    #: pipe arguments
    pipe = ""
    if not sys.stdin.isatty():
        pp = sys.stdin.readlines()
        #: system pipe
        pipe = "".join(pp)

    description = "Command-line tool for cloning all repositories " \
                  "of gitlab (sub-)group"

    epilog = 'examples:\n' \
        '  glclone  -a \n\n' \
        '    - clone all public repositories of "tango-ds" group\n\n' \
        '  glclone  -a -t /home/p00user/private/.token \n\n' \
        '    - clone all repositories of "tango-ds" group\n\n' \
        '  glclone  -a -l  \n\n' \
        '    - clone all public repositories of tango-ds group' \
        ' with gitlab user defined by local user\n\n' \
        '  glclone tango-ds/DeviceClasses \n\n' \
        '    - clone all public repositories of "tango-ds/DeviceClasses" ' \
        'subgroup\n\n' \
        '  glclone tango-ds/DeviceClasses/BeamlineComponents/ABS300 \n\n' \
        '    - clone "tango-ds/DeviceClasses/BeamlineComponents/ABS300" ' \
        'project\n\n'

    parser = argparse.ArgumentParser(
        description=description, epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'args', metavar='filter', type=str, nargs='?',
        help='group filter, e.g. "tango-ds"')
    parser.add_argument(
        "-u", "--user",
        help="gitlab user",
        dest="user", default="")
    parser.add_argument(
        "-t", "--token-file",
        help="token file",
        dest="tokenfile", default="")
    parser.add_argument(
        "-g", "--groupurl",
        help='group url, '
        'default: "https://gitlab.desy.de/api/v4/groups"',
        dest="grpurl", default="https://gitlab.desy.de/api/v4/groups")
    parser.add_argument(
        "-l", "--local-user", action="store_true",
        default=False, dest="local",
        help="get local user")
    parser.add_argument(
        "-a", "--all", action="store_true",
        default=False, dest="all",
        help="set filter to 'tango-ds'")

    try:
        options = parser.parse_args()
    except Exception as e:
        sys.stderr.write("Error: %s\n" % str(e))
        sys.stderr.flush()
        parser.print_help()
        print("")
        sys.exit(255)

    #: command-line and pipe arguments
    parg = []
    if hasattr(options, "args"):
        parg = [options.args] if options.args else []
    if pipe:
        parg.append(pipe)
    if options.all:
        parg.append("tango-ds")
    options.args = parg

    if not options.args:
        parser.print_help()
        print("")
        sys.exit(255)

    if not options.user and options.local:
        options.user = getpass.getuser()
    try:
        command = GLClone(options)
        command.run()
    except Exception as e:
        sys.stderr.write("Error: glclone interrupted with:")
        sys.stderr.write(str(e))
        sys.stderr.flush()
        sys.exit(255)


if __name__ == "__main__":
    main()
