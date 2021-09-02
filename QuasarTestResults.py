"""
Author: Kenneth Rivadeneira
Company: Cytognos
Department: Software
"""

import os
import errno
import matplotlib.pylab as plt
import matplotlib.patches as mpatches
import pandas as pd

"""
This script uses the matplotlib.pylab as plt for plotting
purposes editing the axis ticks and labels since with the traditional  
matplotlib.pyplot as plt is not configure these labels properly 
see plt.xticks(x_labels, list(df_time[self._test_name_col][0:df_time.shape[0]:xlabel_freq]),
                   rotation="vertical", size=self.labels_size)
in get_full_plot()
"""


# Standalone class
class User:  # no need to inherits from (object) that's an python 2 class style
    _user = "admin"  # protected attribute
    _password = "admin"  # protected attribute
    _test_path = r"\\192.168.2.67\testResults"  # default test(server) path

    def __init__(self):
        print("Entering User")
        super(User, self).__init__()  # since its going to be inherited from in multi inheritance?
        print("Leaving User")
        pass

    def get_test_path(self) -> str:
        return self._test_path

    # class methods can also be used as alternative constructors
    @classmethod  # class method cause we might want to change these variables for all instances of this class
    def set_credentials(cls, user: str, password: str):
        cls._user = user
        cls._password = password

    # a method should be static if you dont access the instance (self) or the class (cls) anywhere
    # within the method
    @classmethod
    def set_test_path(cls, path: str):
        cls._test_path = path  # r"\\192.168.2.67\testResults"


# Standalone class
class PlotConfig:  # no need to inherits from (object) that's an python 2 class style

    def __init__(self):
        print("Entering PlotConfig")
        super(PlotConfig, self).__init__()  # since its going to be inherited from in multi inheritance?
        self.fig_size = (20, 5)
        self.labels_size = 15
        self.rotation = 90
        self.x_label = None
        self.y_label = None
        self.xlabel_freq = 1
        self.test_name_col = None
        self.time_col_name = None
        self.title = None
        # Leaves here cause it is last inheritance, it would continue if there were more parents
        print("Leaving PlotConfig")
        # In general if a check o computation is needed property getter, setter and deleter

    # decorators should be used, but if not plain attributes can be used.

    def basic_plot(self, df: pd.DataFrame) -> plt:
        """
        Create a basic matplotlib object
        :param df: dataframe to get the plotting data from
        :return: basic plt object
        """
        plt.figure(figsize=self.fig_size)
        x_labels_pos = [float(n) for n in range(0, df.shape[0], self.xlabel_freq)]
        x_labels = list(df[self.test_name_col][0:df.shape[0]:self.xlabel_freq])
        plt.xticks(x_labels_pos, x_labels, rotation=self.rotation, size=self.labels_size)
        plt.xlabel(self.x_label, size=self.labels_size)
        plt.yticks(size=self.labels_size)
        plt.ylabel(self.y_label, size=self.labels_size)
        plt.title(self.title, size=self.labels_size)
        return plt


class Build(User, PlotConfig):
    # class variables
    # _test_df = None  # this probably needs to be instance variable since can change across instances
    # _ref_test_df = None  # this probably needs to be instance variable since can change across instances
    # _fig_size = (20, 5)  # this is already at the PlotConfig class
    # labels_size = 15  # this is already at the PlotConfig class
    # _time_col_name = "TIME (ms)"  # this probably needs to be instance variable since can change across instances
    # _test_name_col = "TEST_NAME"  # this probably needs to be instance variable since can change across instances
    #  _ref_col_name = "ref_time"  # this probably needs to be instance variable since can change across instances
    # _dif_col_name = "dif_time"  # this probably needs to be instance variable since can change across instances

    # constructor
    def __init__(self, build_id: int):
        # call parent constructor, if parent constructor would have arguments we
        # could call int within this init and the subclass arguments as usual with
        # self.argument = argument
        # super().__init__()  # call parent constructor, mandatory!!
        # super(Build, self).__init__()
        # User.__init__(self)
        # PlotConfig.__init__(self)
        print("Entering Build")
        super(Build, self).__init__()  # the MRO would be [Build, User, PlotConfig].
        self.build_id = build_id
        self.build_df = None
        self.files = None
        self.dif_col_name = "dif_time"  # this probably needs to be instance variable since can change across instances
        print("Leaving Build")

    # maybe hold when connection is not possible differently with a catch throw if != 0
    def connect(self) -> bool:
        # connect to server
        con = os.system(fr"net use {self.get_test_path()} /user:{self._user} {self._password}")
        return True if con == 0 else False

    @property
    def benchmark_files(self) -> dict:
        return self.files

    @benchmark_files.setter
    def benchmark_files(self, benchmark_files_id: list) -> None:
        """
        Set benchmark files as a dictionary containing the build_id : df
        this needs to be with property getter setter since there is some logic in the method and it is not
        only a set or get of the object
        :param benchmark_files_id: list of id builds to get values from
        :return:
        """
        connection = self.connect()
        print("connection", connection)
        if not connection:
            raise ValueError(
                f"Connection to server failed. Invalid credentials: user: {self._user} pass: {self._password}")
        benchmark_files = {}
        current_build = self.build_id
        try:
            full_path = os.path.join(self._test_path, f"testResults_{self.build_id}")
            build_df = pd.read_csv(os.path.join(full_path, "benchmark.csv"), sep=";")
            self.build_df = build_df  # to use for the all tests plot
            benchmark_files[self.build_id] = build_df
            for b in benchmark_files_id:
                current_build = b
                ref_path = os.path.join(self._test_path, f"testResults_{current_build}")
                ref_df = pd.read_csv(os.path.join(ref_path, "benchmark.csv"), sep=";")
                benchmark_files[b] = ref_df
        except FileNotFoundError:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), f"testResults_{current_build}")

        self.files = benchmark_files

    @staticmethod
    def my_fun(value: float, mean: float) -> float:
        if mean != 0:
            return (value - mean) / mean * 100
        return value

    def bulk_df(self) -> pd.DataFrame:
        """
        Get the concatenated dataframes for all builds
        :return: dataframe
        """
        dfs = []
        ref_columns = []
        for build, df in self.benchmark_files.items():
            #  we can keep it all in a single df
            if build == self.build_id:  # keep test name from build
                df = df[[self.test_name_col, self.time_col_name]]
                # change column name to keep track of build
                df.columns = [self.test_name_col, f"{build} {self.time_col_name}"]
                dfs.append(df)
            else:
                df = df[[self.time_col_name]]
                col_name = f"{build} {self.time_col_name}"
                df.columns = [col_name]
                dfs.append(df)
                ref_columns.append(col_name)
        concat = pd.concat(dfs, axis=1)
        concat['mean'] = concat[ref_columns].mean(axis=1)
        concat["std"] = concat[ref_columns].std(axis=1)
        new_build_time_name = f"{self.build_id} {self.time_col_name}"
        concat[self.dif_col_name] = concat.apply(lambda row: self.my_fun(row[new_build_time_name], row["mean"]), axis=1)

        return concat

    # El ususario de test tiene que poder editar estos valores del grafico
    # no dejarlos aqui en la clase no?
    def get_full_plot(self, df_build: pd.DataFrame, xlabel_freq: int, sorting: bool) -> plt:
        if sorting:
            df_build.sort_values(self.time_col_name, ascending=False, inplace=True)
        # filer out invalid tests
        df_build = df_build[df_build[self.time_col_name] > 0]
        # set xlabel_freq
        self.xlabel_freq = xlabel_freq
        self.title = f"Execution Time Build {self.build_id}"
        plt_ = self.basic_plot(df_build)
        # set index to plot series
        df_build.index = df_build[self.test_name_col]
        # when compiling script into .exe file pandas.plot() does not compile
        # so we used plt buy using pylab instead of pyplot for plotting series
        # editing the xticks and and labels
        plt_.plot(df_build[self.time_col_name].values, label=self.time_col_name)
        # plt.yscale('log', base=10)
        plt_.legend(prop={'size': self.labels_size})
        return plt

    def get_it_df(self, df_time: pd.DataFrame) -> pd.DataFrame:
        # get only IT tests
        return df_time[df_time[self.test_name_col].str.contains('IT+[A-Z]')]

    def it_test_plot(self, bulk_df: pd.DataFrame) -> plt:
        it_df = self.get_it_df(bulk_df)
        x = it_df[self.test_name_col]
        y = it_df[f"{self.build_id} {self.time_col_name}"]
        x1 = it_df[self.test_name_col]
        y1 = it_df["mean"]
        self.title = "IT Tests"
        plt_ = self.basic_plot(bulk_df)
        plt_.plot(x, y, marker='o', label=f"Current Build {self.build_id}")
        plt_.plot(x1, y1, marker='s', label=f"Mean Builds {list(self.benchmark_files.keys())[1:]} ")
        plt_.legend(prop={'size': self.labels_size})
        return plt_

    def add_it_plot_data(self, it_test: pd.DataFrame, it_plt: plt) -> plt:
        """
        Add extra data to the it plot for color visual time
        representation.
        :param it_test: dataframe containing only the it data
        :param it_plt: it plot to be used as template
        :return: new it plot with extra data
        """
        l1 = plt.legend(prop={'size': self.labels_size})
        red_patch = mpatches.Patch(color='red', label='Test takes more time than reference')
        light_red = mpatches.Patch(color='salmon', label='Test takes more time than reference')
        dark_red = mpatches.Patch(color='darkred', label='Test takes more time than reference')
        green_patch = mpatches.Patch(color='green', label='Test takes less time than reference')
        light_green_patch = mpatches.Patch(color='lightgreen', label='Test takes less time than reference')
        dark_green_patch = mpatches.Patch(color='darkgreen', label='Test takes less time than reference')
        # This removes l1 from the axes.
        it_plt.legend(handles=[light_red, red_patch, dark_red, light_green_patch, green_patch, dark_green_patch],
                      bbox_to_anchor=(1.05, -3), loc='lower right', prop={'size': self.labels_size})
        # Add l1 as a separate artist to the axes
        it_plt.gca().add_artist(l1)
        # We can specify ranges her and define colors
        for i in range(0, it_test.shape[0]):
            if it_test[self.dif_col_name].values[i] < 0:
                plt.gca().get_xticklabels()[i].set_color("green")
            elif it_test[self.dif_col_name].values[i] > 0:
                plt.gca().get_xticklabels()[i].set_color("red")
            else:
                continue

        return it_plt

    # displays object info in a pythonic code format (for recreating the object)
    def __repr__(self):  # dunder method (magic method)
        return f"Build({self.build_id})"

    # displays end user object info (human readable)
    def __str__(self):
        return f"Build {self.build_id}"

    def __add__(self, other):
        if isinstance(other, Build):
            return self.build_id + self.build_id
        return NotImplemented  # let the other object try to handle the add operations avoiding an initial error
        # if other object does not how to handle will throw an error

    def __len__(self, other):
        return len(self.benchmark_files) - 1

# df.style.set_table_styles([{'selector': 'th', 'props': [('background-color', 'gray')]}]).to_excel('styled.xlsx',
# engine='openpyxl')

# styled = (out_df.style.applymap(lambda x: 'background-color: %s' % 'yellow' if x == "Test" else ''))
# styled = out_df.style.set_table_styles([{'selector': 'th', 'props': [('background-color', 'yellow')]}])


# out_df.style.set_table_styles([{'selector': 'th', 'props': [('background-color', 'gray')]}])\
#    .to_excel('styled.xlsx', engine='openpyxl')

# styled.to_excel('failedTestsBuild{}.xlsx'.format(build), engine='openpyxl',index=False, header=True)
# out_df.to_csv('failedTestsBuild{}.csv'.format(build), sep=",", index=False)
