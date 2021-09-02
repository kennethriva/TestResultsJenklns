#!/usr/bin/env python

"""
Author: Kenneth Rivadeneira
Company: Cytognos
Department: Software
"""

import argparse
from QuasarTestResults import *


# col_names = Build.get_benchmark_col_names()


def create_arg_parser():
    """Creates and returns the ArgumentParser object."""

    parser = argparse.ArgumentParser()
    parser.description = "Benchmark file analysis"
    parser.add_argument("-build", help='Current build id', required=True)
    parser.add_argument("-ref", help='Reference build id', required=True)
    parser.add_argument("-outdir", help='Desired output directory', required=True)

    return parser.parse_args()


def get_failed_tests(df):
    # SUCCESS is a boolean field
    failed_tests = df[~df["SUCCESS"]]
    # col names
    out_df = pd.DataFrame(failed_tests['TEST_NAME'].values)
    out_df["Descripcion"] = "-"
    out_df["Responsable"] = "-"
    out_df.columns = ["Test", "Description", "Assignment"]
    # set output dir of writer object
    writer = pd.ExcelWriter(os.path.join(parsed_args.outdir, "test_failed_{}.xlsx".format(parsed_args.build)),
                            engine='xlsxwriter')
    workbook_ = writer.book
    worksheet = workbook_.add_worksheet('Summary')
    writer.sheets['Summary'] = worksheet

    for i, width in enumerate(get_col_widths(out_df)):
        worksheet.set_column(i, i - 1, width)  # set header column range to the maximum
    out_df.to_excel(writer, sheet_name='Summary', index=False, startrow=1, header=False)

    # Add a header format.
    header_format = workbook_.add_format({
        'bg_color': 'yellow',  # your setting
        'bold': True,  # additional stuff...
        'text_wrap': False,
        'valign': 'top',
        'align': 'center',
        'shrink': True,
        'border': 0})

    # Write the column headers with the defined format.
    for col_num, value in enumerate(out_df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    return writer


def get_col_widths(df):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in df[col].values] + [len(col)]) for col in df.columns]


def main():
    build = Build(parsed_args.build, parsed_args.ref)
    print(build)
    print(repr(build))
    build.set_credentials("cytognos", "cytognos")  # set credentials
    build.set_benchmark_files()  # set benchmark file current and re

    df_current = build.get_benchmark_file()
    df_time = build.get_time_df(sorting=True)
    it_df = build.get_it_df(df_time)

    # Get test results file
    writer = get_failed_tests(df_current)
    writer.save()  # its output dir has already been set in the get_failed_tests()
    # writer.close()
    file_path = os.path.join(parsed_args.outdir, "test_failed_{}.xlsx".format(build.get_build_id()))
    print("Test results file saved file at: {}".format(file_path))

    # Get it plot
    plot_path = os.path.join(parsed_args.outdir,
                             "plot_{}-{}.png".format(build.get_build_id(), build.get_ref_build_id()))
    it_plot = build.get_it_plot(df_time)
    # this is optional
    build.add_it_plot_data(it_df, it_plot)
    it_plot.savefig(plot_path, bbox_inches='tight')
    print("IT Plot file saved at: {}".format(plot_path))

    # Get full plot
    plot_full_path_original = os.path.join(parsed_args.outdir, "plot_original{}.png".format(build.get_build_id()))
    plot_full_path = os.path.join(parsed_args.outdir, "plot_{}.png".format(build.get_build_id()))

    plot_full_original = build.get_full_plot(df_time, xlabel_freq=100)
    plot_full = build.all_tests_plot(df_time)

    plot_full_original.savefig(plot_full_path_original, bbox_inches='tight', pad_inches=0.5)  # access figure to save

    plot_full.savefig(plot_full_path, bbox_inches='tight', pad_inches=0.5)  # access figure to save
    print("Full Plot file saved at: {}".format(plot_full_path))

    # This is how we should use the api
    # build.time_col_name = "TIME (ms)"
    # build.test_name_col = "TEST_NAME"
    # build.xlabel_freq = 100
    # build.basic_plot(df_time).savefig(plot_full_path, bbox_inches='tight', pad_inches=0.5)


def debug():
    my_build = Build(1771)
    my_build.set_credentials("cytognos", "cytognos")
    # When using a property, you do not manually call the setter's
    # name like build.benchmark_files([1762, 1761, 1760, 1759, 1759]).
    # You use attribute assignment syntax, build.benchmark_files = [1762, 1761, 1760, 1759, 1759].
    # This is the entire point of properties: to have transparent attribute-like syntax
    # while still having function-like behavior.
    # It
    my_build.benchmark_files = [1770, 1769]
    my_build.test_name_col = my_build.x_label = "TEST_NAME"
    my_build.time_col_name = my_build.y_label = "TIME (ms)"
    bulk_df = my_build.bulk_df()
    bulk_df_it = my_build.get_it_df(bulk_df)
    df_build = my_build.build_df
    df_build.df.sort_values(my_build.test_name_col)
    df_build.columns = ["Test", "Time"]

    plot_path = os.path.join(r"C:\\Users\\Kenneth Rivadeneira\\Desktop",
                                  "plot_{}_IT.png".format(my_build.build_id))
    plot_ = my_build.it_test_plot(bulk_df_it)

    plot_.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)  # access figure to save
    plot_full_path = os.path.join(r"C:\\Users\\Kenneth Rivadeneira\\Desktop", "plot_{}_full.png".format(my_build.build_id))
    plot_1 = my_build.get_full_plot(df_build, xlabel_freq=100, sorting=True)
    plot_1.savefig(plot_full_path, bbox_inches='tight', pad_inches=0.5)  # access figure to save

    build = Build(1755)
    # print(build._test_path)
    build.set_credentials("cytognos", "cytognos")
    build.set_benchmark_files()  # set benchmark file current and ref
    plot_full_path = os.path.join(r"C:\\Users\\Kenneth Rivadeneira\\Desktop", "plot_{}.png".format(build.get_build_id()))
    df_time = build.get_time_df(sorting=True)
    # build.time_col_name = "TIME (ms)"
    build.test_name_col = "TEST_NAME"
    build.xlabel_freq = 100

    # This is how you use pure attributes to set its value
    time_col_name_ = "TIME (ms)"
    build.time_col_name = time_col_name_
    time_col_name_ = build.time_col_name
    # here we are deleting this attribute and we should not
    # this is more when we are creating attributes using
    # the build.newProperty = value and it is not defined within
    # the class or parent class
    del build.time_col_name  # does this deleter should be used?

    plot_full = build.basic_plot(df_time)
    plot_full.plot(df_time[build.time_col_name].values, label=build.time_col_name)
    plot_full.legend(prop={'size': build._labels_size})
    # plot_full = build.all_tests_plot(df_time)
    plot_full.savefig(plot_full_path, bbox_inches='tight', pad_inches=0.5)  # access figure to save
    print("Full Plot file saved at: {}".format(plot_full_path))


if __name__ == "__main__":
    # parsed_args = create_arg_parser()
    debug()
    # main()
