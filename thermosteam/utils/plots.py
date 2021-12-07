# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020-2021, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""

import matplotlib.pyplot as plt
from typing import Iterable
import matplotlib.ticker as ticker
import numpy as np

__all__ = (
    'set_font',
    'set_figure_size',
    'style_axis',
    'style_plot_limits',
    'fill_plot',
    'set_axes_labels',
    'set_axes_xlabels',
    'set_axes_ylabels',
)   

def set_font(size=10, family='sans-serif', font='Arial'):
    import matplotlib
    fontkwargs = {'size': size}
    matplotlib.rc('font', **fontkwargs)
    params = matplotlib.rcParams
    params['font.' + family] = font
    params['font.family'] = family
    
def set_figure_size(width=None, aspect_ratio=None, units=None): 
    # units default to inch
    # width defaults 6.614 inches
    # aspect ratio defaults to 0.65
    if aspect_ratio is None:
        aspect_ratio = 0.65
    if width is None:
        width = 6.6142
    else:
        if units is not None:
            from thermosteam.units_of_measure import convert
            width = convert(width, units, 'inch')
    import matplotlib
    params = matplotlib.rcParams
    params['figure.figsize'] = np.array([width, width * aspect_ratio])

def style_axis(ax=None, xticks=None, yticks=None, 
               xticklabels=True, yticklabels=True,
               top=True, right=True, trim_to_limits=False,
               xtick0=True, ytick0=True,
               xtickf=True, ytickf=True,
               offset_xticks=False,
               xrot=None, ha=None): # pragma: no cover
    if ax is None:
        ax = plt.gca()
    if xticks is None:
        xticks, xtext = plt.xticks()
    else:
        xtext = xticklabels if isinstance(xticklabels, Iterable) else list(xticks)
    if yticks is None:
        yticks, ytext = plt.yticks()
        if not any([str(i) for i in ytext]): ytext = yticks
    else:
        ytext = yticklabels if isinstance(yticklabels, Iterable) else list(yticks)
    xtext = list(xtext)
    ytext = list(ytext)
    if trim_to_limits:
        style_plot_limits(xticks, yticks)
        if yticks[0] == 0.:
            yticks = yticks[1:]
    if not xtick0:
        xtext[0] = ''
    if not xtickf:
        xtext[-1] = ''
    if not ytick0:
        ytext[0] = ''
    if not ytickf:
        ytext[-1] = ''
    if offset_xticks:
        xticks_offset = np.array(xticks, float)
        xticks_offset[:] += 0.5 * np.diff(xticks).mean()
        ax.tick_params(axis="x", which='major', top=False, direction="inout", 
                       length=4)
        ax.tick_params(axis="x", which='minor', top=False, length=0, labelrotation=xrot)
        if xticklabels:
            plt.xticks(xticks_offset, ())
            ax.xaxis.set_minor_locator(ticker.FixedLocator(xticks))
            ax.xaxis.set_minor_formatter(ticker.FixedFormatter(xticklabels))
            if ha is not None: 
                for i in ax.xaxis.get_minorticklabels():
                    i.set_ha(ha)
        else:
            plt.xticks(xticks_offset, ())
    else:
        if xticklabels: 
            plt.xticks(xticks, xtext)
            if ha is not None: 
                for i in ax.xaxis.get_majorticklabels():
                    i.set_ha(ha)
        else:
            plt.xticks(xticks, ())
        ax.tick_params(axis="x", top=False, direction="inout", length=4, 
                       labelrotation=xrot)
    plt.yticks(yticks, ytext) if yticklabels else plt.yticks(yticks, ())
    ax.tick_params(axis="y", right=False, direction="inout", length=4)
    ax.zorder = 1
    xlim = plt.xlim()
    ylim = plt.ylim()
    axes = {'ax': ax}
    if right:
        x_twin = ax.twinx()
        ax._cached_xtwin = x_twin
        axes['twinx'] = x_twin 
        plt.sca(x_twin)
        x_twin.tick_params(axis='y', right=True, direction="in", length=4)
        x_twin.zorder = 2
        plt.ylim(ylim)
        plt.yticks(yticks, ())
    if top:
        y_twin = ax.twiny()
        ax._cached_ytwin = y_twin
        axes['twiny'] = y_twin 
        plt.sca(y_twin)
        y_twin.tick_params(axis='x', top=True, direction="in", length=4)
        y_twin.zorder = 2
        plt.xlim(xlim)
        if offset_xticks:
            plt.xticks(xticks_offset, ())
        else:
            plt.xticks(xticks, ())
    return axes
    
def style_plot_limits(xticks, yticks): # pragma: no cover
    plt.xlim([xticks[0], xticks[-1]])
    plt.ylim([yticks[0], yticks[-1]])
    
def fill_plot(color='k'): # pragma: no cover
    y_lb, y_ub = plt.ylim()
    plt.fill_between(plt.xlim(), [y_lb], [y_ub], color=color)
   
def set_axes_labels(axes, xlabel, ylabel): # pragma: no cover
    set_axes_xlabels(axes, xlabel)
    set_axes_ylabels(axes, ylabel)
   
def set_axes_xlabels(axes, xlabel): # pragma: no cover
    assert axes.ndim == 2
    N = axes.shape[1]
    if isinstance(xlabel, str): xlabel = N * [xlabel]
    for i in range(N): axes[-1, i].set_xlabel(xlabel[i])
    
def set_axes_ylabels(axes, ylabel): # pragma: no cover
    assert axes.ndim == 2
    N = axes.shape[0]
    if isinstance(ylabel, str): ylabel = N * [ylabel]
    for i in range(N): axes[i, 0].set_ylabel(ylabel[i])