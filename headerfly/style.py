################################################################################
#                                    General
################################################################################


def slash_star(header):
    """Apply c-style block comments (/* */) style to given header."""
    return "\n".join(
        ["/**"] +
        ["  * %s" % line for line in header.split("\n")] +
        ["*/"])


def slash_star_bang(header):
    """Apply non-minifying js-style block comments (/*! */) style to given header."""
    return "\n".join(
        ["/*!"] +
        ["  * %s" % line for line in header.split("\n")] +
        ["*/"])


def scripting(header):
    """Apply scripting comment style (#) to given header."""
    return "\n".join(["# %s" % line if line else "#"
                      for line in header.split("\n")])


def utf_8_scripting(header):
    """Apply utf-8 coding header and scripting comment style (#) to given header."""
    return "\n".join(["# -*- coding: utf-8 -*-", "", scripting(header)])


################################################################################
#                                Language-specific
################################################################################


def html(header):
    """Apply html-style block comments (<!-- -->) style to given header."""
    return "\n".join(
        ["<!--"] +
        ["\t%s" % line for line in header.split("\n")] +
        ["-->"])
