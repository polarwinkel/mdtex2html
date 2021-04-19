#!/usr/bin/python3
'''
This will convert Markdown with included LaTeX-equations to HTML.
The Formulas will be in MathML-Format.

block-equations need to start with $$ or \[
inline-equations start with \( or $

version 1.2.0

(c) 2020-2021 by Dirk Winkel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    
'''

from latex2mathml.converter import convert as tex2mathml
from markdown import markdown as md2html
import re

incomplete = '<font style="color:orange;" class="tooltip">&#9888;<span class="tooltiptext">formula incomplete</span></font>'
convError = '<font style="color:red" class="tooltip">&#9888;<span class="tooltiptext">LaTeX-convert-error</span></font>'

def convert(mdtex, extensions=[], splitParagraphs=True):
    ''' converts recursively the Markdown-LaTeX-mixture to HTML with MathML '''
    found = False
    # handle all paragraphs separately (prevents aftereffects)
    if splitParagraphs:
        parts = re.split("\n\n", mdtex)
        result = ''
        for part in parts:
            result += convert(part, extensions, splitParagraphs=False)
        return result
    # find first $$-formula:
    parts = re.split('\${2}', mdtex, 2)
    if len(parts)>1:
        found = True
        result = convert(parts[0], extensions, splitParagraphs=False)+'\n'
        try:
            result += '<div class="blockformula">'+tex2mathml(parts[1])+'</div>\n'
        except:
            result += '<div class="blockformula">'+convError+'</div>'
        if len(parts)==3:
            result += convert(parts[2], extensions, splitParagraphs=False)
        else:
            result += '<div class="blockformula">'+incomplete+'</div>'
    # else find first $-formulas:
    else:
        parts = re.split('\${1}', mdtex, 2)
    if len(parts)>1 and not found:
        found = True
        try:
            mathml = tex2mathml(parts[1])
        except:
            mathml = convError
        if parts[0].endswith('\n\n') or parts[0]=='': # make sure textblock starts before formula!
            parts[0]=parts[0]+'&#x200b;'
        if len(parts)==3:
            result = convert(parts[0]+mathml+parts[2], extensions, splitParagraphs=False)
        else:
            result = convert(parts[0]+mathml+incomplete, extensions, splitParagraphs=False)
    # else find first \[..\]-equation:
    else:
        parts = re.split(r'\\\[', mdtex, 1)
    if len(parts)>1 and not found:
        found = True
        result = convert(parts[0], extensions, splitParagraphs=False)+'\n'
        parts = re.split(r'\\\]', parts[1], 1)
        try:
            result += '<div class="blockformula">'+tex2mathml(parts[0])+'</div>\n'
        except:
            result += '<div class="blockformula">'+convError+'</div>'
        if len(parts)==2:
            result += convert(parts[1], extensions, splitParagraphs=False)
        else:
            result += '<div class="blockformula">'+incomplete+'</div>'
    # else find first \(..\)-equation:
    else:
        parts = re.split(r'\\\(', mdtex, 1)
    if len(parts)>1 and not found:
        found = True
        subp = re.split(r'\\\)', parts[1], 1)
        try:
            mathml = tex2mathml(subp[0])
        except:
            mathml = convError
        if parts[0].endswith('\n\n') or parts[0]=='': # make sure textblock starts before formula!
            parts[0]=parts[0]+'&#x200b;'
        if len(subp)==2:
            result = convert(parts[0]+mathml+subp[1], extensions, splitParagraphs=False)
        else:
            result = convert(parts[0]+mathml+incomplete, extensions, splitParagraphs=False)
    if not found:
        # no more formulas found
        result = md2html(mdtex, extensions=extensions)
    return result
