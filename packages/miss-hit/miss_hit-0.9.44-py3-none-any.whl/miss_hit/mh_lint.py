#!/usr/bin/env python3
##############################################################################
##                                                                          ##
##          MATLAB Independent, Small & Safe, High Integrity Tools          ##
##                                                                          ##
##              Copyright (C) 2020-2022, Florian Schanda                    ##
##                                                                          ##
##  This file is part of MISS_HIT.                                          ##
##                                                                          ##
##  MATLAB Independent, Small & Safe, High Integrity Tools (MISS_HIT) is    ##
##  free software: you can redistribute it and/or modify                    ##
##  it under the terms of the GNU Affero General Public License as          ##
##  published by the Free Software Foundation, either version 3 of the      ##
##  License, or (at your option) any later version.                         ##
##                                                                          ##
##  MISS_HIT is distributed in the hope that it will be useful,             ##
##  but WITHOUT ANY WARRANTY; without even the implied warranty of          ##
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           ##
##  GNU Afferto General Public License for more details.                    ##
##                                                                          ##
##  You should have received a copy of the GNU Affero General Public        ##
##  License along with MISS_HIT. If not, see                                ##
##  <http://www.gnu.org/licenses/>.                                         ##
##                                                                          ##
##############################################################################

import os

from miss_hit_core import pathutil
from miss_hit_core import command_line
from miss_hit_core import work_package
from miss_hit_core import cfg_tree
from miss_hit_core.m_ast import *
from miss_hit_core.errors import (Error,
                                  Message_Handler,
                                  HTML_Message_Handler,
                                  JSON_Message_Handler)
from miss_hit_core.m_lexer import MATLAB_Lexer
from miss_hit_core.m_parser import MATLAB_Parser
from miss_hit_core.m_language_builtins import BUILTIN_FUNCTIONS

from miss_hit.m_sem import sem_pass_1


class Stage_1_Linting(AST_Visitor):
    """ Checks which do not require semantic analysis """
    def __init__(self, mh):
        self.mh = mh

    def visit(self, node, n_parent, relation):
        if isinstance(node, Compilation_Unit):
            self.check_compilation_unit(node)
        elif isinstance(node, Special_Block) and node.kind() == "methods":
            self.check_methods_block(node)

    def check_compilation_unit(self, n_cu):
        assert isinstance(n_cu, Compilation_Unit)

        # Check that filename matches the primary entity
        if isinstance(n_cu, Function_File):
            self.check_filename(file_name = n_cu.name,
                                kind      = "function",
                                ent_name  = n_cu.l_functions[0].n_sig.n_name)
        elif isinstance(n_cu, Class_File):
            self.check_filename(file_name = n_cu.name,
                                kind      = "class",
                                ent_name  = n_cu.n_classdef.n_name)

        # Check that Contents.m doesn't contain anything but
        # comments. We do this case-insensitive to make sure this
        # nobody slips in a "ConTENTS.m" file on Linux that would
        # cause issues in Windows.
        if n_cu.name.lower() == "contents.m":
            error_loc = None
            if isinstance(n_cu, Script_File):
                # No need to check functions, a script file with no
                # statements would be a functin file OR a blank file
                is_blank = len(n_cu.n_statements.l_statements) == 0
                if not is_blank:
                    error_loc = n_cu.n_statements.l_statements[0].loc()

            elif isinstance(n_cu, Function_File):
                # Function files are always a problem
                is_blank = False
                error_loc = n_cu.l_functions[0].loc()

            elif isinstance(n_cu, Class_File):
                # Class files are also always a problem
                is_blank = False
                error_loc = n_cu.n_classdef.loc()

            if not is_blank:
                self.mh.check(error_loc,
                              "a Contents.m file must only contain comments",
                              "malformed_contents",
                              "low")

    def check_methods_block(self, n_block):
        assert isinstance(n_block, Special_Block) and \
            n_block.kind() == "methods"

        # Check that TestTags is well formed. Otherwise MATLAB can
        # silently ignore these tests when you form a suite.
        test_tags = n_block.get_attribute("TestTags")
        if test_tags:
            n_value = test_tags.n_value
            if isinstance(n_value, Matrix_Expression):
                n_rows = n_value.n_content
            elif isinstance(n_value, Cell_Expression):
                n_rows = n_value.n_content
            else:
                self.mh.check(n_value.loc(),
                              "TestTags must be a matrix or cell expression",
                              "malformed_test_tags",
                              "high")
                n_rows = None

            if n_rows is not None and len(n_rows.l_items) != 1:
                self.mh.check(n_value.loc(),
                              "TestTags must contain precisely one row",
                              "malformed_test_tags",
                              "high")

            if n_rows:
                for n_row in n_rows.l_items:
                    for n_item in n_row.l_items:
                        if isinstance(n_value, Matrix_Expression) and \
                           not isinstance(n_item, String_Literal):
                            self.mh.check(n_item.loc(),
                                          "expressions in matrix TestTags must"
                                          " be strings",
                                          "malformed_test_tags",
                                          "high")
                        elif isinstance(n_value, Cell_Expression) and \
                             not isinstance(n_item, Char_Array_Literal):
                            self.mh.check(n_item.loc(),
                                          "expressions in cell TestTags must"
                                          " be character arrays",
                                          "malformed_test_tags",
                                          "high")

    def check_filename(self, file_name, kind, ent_name):
        assert isinstance(file_name, str)
        assert isinstance(ent_name, Name) and ent_name.is_simple_dotted_name()

        base_filename, ext = os.path.splitext(file_name)

        if ext != ".m":
            # This check is not applicable for MATLAB embedded in
            # Simulink models
            pass
        elif base_filename != str(ent_name):
            self.mh.check(ent_name.loc(),
                          "%s name does not match the filename %s" %
                          (kind, base_filename),
                          "filename_primary_entity_name",
                          "low")


class MH_Lint_Result(work_package.Result):
    def __init__(self, wp, sem=None):
        super().__init__(wp, True)
        self.sem = sem


class MH_Lint(command_line.MISS_HIT_Back_End):
    def __init__(self, options):
        super().__init__("MH Lint")
        self.perform_sem = options.entry_point is not None
        self.debug_show_st = options.debug_show_global_symbol_table

    @classmethod
    def process_wp(cls, wp):
        # Create lexer
        lexer = MATLAB_Lexer(wp.cfg.language,
                             wp.mh,
                             wp.get_content(),
                             wp.filename,
                             wp.blockname)
        if not wp.cfg.pragmas:
            lexer.process_pragmas = False
        if len(lexer.text.strip()) == 0:
            return MH_Lint_Result(wp)

        # Create parse tree
        try:
            parser = MATLAB_Parser(wp.mh, lexer, wp.cfg)
            n_cu = parser.parse_file()
        except Error:
            return MH_Lint_Result(wp)

        # Check compilation units for shadowing a built-in
        base_name = os.path.splitext(n_cu.name)[0]
        dir_name = os.path.basename(os.path.dirname(
            pathutil.abspath(wp.filename)))
        if wp.cfg.active("builtin_shadow") and \
           base_name in BUILTIN_FUNCTIONS and \
           not (dir_name.startswith("+") or dir_name.startswith("@")):
            wp.mh.check(n_cu.loc(),
                        "this file shadows built-in %s which is very naughty"
                        % base_name,
                        "builtin_shadow",
                        "high")

        # Initial checks
        n_cu.visit(None, Stage_1_Linting(wp.mh), "Root")

        # First pass of semantic analysis
        entrypoint = cfg_tree.get_entry_point(wp.options.entry_point)
        sem = sem_pass_1(wp.mh, entrypoint, n_cu)

        return MH_Lint_Result(wp, sem)

    def process_result(self, result):
        if not self.perform_sem:
            return
        if not isinstance(result, MH_Lint_Result):
            return
        if result.sem is None:
            return

        if self.debug_show_st:
            result.sem.scope.dump(result.wp.filename)

    def post_process(self):
        pass


def main_handler():
    clp = command_line.create_basic_clp()

    # Extra output options
    clp["output_options"].add_argument(
        "--html",
        default=None,
        help="Write report to given file as HTML")
    clp["output_options"].add_argument(
        "--json",
        default=None,
        help="Produce JSON report")

    # Extra debug options
    clp["debug_options"].add_argument(
        "--debug-show-global-symbol-table",
        default=False,
        action="store_true",
        help="Show global symbol table")

    options = command_line.parse_args(clp)

    if options.html:
        if options.json:
            clp["ap"].error("Cannot produce JSON and HTML at the same time")
        if os.path.exists(options.html) and not os.path.isfile(options.html):
            clp["ap"].error("Cannot write to %s: it is not a file" %
                            options.html)
        mh = HTML_Message_Handler("lint", options.html)
    elif options.json:
        if os.path.exists(options.json) and not os.path.isfile(options.json):
            clp["ap"].error("Cannot write to %s: it is not a file" %
                            options.json)
        mh = JSON_Message_Handler("lint", options.json)
    else:
        mh = Message_Handler("lint")

    mh.show_context = not options.brief
    mh.show_style   = False
    mh.show_checks  = True
    mh.autofix      = False

    lint_backend = MH_Lint(options)
    command_line.execute(mh, options, {}, lint_backend)


def main():
    command_line.ice_handler(main_handler)


if __name__ == "__main__":
    main()
