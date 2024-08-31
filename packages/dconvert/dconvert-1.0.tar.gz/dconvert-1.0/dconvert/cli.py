"""
================================================================================
   Project: dconvert
   Description: dconvert is a command-line tool that allows you to easily convert data files between various formats, including JSON, CSV, XML, HTML, and XLSX. 
   Author: Aaron Mathis
   Email: aaron.mathis@gmail.com
   License: GNU General Public License v3.0 (GPL-3.0)
   License URL: https://www.gnu.org/licenses/gpl-3.0.en.html
================================================================================

   This file is part of dconvert.

   pySQLExport-gui is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   pySQLExport-gui is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with pySQLExport-gui. If not, see <https://www.gnu.org/licenses/>.

================================================================================
"""

import argparse
import os

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="dconvert CLI Tool")
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument('-i','--input', type=str, required=True, help='Path of the file to convert.')
        self.parser.add_argument('-o','--outfile', type=str, required=True,help='Path of the converted file')
        self.parser.add_argument('-f','--format', type=str, choices=['csv', 'json', 'html', 'xml','xlsx'], help='Output format (csv, json, html, xml,xlsx)')
        self.parser.add_argument('-t','--inputfiletype', type=str, choices=['csv', 'json', 'html', 'xml','xlsx'], help='Input file type (csv, json, html, xml,xlsx)')
        self.parser.add_argument('-l', '--jsonlines', type=self.str2bool, nargs='?', const=True, default=False, help='Single JSON array (false) or Newline-Delimited JSON (true)')
        self.parser.add_argument('--index', type=self.str2bool, nargs='?', const=True, default=False, help='Include index in output (true) or exclude it (false)')


    
    def str2bool(self, v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')    


    def parse_args(self, args=None):
        parsed_args = self.parser.parse_args(args)
        parsed_args = self.parser.parse_args(args)

        # If format is not specified, try to infer from the outfile extension
        if not parsed_args.format:
            ext = os.path.splitext(parsed_args.outfile)[1].lower()
            if ext in ['.csv', '.json', '.html', '.xml','.xlsx']:
                parsed_args.format = ext.lstrip('.')
            else:
                raise ValueError(f"Could not infer format from file extension: {ext}. Please specify the format explicitly with --format.")
        
        # Check if input file type is specified or can be inferred
        input_ext = os.path.splitext(parsed_args.input)[1].lower()
        if not parsed_args.inputfiletype:
            if input_ext in ['.csv', '.json', '.html', '.xml', '.xlsx']:
                parsed_args.inputfiletype = input_ext.lstrip('.')
            else:
                raise ValueError(f"Could not infer input file type from file extension: {input_ext}. Please specify the input file type with --inputfiletype.")


        return parsed_args
