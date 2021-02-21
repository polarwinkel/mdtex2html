#!/usr/bin/python3
'''
This will convert Markdown with included LaTeX-equations to HTML.
The Formulas will be in MathML-Format.

block-equations need to start with $$ or \[
inline-equations start with \( or $

version 1.1

(c) 2020 by Dirk Winkel

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

incomplete = '<font color="orange">Warning: Formula incomplete!</font>'
convError = '<font color="red">ERROR converting TeX2mathml!</font>'

def convert(mdtex):
    ''' converts recursively the mdTeX-mixture to HTML with MathML '''
    found = False
    # find first $$-formula:
    parts = re.split('\${2}', mdtex, 2)
    if len(parts)>1:
        found = True
        result = convert(parts[0])+'\n'
        try:
            result += '<div class="blockformula">'+tex2mathml(parts[1])+'</div>\n'
        except:
            result += '<div class="blockformula">'+convError+'</div>'
        if len(parts)==3:
            result += convert(parts[2])
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
            result = convert(parts[0]+mathml+parts[2])
        else:
            result = convert(parts[0]+mathml+incomplete)
    # else find first \[..\]-equation:
    else:
        parts = re.split(r'\\\[', mdtex, 1)
    if len(parts)>1 and not found:
        found = True
        result = convert(parts[0])+'\n'
        parts = re.split(r'\\\]', parts[1], 1)
        try:
            result += '<div class="blockformula">'+tex2mathml(parts[0])+'</div>\n'
        except:
            result += '<div class="blockformula">'+convError+'</div>'
        if len(parts)==2:
            result += convert(parts[1])
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
            result = convert(parts[0]+mathml+subp[1])
        else:
            result = convert(parts[0]+mathml+incomplete)
    if not found:
        # no more formulas found
        result = md2html(mdtex)
    return result
