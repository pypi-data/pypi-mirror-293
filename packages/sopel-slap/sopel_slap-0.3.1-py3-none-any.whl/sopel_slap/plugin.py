"""Sopel Slap plugin

Plugin for Sopel that lets users slap each other in fun ways.

Original slap.py copyright 2009, Michael Yanovich, yanovich.net.

This reworked version for Sopel 7.1+ copyright 2024, dgw, technobabbl.es

https://sopel.chat
"""
from __future__ import annotations

from sopel import plugin

from .config import SlapSection, do_configure
from .util import slap


def setup(bot):
    bot.settings.define_section('slap', SlapSection)


def configure(settings):
    settings.define_section('slap', SlapSection)
    do_configure(settings.slap)


@plugin.commands('slap', 'slaps')
def slap_command(bot, trigger):
    """Slap a <target> (e.g. nickname)"""
    target = trigger.group(3)

    if target is None:
        target = trigger.nick

    return slap(bot, trigger, target)


@plugin.ctcp('ACTION')
@plugin.rule(r'^slaps (\S+)$')
def slap_action(bot, trigger):
    """Slap someone using the power of CTCP ACTION."""
    target = trigger.group(1)

    if target is None:
        # no self-slaps via /me; just fail silently
        return plugin.NOLIMIT

    return slap(bot, trigger, target)
