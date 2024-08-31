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

from dconvert.cli import CLI
from dconvert.dconvert import DConvert
import os
import sys

def main():
    cli = CLI()
    dconvert = DConvert()
    try:
        args = cli.parse_args()  # Now works without needing to pass anything
        print(f"Converting {args.input} to {args.outfile} as {args.format} format.")
        print(args.index)
        dconvert.convert(args.input, args.inputfiletype, args.outfile, args.format, args.jsonlines, args.index)

        
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
