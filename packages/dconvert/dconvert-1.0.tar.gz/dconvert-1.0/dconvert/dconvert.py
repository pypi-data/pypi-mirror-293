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

import pandas as pd
from pandas.errors import ParserError

class DConvert:
    def __init__(self) -> None:
        self.df = None


    def read_file(self, input_file: str, file_format: str) -> None:
        if file_format == 'csv':
            try:
                self.df = pd.read_csv(input_file)
            except Exception as e:
                raise RuntimeError(f"Failed to import from CSV: {e}")                
        elif file_format == 'json':
            try:
                # First, try to load it as a standard JSON file
                self.df = pd.read_json(input_file)
            except ValueError as e:
                # If it fails, check if it might be newline-delimited JSON
                try:
                    self.df = pd.read_json(input_file, lines=True)
                except ValueError as e2:
                    # If both methods fail, raise an error
                    raise RuntimeError(f"Failed to import from JSON. Possible format issue.\n"
                                    f"Standard JSON error: {e}\n"
                                    f"Newline-delimited JSON error: {e2}")            
        elif file_format == 'xml':
            try:
                self.df = pd.read_xml(input_file)
            except Exception as e:
                raise RuntimeError(f"Failed to import from XML: {e}")     
        elif file_format == 'html':
            try:
                self.df = pd.read_html(input_file)
            except Exception as e:
                raise RuntimeError(f"Failed to import from HTML: {e}")     
        elif file_format == 'xlsx':
            try:
                self.df = pd.read_excel(input_file)
            except Exception as e:
                raise RuntimeError(f"Failed to import from EXCEL: {e}")     
 
    
    def write_file(self, outfile: str, file_format: str, json_lines: bool = False, index: bool = False) -> None:
        if file_format == 'csv':
            try:
                self.df.to_csv(outfile, index=False)
            except Exception as e:
                raise RuntimeError(f"Failed to export to CSV: {e}")       
                     
        elif file_format == 'json':
            try:
                if json_lines:
                    self.df.to_json(outfile, orient='records', lines=True)
                else:
                    self.df.to_json(outfile,orient='records', indent=4)
            except Exception as e:
                raise RuntimeError(f"Failed to export to JSON: {e}")      
            
        elif file_format == 'xml':
            try:
                self.df.to_xml(outfile, index=index, parser='lxml')
 
            except ImportError:
                print("lxml not found, falling back to etree parser.")
                self.df.to_xml(outfile, index=index, parser='etree')
            except ParserError as e:
                raise ValueError(f"Failed to export to XML: {e}")
        
        elif file_format == 'html':
            try:            
                self.df.to_html(outfile, index=index)
            except Exception as e:
                raise RuntimeError(f"Failed to export to HTML: {e}")
            
        elif file_format == 'xlsx':
            try:
                self.df.to_excel(outfile, index=index, sheet_name='Sheet1')
            except Exception as e:
                raise RuntimeError(f"Failed to export to Excel: {e}")            

    
    def convert(self, input_file: str, input_file_type: str, outfile: str, file_format: str, json_lines: bool = False, index: bool = False) -> None:
        self.read_file(input_file, input_file_type)
        self.write_file(outfile, file_format, json_lines, index)

    
