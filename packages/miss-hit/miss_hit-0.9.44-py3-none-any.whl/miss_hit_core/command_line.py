#!/usr/bin/env python3
##############################################################################
##                                                                          ##
##          MATLAB Independent, Small & Safe, High Integrity Tools          ##
##                                                                          ##
##              Copyright (C) 2020-2024, Florian Schanda                    ##
##              Copyright (C) 2023,      BMW AG                             ##
##                                                                          ##
##  This file is part of MISS_HIT.                                          ##
##                                                                          ##
##  MATLAB Independent, Small & Safe, High Integrity Tools (MISS_HIT) is    ##
##  free software: you can redistribute it and/or modify it under the       ##
##  terms of the GNU General Public License as published by the Free        ##
##  Software Foundation, either version 3 of the License, or (at your       ##
##  option) any later version.                                              ##
##                                                                          ##
##  MISS_HIT is distributed in the hope that it will be useful,             ##
##  but WITHOUT ANY WARRANTY; without even the implied warranty of          ##
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           ##
##  GNU General Public License for more details.                            ##
##                                                                          ##
##  You should have received a copy of the GNU General Public License       ##
##  along with MISS_HIT. If not, see <http://www.gnu.org/licenses/>.        ##
##                                                                          ##
##############################################################################

# This is the common command-line handling for all MISS_HIT tools.

import os
import sys
import argparse
import traceback
import textwrap
import multiprocessing
import functools

from miss_hit_core import pathutil
from miss_hit_core import cfg_tree
from miss_hit_core import errors
from miss_hit_core import work_package
from miss_hit_core import s_ast

from miss_hit_core.version import GITHUB_ISSUES, VERSION, FULL_NAME
from miss_hit_core.m_language import (Base_MATLAB_Language,
                                      Base_Octave_Language)


def has_relevant_extension(path, process_slx=True):
    assert isinstance(path, str)
    assert isinstance(process_slx, bool)

    if process_slx:
        return os.path.splitext(path)[1] in (".m", ".tst", ".slx")
    else:
        return os.path.splitext(path)[1] in (".m", ".tst")


def create_basic_clp(epilog=None):
    rv = {}

    ap = argparse.ArgumentParser(
        description="MATLAB Independent, Small & Safe, High Integrity Tools",
        epilog=epilog)
    rv["ap"] = ap

    ap.add_argument("-v", "--version",
                    action="store_true",
                    default=False,
                    help="Show MISS_HIT version and exit")

    language_options = ap.add_mutually_exclusive_group()
    language_options.add_argument("--octave",
                                  default=None,
                                  metavar="VERSION",
                                  help=("Enable support for the Octave"
                                        " language at a given version,"
                                        " e.g. 4.4. If no version is specified"
                                        " then latest supported is used."))

    language_options.add_argument("--matlab",
                                  default=None,
                                  metavar="VERSION",
                                  help=("Enable support for the MATLAB"
                                        " language at a given version,"
                                        " e.g. 2021a. If no version is "
                                        " specified then the latest supported"
                                        " is used."))

    ap.add_argument("--include-version",
                    action="store_true",
                    default=False,
                    help=("Include version number in output, can helpful to"
                          " debug CI issues"))
    ap.add_argument("files",
                    metavar="FILE|DIR",
                    nargs="*",
                    help="MATLAB/Simulink files or directories to analyze")
    ap.add_argument("--entry-point",
                    metavar="ENTRY_POINT_NAME",
                    default=None,
                    help=("Set MATLAB entry point. Required for any advanced"
                          " static analysis."))
    ap.add_argument("--single",
                    action="store_true",
                    default=False,
                    help="Do not use multi-threaded analysis")
    ap.add_argument("--ignore-config",
                    action="store_true",
                    default=False,
                    help=("Ignore all %s files." %
                          " or ".join(cfg_tree.CONFIG_FILENAMES)))
    ap.add_argument("--input-encoding",
                    default="cp1252",
                    help=("By default we use cp1252 to read m files, but this"
                          " can be changed to any valid encoding."))

    pragma_options = ap.add_argument_group("pragma options")
    rv["pragmas"] = pragma_options

    pragma_options.add_argument(
        "--ignore-pragmas",
        default=False,
        action="store_true",
        help=("Disable special treatment of MISS_HIT pragmas. These are"
              " comments that start with '%% mh:'"))

    pragma_options.add_argument(
        "--ignore-justifications-with-tickets",
        default=False,
        action="store_true",
        help=("Ignore any justifications that mention a ticket, as they are"
              " likely to be temporary justifications that need to be"
              " resolved later."))

    output_options = ap.add_argument_group("output options")
    rv["output_options"] = output_options

    output_options.add_argument("--brief",
                                action="store_true",
                                default=False,
                                help="Don't show line-context on messages")

    debug_options = ap.add_argument_group("debugging options")
    rv["debug_options"] = debug_options

    debug_options.add_argument("--debug-show-path",
                               default=False,
                               action="store_true",
                               help=("Show PATH used for function/class"
                                     " searching."))

    return rv


def parse_args(clp):
    options = clp["ap"].parse_args()

    if options.version or options.include_version:
        print(FULL_NAME)
        if options.version:
            sys.exit(0)

    # False alarm from pylint
    # pylint: disable=no-member
    if (not options.brief and
        sys.stdout.encoding.lower() != "utf-8"):  # pragma: no cover
        print("WARNING: It looks like your environment is not set up quite")
        print("         right since python will encode to %s on stdout." %
              sys.stdout.encoding)
        print()
        print("To fix set one of the following environment variables:")
        print("   LC_ALL=en_GB.UTF-8 (or something similar)")
        print("   PYTHONIOENCODING=UTF-8")

    for item in options.files:
        if not (os.path.isdir(item) or os.path.isfile(item)):
            clp["ap"].error("%s is neither a file nor directory" % item)

    try:
        "potato".encode(options.input_encoding)
    except LookupError:
        clp["ap"].error("invalid encoding '%s'" % options.input_encoding)

    options.language = None
    if options.octave is not None:
        try:
            major, minor = Base_Octave_Language.parse_version(options.octave)
            options.language = Base_Octave_Language.get_version(major, minor)
        except ValueError as verr:
            clp["ap"].error(verr.args[0])
        del options.octave
    if options.matlab is not None:
        try:
            major, minor = Base_MATLAB_Language.parse_version(options.matlab)
            options.language = Base_MATLAB_Language.get_version(major, minor)
        except ValueError as verr:
            clp["ap"].error(verr.args[0])
        del options.matlab

    return options


class MISS_HIT_Back_End:
    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name

    @classmethod
    def process_wp(cls, wp):
        return work_package.Result(wp, False)

    @classmethod
    def process_simulink_wp(cls, wp):
        return work_package.Result(wp, False)

    def process_result(self, result):
        pass

    def post_process(self):
        pass


def dispatch_wp(process_m_fn, process_s_fn, wp):
    results = []

    try:
        if not wp.cfg.enabled:
            wp.mh.register_exclusion(wp.filename)
            results.append(work_package.Result(wp, False))

        elif isinstance(wp, work_package.SIMULINK_File_WP):
            wp.register_file()
            try:
                wp.parse_simulink()
            except errors.Error:
                results.append(work_package.Result(wp, False))
                return results
            if wp.n_content:
                for block in wp.n_content.iter_all_blocks():
                    if isinstance(block, s_ast.Matlab_Function):
                        block_wp = work_package.Embedded_MATLAB_WP(wp, block)
                        block_wp.register_file()
                        results.append(process_m_fn(block_wp))
            results.append(process_s_fn(wp))
            if wp.modified:
                wp.save_and_close()

        elif isinstance(wp, work_package.MATLAB_File_WP):
            wp.register_file()
            results.append(process_m_fn(wp))

        else:
            raise errors.ICE("unknown work package kind %s" %
                             wp.__class__.__name__)

    except errors.Error as err:
        raise errors.ICE("uncaught Error in process_generic_wp") from err

    return results


def execute(mh, options, extra_options, back_end,
            process_slx=True,
            process_tests=False):
    assert isinstance(mh, errors.Message_Handler)
    assert isinstance(back_end, MISS_HIT_Back_End)

    try:
        if options.entry_point:
            # If an entry point is specified, config parsing is quite
            # different. We go find the project root and from there
            # build a config tree.
            cfg_tree.register_item(mh,
                                   pathutil.abspath("."),
                                   options)
            prj_root = cfg_tree.get_root(pathutil.abspath("."))
            cfg_tree.register_item(mh,
                                   prj_root,
                                   options)
            cfg_tree.validate_project_config(mh)

            # Make sure the entry point specified exists
            n_ep = cfg_tree.get_entry_point(options.entry_point)
            if n_ep is None:
                mh.command_line_error("Entry point or library '%s' does "
                                      "not exist." %
                                      options.entry_point)

            # Get PATH
            item_list = [(False, item)
                         for item in cfg_tree.get_source_path(n_ep)]
            if process_tests:
                item_list += [(True, item)
                              for item in cfg_tree.get_test_path(n_ep)]

            if options.debug_show_path:
                print("Using the following PATH:")
                for _, path in item_list:
                    print("> %s" % os.path.relpath(path))

            # Determine relevant files based on these
            # directories. This is a bit more complex than
            # "everything".
            #
            # See
            # https://www.mathworks.com/help/matlab/matlab_env/files-and-folders-that-matlab-accesses.html

            code_in_path = set()
            test_in_path = set()
            for in_test_dir, path_root in item_list:
                container = test_in_path if in_test_dir else code_in_path
                for path, dirs, files in os.walk(path_root):
                    container.add(os.path.normpath(path))
                    for f in files:
                        if has_relevant_extension(f):
                            container.add(
                                os.path.normpath(os.path.join(path, f)))
                    irrelevant_dirs = set(d for d in dirs
                                          if not (d.startswith("+") or
                                                  d.startswith("@") or
                                                  d == "private"))
                    for idir in irrelevant_dirs:
                        dirs.remove(idir)

            if options.files:
                # If the user has supplied files/dirs to analyze, we
                # only do that if they are part of _this_ entrypoint.
                item_list = []
                for item in options.files:
                    if pathutil.abspath(item) in code_in_path:
                        item_list.append((False, item))
                    elif pathutil.abspath(item) in test_in_path:
                        item_list.append((True, item))
                    else:
                        mh.command_line_error("'%s' is not part of "
                                              "entry point %s" %
                                              (item, options.entry_point))
            else:
                # Otherwise we look at all applicable files on the
                # path.
                item_list = [(False, item)
                             for item in sorted(code_in_path)
                             if has_relevant_extension(item)]
                item_list += [(True, item)
                              for item in sorted(test_in_path)
                              if has_relevant_extension(item)]

            # Post-process to use relative directories
            item_list = [(in_test_dir, os.path.relpath(item))
                         for in_test_dir, item in item_list]

        else:
            # Without an entry point, we build a minimally sufficient
            # tree to analyse what we have. We loop over
            # files/directories from the command-line and parse
            # configuration.

            if options.files:
                item_list = [(False, item)
                             for item in list(options.files)]
            else:
                item_list = [(False, ".")]

            for in_test_dir, item in item_list:
                if os.path.isdir(item) or os.path.isfile(item):
                    cfg_tree.register_item(mh,
                                           pathutil.abspath(item),
                                           options)

        mh.reset_seen()

    except errors.Error:
        mh.summary_and_exit()

    # Loop over files/directories from the command-line again, and
    # build a list of work packages.

    work_list = []
    for in_test_dir, item in item_list:
        if os.path.isdir(item):
            for path, dirs, files in os.walk(item):
                dirs.sort()
                for excluded_dir in cfg_tree.get_excluded_directories(path):
                    if os.path.exists(os.path.join(path, excluded_dir)):
                        dirs.remove(excluded_dir)
                hidden_dirs = [d for d in dirs if d.startswith(".")]
                for hidden_dir in hidden_dirs:
                    dirs.remove(hidden_dir)

                if path == ".":
                    path = ""

                for f in sorted(files):
                    if not os.path.isfile(os.path.join(path, f)):
                        # This removes broken symlinks
                        continue
                    if has_relevant_extension(f, process_slx):
                        work_list.append(
                            work_package.create(in_test_dir,
                                                os.path.join(path, f),
                                                options.input_encoding,
                                                mh,
                                                options, extra_options))

        elif has_relevant_extension(item, process_slx):
            work_list.append(work_package.create(in_test_dir,
                                                 item,
                                                 options.input_encoding,
                                                 mh,
                                                 options, extra_options))

        else:
            pass

    # Resolve all work packages, using single or multi-threading (the
    # default) as demanded.

    process_fn = functools.partial(dispatch_wp,
                                   back_end.process_wp,
                                   back_end.process_simulink_wp)

    if options.single:
        for wp in work_list:
            for result in process_fn(wp):
                assert isinstance(result, work_package.Result)
                mh.integrate(result.wp.mh)
                if result.processed:
                    mh.finalize_file(result.wp.filename)
                    back_end.process_result(result)

    else:
        with multiprocessing.Pool() as pool:
            for results in pool.imap(process_fn, work_list, 5):
                for result in results:
                    assert isinstance(result, work_package.Result)
                    mh.integrate(result.wp.mh)
                    if result.processed:
                        mh.finalize_file(result.wp.filename)
                        back_end.process_result(result)

    # Call hook for final work and issue summary message

    back_end.post_process()
    mh.summary_and_exit()


def ice_handler(main_function):
    try:
        main_function()
    except errors.ICE as internal_compiler_error:  # pragma: no cover
        traceback.print_exc()
        print("-" * 70)
        print("- Encountered an internal compiler error. This is a tool")
        print("- bug, please report it on our github issues so we can fix it:")
        print("-")
        print("-    %s" % GITHUB_ISSUES)
        print("-")
        print("- Please include the above backtrace in your bug report, and")
        print("- the following information:")
        print("-")
        print("- MISS_HIT version: %s" % VERSION)
        print("-")
        lines = textwrap.wrap(internal_compiler_error.reason)
        print("\n".join("- %s" % line for line in lines))
        print("-" * 70)
