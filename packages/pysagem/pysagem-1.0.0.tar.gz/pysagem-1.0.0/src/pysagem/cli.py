from argparse import SUPPRESS, ArgumentParser, ArgumentTypeError, RawTextHelpFormatter

BAR_CONFIG = {
    "simulation": {
        "title": "Simulating:",
        "bar": "classic2",
        "spinner": "stars",
        "stats": False,
    },
    "animation": {
        "title": "Generating the animation ...",
        "bar": "brackets",
        "length": 10,
        "spinner": None,
        "monitor": False,
        "elapsed": False,
        "stats": False,
    },
}


class MyArgumentParser(ArgumentParser):
    """Changing ArgumentParser method to treat each space-separated word as an argument"""

    def convert_arg_line_to_args(self, arg_line):
        return arg_line.split()


def type_generation(x):
    x = int(x)

    if x < 2:
        raise ArgumentTypeError(
            "Choose a number of generations >= 2 to permit the initial disturbance (t=1)"
        )

    return x


def type_neighbor_radius(x):
    x = float(x)

    if x < 1.0:
        raise ArgumentTypeError(
            "The neighborhood radius should be at least 1.0 to permit the migration of individuals"
        )

    return x


def type_migration_rate(x):
    x = float(x)

    if x < 0 or x > 1.0:
        raise ArgumentTypeError("The migration rate must be between 0 and 1")

    return x


def type_event_intensity(x):
    x = float(x)

    if x < 0 or x > 1.0:
        raise ArgumentTypeError(
            "The intensity of this event must be a value between 0 and 1"
        )

    return x


def setup_parser():
    parser = MyArgumentParser(
        description="""
 _ __  _   _ ___  __ _  __ _  ___ _ __ ___  
| '_ \| | | / __|/ _` |/ _` |/ _ \ '_ ` _ \ 
| |_) | |_| \__ \ (_| | (_| |  __/ | | | | |
| .__/ \__, |___/\__,_|\__, |\___|_| |_| |_|
| |     __/ |           __/ |               
|_|    |___/           |___/             
                                      
Simulate and visualize biological invasions in dynamic landscapes 

Arguments:""",
        usage="%(prog)s [--parameter <value>] [options]",
        formatter_class=lambda prog: RawTextHelpFormatter(prog, max_help_position=28),
        add_help=False,
        fromfile_prefix_chars="@",
    )

    initial_dist = parser.add_argument_group("Initial Disturbance")
    initial_dist.add_argument(
        "--p_initialdist",
        type=type_event_intensity,
        default=0.5,
        metavar="<float>",
        help="disturbance intensity, i.e., the probability of a random\npatch being selected to be disturbed (default: %(default)s)",
    )

    initial_dist.add_argument(
        "--q_initialdist",
        type=type_event_intensity,
        default=1.0,
        metavar="<float>",
        help="disturbance degree of clustering (default: %(default)s)",
    )

    restorations = parser.add_argument_group("Restorations")
    restorations.add_argument(
        "--rest",
        action="store_true",
        help="enables restorations (default: %(default)s)",
    )

    restorations.add_argument(
        "--p_rest",
        type=type_event_intensity,
        default=0.5,
        metavar="<float>",
        help="restoration intensity, i.e., the probability of a random\npatch being selected to be restored (default: %(default)s)",
    )

    restorations.add_argument(
        "--n_rest",
        type=int,
        default=5,
        metavar="<int>",
        help="number of restorations (default: %(default)s)",
    )

    add_dist = parser.add_argument_group("Additional Disturbances")
    add_dist.add_argument(
        "--add_dist",
        action="store_true",
        help="enables additional disturbances (default: %(default)s)",
    )

    add_dist.add_argument(
        "--p_add_dist",
        type=type_event_intensity,
        default=0.5,
        metavar="<float>",
        help="additional disturbance intensity (default: %(default)s)",
    )

    add_dist.add_argument(
        "--q_add_dist",
        type=type_event_intensity,
        default=1.0,
        metavar="<float>",
        help="degree of clustering of additional disturbance (default: %(default)s)",
    )

    add_dist.add_argument(
        "--n_add_dist",
        type=int,
        default=5,
        metavar="<int>",
        help="number of additional disturbances (default: %(default)s)",
    )

    general = parser.add_argument_group("General")
    general.add_argument(
        "--length",
        type=int,
        default=50,
        metavar="<int>",
        help="length of the square matrix (default: %(default)s)",
    )

    general.add_argument(
        "--gen",
        type=type_generation,
        default=1000,
        metavar="<int>",
        help="number of generations (default: %(default)s)",
    )

    general.add_argument(
        "--radius",
        type=type_neighbor_radius,
        default=3.0,
        metavar="<float>",
        help="radius of neighbors to consider (default: %(default)s)",
    )

    general.add_argument(
        "--alpha",
        type=float,
        default=0.8,
        metavar="<float>",
        help="effect of the invasive species on the native species (default: %(default)s)",
    )

    general.add_argument(
        "--beta",
        type=float,
        default=0.8,
        metavar="<float>",
        help="effect of the native species on the invasive species (default: %(default)s)",
    )

    general.add_argument(
        "--rn",
        type=float,
        default=1.0,
        metavar="<float>",
        help="growth rate of the native species (default: %(default)s)",
    )

    general.add_argument(
        "--ri",
        type=float,
        default=1.0,
        metavar="<float>",
        help="growth rate of the invasive species (default: %(default)s)",
    )

    general.add_argument(
        "--invasors",
        type=int,
        default=1000,
        metavar="<int>",
        help="number of invasors (default: %(default)s)",
    )

    general.add_argument(
        "--mignative",
        type=type_migration_rate,
        default=0.2,
        metavar="<float>",
        help="migration rate of native species (default: %(default)s)",
    )

    general.add_argument(
        "--miginvasive",
        type=type_migration_rate,
        default=0.2,
        metavar="<float>",
        help="migration rate of invasive species (default: %(default)s)",
    )

    options = parser.add_argument_group("Other Options")
    options.add_argument(
        "-h",
        "--help",
        action="help",
        default=SUPPRESS,
        help="show this help message and exit",
    )

    options.add_argument(
        "-s",
        "--seed",
        type=int,
        metavar="<int>",
        help="seed for reproducibility (default: random int)",
    )

    options.add_argument(
        "-a",
        "--animation",
        action="store_true",
        help="generates an animation according to the simulation",
    )

    options.add_argument(
        "-n",
        "--name",
        type=str,
        default="pysagem",
        metavar="<str>",
        help="name of the run used for outputs (default: %(default)s)",
    )

    return parser
