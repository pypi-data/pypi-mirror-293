import numpy as np
from alive_progress import alive_bar

from .animation import animate
from .cli import BAR_CONFIG, setup_parser
from .events import (
    disturbance,
    find_neighbors,
    invasion,
    ki_update,
    kn_update,
    lotka,
    migration,
    restoration,
)
from .utils import get_pattern, log_initial_args, randint, set_seed, setup_logger


def main():
    try:
        parser = setup_parser()
        args = parser.parse_args()
        logger = setup_logger(args.name)

        if not args.q_initialdist >= (2 - (1 / args.p_initialdist)):
            raise ValueError("initial disturbance: q00 must be >= 2 - 1/p0")

        if args.add_dist:
            if not args.q_add_dist >= (2 - (1 / args.p_add_dist)):
                raise ValueError("additional disturbance: q value must be >= 2 - 1/p")

        if not args.seed:
            args.seed = np.random.randint(1000000)

        neighbors = find_neighbors(args.length, args.radius)
        close_neighbors = find_neighbors(args.length, 1.0)

        patches = np.empty(
            args.length**2,
            dtype=[
                ("quality", "uint8"),
                ("natpop", "float64"),
                ("invpop", "float64"),
                ("k_nat", "uint16"),
                ("k_inv", "uint16"),
            ],
        )

        data_arr = np.empty(
            (args.gen, args.length**2),
            dtype=[
                ("quality", "uint8"),
                ("natpop", "float64"),
                ("invpop", "float64"),
            ],
        )

        pop_mean = np.empty(
            args.gen,
            dtype=[
                ("native", "float64"),
                ("invasive", "float64"),
            ],
        )

        if args.rest:
            if args.add_dist:
                set_seed(args.seed)
                events_gens = np.array(
                    [randint(2, args.gen) for _ in range(args.n_rest + args.n_add_dist)]
                )
                rest_gens = events_gens[: args.n_rest]
                additional_dist_gens = events_gens[args.n_rest :]

            else:
                set_seed(args.seed)
                rest_gens = np.array([randint(2, args.gen) for _ in range(args.n_rest)])

        else:
            if args.add_dist:
                set_seed(args.seed)
                additional_dist_gens = np.array(
                    [randint(2, args.gen) for _ in range(args.n_add_dist)]
                )

        counter_rest = 0
        counter_addist = 0

        log_initial_args(logger, args)
        if args.rest:
            logger.info("\u2022 restorations:")
            logger.info(f"  - intensity: {args.p_rest}")
            logger.info("  - random pattern")
            logger.info(
                f"  - selected generations:\n    {sorted(rest_gens.tolist())}\n"
            )

        if args.add_dist:
            logger.info("\u2022 additional disturbances:")
            logger.info(f"  - intensity: {args.p_add_dist}")
            logger.info(f"  - degree of clustering: {args.q_add_dist}")
            logger.info(f"  - {get_pattern(args.p_add_dist, args.q_add_dist)}")
            logger.info(
                f"  - selected generations:\n    {sorted(additional_dist_gens.tolist())}\n"
            )

        with alive_bar(args.gen, **BAR_CONFIG["simulation"]) as bar:
            for t in range(args.gen):
                if t == 0:
                    patches["quality"] = 2
                    patches["natpop"] = 500
                    patches["invpop"] = 0

                    data_arr["quality"][t] = patches["quality"]
                    data_arr["natpop"][t] = patches["natpop"]
                    data_arr["invpop"][t] = patches["invpop"]
                    pop_mean["native"][t] = np.mean(patches["natpop"])
                    pop_mean["invasive"][t] = np.mean(patches["invpop"])

                    bar()
                    continue

                patches["k_nat"] = kn_update(patches["quality"])
                patches["k_inv"] = ki_update(patches["quality"])

                temp_natpop = lotka(
                    patches["natpop"],
                    patches["invpop"],
                    args.rn,
                    args.alpha,
                    patches["k_nat"],
                )
                temp_invpop = lotka(
                    patches["invpop"],
                    patches["natpop"],
                    args.ri,
                    args.beta,
                    patches["k_inv"],
                )

                patches["natpop"] = temp_natpop
                patches["invpop"] = temp_invpop

                set_seed(args.seed)
                patches["natpop"] = migration(
                    patches["natpop"], args.mignative, neighbors
                )

                set_seed(args.seed)
                patches["invpop"] = migration(
                    patches["invpop"], args.miginvasive, neighbors
                )

                if t == 1:
                    set_seed(args.seed)
                    patches["quality"] = disturbance(
                        patches["quality"],
                        args.p_initialdist,
                        args.q_initialdist,
                        close_neighbors,
                    )
                    print("initial disturbance")

                    set_seed(args.seed)
                    patches["invpop"] = invasion(
                        patches["quality"], patches["invpop"], args.invasors
                    )
                    print("biological invasion")

                if args.rest:
                    if np.any(t == rest_gens):
                        set_seed(args.seed)
                        patches["quality"] = restoration(
                            patches["quality"], args.p_rest
                        )

                        counter_rest += 1
                        print(f"restoration #{counter_rest}")

                if args.add_dist:
                    if np.any(t == additional_dist_gens):
                        set_seed(args.seed)
                        patches["quality"] = disturbance(
                            patches["quality"],
                            args.p_add_dist,
                            args.q_add_dist,
                            close_neighbors,
                        )

                        counter_addist += 1
                        print(f"additional disturbance #{counter_addist}")

                data_arr["quality"][t] = patches["quality"]
                data_arr["natpop"][t] = patches["natpop"]
                data_arr["invpop"][t] = patches["invpop"]
                pop_mean["native"][t] = np.mean(patches["natpop"])
                pop_mean["invasive"][t] = np.mean(patches["invpop"])
                bar()

        print("Simulation finished!")
        np.savez_compressed(
            f"{args.name}.npz",
            mean_nat=pop_mean["native"],
            mean_inv=pop_mean["invasive"],
            landscape=data_arr["quality"],
            natpop=data_arr["natpop"],
            invpop=data_arr["invpop"],
        )

        if args.animation:
            animate(
                args,
                data=data_arr,
                mean=pop_mean,
                rest_gens=rest_gens,
                add_dist_gens=additional_dist_gens,
            )
            print("Animation Finished!")

    except KeyboardInterrupt:
        print("\nShutdown requested...exiting")

    except Exception as e:
        print(f"\nERROR:{e}")


if __name__ == "__main__":
    main()
