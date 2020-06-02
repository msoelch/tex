"""Naval Fate.

Usage:
  mlmacros variables <variables> [--macros=<macros>] [--main_file=<p>] [--variables_file=<tf>] [--typora]
  mlmacros -h | --help

Options:
  --main_file=<m>    main
  -h --help     Show this screen.
"""
import docopt
import os


typora_header = """% % % % % % % %
% typora mlmacros light
% % % % % % % %
\\newcommand{\\ts}{_{1:t}}
\\newcommand{\\tm}{_{t-1}}
\\newcommand{\\tp}{_{t+1}}
\\newcommand{\\tsm}{_{1:t-1}}
\\newcommand{\\tsp}{_{1:t+1}}

\\newcommand{\\Ts}{_{1:T}}
\\newcommand{\\Tm}{_{T-1}}
\\newcommand{\\Tp}{_{T+1}}
\\newcommand{\\Tsm}{_{1:T-1}}
\\newcommand{\\Tsp}{_{1:T+1}}

"""

var_template = """% % % % % % % %
% macro name: {var}
% macro value: {macro}
% % % % % % % %
\\newcommand{{\\{var}}}{{{macro}}}
\\newcommand{{\\{var}seq}}{{\\overline{{\\{var}}}}}
\\newcommand{{\\{var}all}}{{\\{var}\Ts}}
\\newcommand{{\\{var}past}}{{\\{var}\\tsm}}
\\newcommand{{\\{var}filter}}{{\\{var}\\ts}}
\\newcommand{{\\{var}future}}{{\\{var}\\tsub{{\\tplus1}}{{T}}}}

\\newcommand{{\\b{var}}}{{\\boldsymbol{{\\mathbf{{\\{var}}}}}}}
\\newcommand{{\\b{var}seq}}{{\\bar{{\\b{var}}}}}
\\newcommand{{\\b{var}all}}{{\\b{var}\Ts}}
\\newcommand{{\\b{var}past}}{{\\b{var}\\tsm}}
\\newcommand{{\\b{var}filter}}{{\\b{var}\\ts}}
\\newcommand{{\\b{var}future}}{{\\b{var}\\tsub{{\\tplus1}}{{T}}}}

"""


def get_file_paths(args):

    is_variables = args["variables"]
    filename = "variables.tex"

    main_file = args["--main_file"]
    variables_file = args["--variables_file"]

    if variables_file is None:
        if main_file is not None:
            target_dir = os.path.dirname(main_file)
            variables_file = os.path.join(target_dir, filename)

    return variables_file, main_file


def write_to_file(preamble):
    variables_file, main_file = get_file_paths(args)

    if main_file is not None:
        raise NotImplementedError()

    if os.path.exists(variables_file) and os.path.getsize(variables_file) > 0:
        raise NotImplementedError("writing to a non-empty file is currently not supported.")
    else:
        with open(variables_file, 'w') as f:
            f.write(preamble)

    # the following is currently unreachable, unfinished code to support the
    # NotImplementedError scenarios.
    if main_file is not None:
        rel_variables_file = os.path.relpath(
            variables_file, start=os.path.dirname(main_file))
        with open(main_file, "r+") as f:
            main_text = f.read()
            contains_mlmacros = "\\usepackage{mlmacros}" in main_text
            contains_filename = "\\input{{{filename}}}".format(
                filename=rel_variables_file) in main_text

        if not contains_mlmacros:
            main_text = main_text.replace(
                "\n\\begin{document}",
                "\n\\usepackage{mlmacros}\n\n\\begin{document}")
            with open(main_file, "r+") as f:
                f.write(main_text)

        if not contains_filename:
            main_text = main_text.replace(
                "\n\\begin{document}",
                "\n\\input{{{filename}}}\n\n\\begin{{document}}".format(
                    filename=rel_variables_file))

        if not contains_filename or not contains_mlmacros:
            with open(main_file, "r+") as f:
                f.write(main_text)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    # add simplified macros for typora
    if args["--typora"]:
        preamble = typora_header
    else:
        preamble = ""

    # make a dict with pairs variables and macros
    vars = args["<variables>"].split(",")
    if args["--macros"] is not None:
        macros = args["--macros"].split(",")
        assert len(vars) == len(macros), "different number of variables and macros"
    else:
        macros = vars
    vars_dict = {v: m for v, m in zip(vars, macros)}

    # add a block per variable
    for var, macro in vars_dict.items():
        preamble += var_template.format(var=var, macro=macro)

    # put everything in a math block for typora
    if args["--typora"]:
        preamble = f"$$\n{preamble}$$"

    if args["--main_file"] is None and args["--variables_file"] is None:
        print(preamble)
    else:
        write_to_file(preamble)

