
import re
import os
import datetime
import json
import numpy as np
import pandas as pd

def clean_split(x:str) -> list[str]:
    """Split strings at a space without keeping empty characters"""
    return [
        char for char in x.split(" ")
        if char != ""
    ]


def regex(
    strings: list[str] | str,
    patterns: list[str] | str,
    indices: bool = True,
    require_all: bool = False,
    split_newlines: bool = True
) -> list[str] | list[int]:
    """Perform regular expression analysis

    _extended_summary_

    Parameters
    ----------
    strings : list[str] | str
        Strings to match patterns for
    patterns : list[str] | str
        Patterns to match in strings
    indices : bool, optional
        If True, return the indices of matches, if False, return the values of
        the matches, by default True
    require_all : bool, optional
        If True, require the strings to match every pattern, by default False
    split_newlines : bool, optional
        If a single string is provided, split the string at each newline,
        by default True

    Returns
    -------
    list[str] | list[int]
        List of strings containing the matches if not indices, list of integers
        for the index of a match if indices.
    """
    if isinstance(strings, str):
        strings = strings.split(sep="\n") if split_newlines else [strings]
    if isinstance(patterns, str):
        patterns = [patterns]

    anyall = all if require_all else any

    compiled_patterns = [re.compile(pattern) for pattern in patterns]

    if indices:
        return [i for i, string in enumerate(strings) if anyall(
            regex.search(string) for regex in compiled_patterns
        )]
    return [string for string in strings if any(
        regex.search(string) for regex in compiled_patterns
    )]


def find_mcnp_outputs(dir: str = "") -> list[str]:
    """Find all MCNP output files in directory

    Parameters
    ----------
    dir : str, optional
        Directory, by default `os.getcwd()`

    Returns
    -------
    list[str]
        List of all mcnp output files
    """
    if dir == "":
        dir = os.getcwd()
    out: list[str] = regex(
        os.listdir(dir),
        [".o", ".out", ".mcnpout"],
        indices=False
    ) # type: ingore # this is one of the possible output types of regex
    return out


def get_tally_info(full_output: list[str]) -> pd.DataFrame:
    """Return tally summary information

    Parameters
    ----------
    full_output : list[str]
        MCNP output as list of strings for each line

    Returns
    -------
    pd.DataFrame
        Dataframe with columns for the name of the tally, the tally type,
        the start and endpoints within the output file, the start and endpoints
        for the binned data within the subset, and the results of the ten
        statistical checks performed by MCNP.
    """
    tally_info = (
        pd.DataFrame(regex(full_output, "1tally    "), columns=["start"])
        .assign(**{
            "end": (lambda df:
                [loc-1 for loc in df["start"][1:]]+[len(full_output)]
            ),
            "name":"", "kind":"", "dat_start":0, "dat_end":0,
            "mean_behavior":"",
            "re_value":"", "re_decrease":"", "re_rate":"",
            "vov_value":"", "vov_decrease":"", "vov_rate":"",
            "fom":"", "fom_behavior":"", "pdf_slope":""
        })
    )

    stat_checks = [
        "mean_behavior",
        "re_value", "re_decrease", "re_rate",
        "vov_value", "vov_decrease", "vov_rate",
        "fom", "fom_behavior", "pdf_slope"
    ]

    for i in range(tally_info.shape[0]):
        print(i)
        partial_output = full_output[
            int(
                tally_info.loc[i,"start"]
            ):int(
                tally_info.loc[i,"end"]
            )
        ]
        print(partial_output)
        tally_info.loc[i, "name"] = clean_split(partial_output[0])[1]
        tally_info.loc[i, "kind"] = clean_split(partial_output[1])[2]
        tally_info.loc[i, "dat_start"] = regex(partial_output, r"0\.0000E\+00")[0]
        tally_info.loc[i, "dat_end"] = regex(partial_output, "      total")[0]
        stat_check_loc = (
            regex(
                partial_output,
                "results of 10 statistical checks for the estimated answer"
            )[0] + 6
        )
        tally_info.loc[i, stat_checks] = clean_split(partial_output[stat_check_loc])[1:]

    for col in ["re_value", "vov_value", "pdf_slope"]:
        tally_info[col] = tally_info[col].to_numpy(dtype="float64")

    tally_info = (
        tally_info
        .set_index("name")
        .reset_index()
        .convert_dtypes()
    )

    return tally_info


def mcnparse_single(
    dir: str,
    file: str
) -> dict[str, pd.DataFrame | str]:

    print(file)
    with open(os.path.join(dir, file), mode="rt") as handle:
        full_output = handle.read().split(sep="\n")

    tally_info = get_tally_info(full_output).assign(run=file)

    num_tallies = tally_info.shape[0]

    binned_data = pd.concat(objs=[
        pd.DataFrame(
            data = np.array(dtype="float64",object=[# whole thing is float
                clean_split(single_bin) # bin contains energy, value, and re
                for single_bin in full_output[(
                    # starting point for the binned tally data
                    # start of tally plus the index of the bin starting relative to
                    # that section
                    tally_info.loc[i, "dat_start"] + tally_info.loc[i, "start"]
                ):(
                    # endingpoint for the binned tally data
                    # start of tally plus the index of the bin ending relative to
                    # that section
                    tally_info.loc[i, "start"] + tally_info.loc[i, "dat_end"]
                )]
            ]),
            columns=["mev", "value", "re"]
        )
        .assign(**{
            "tally": tally_info.loc[i,"name"],
            "run": file
        })
        for i in range(num_tallies)
    ])

    return {
        "summary":tally_info,
        "bins":binned_data,
        "output":full_output
    }


def mcnparse(dir: str = "") -> None:

    out_file = f"mcnp_{datetime.datetime.now().strftime(r"%Y%m%d_%H%M%S")}.json"
    outputs = find_mcnp_outputs(dir)
    all_out = {
        file:mcnparse_single(dir, file)
        for file in outputs
    }
    out = {
        "raw_data":{
            file:all_out[file]["output"]
            for file in outputs
        },
        "data":(
            pd.concat(objs=[
                all_out[file]["bins"]
                for file in outputs
            ])
            .reset_index(drop=True)
            .to_dict()
        ),
        "summary":(
            pd.concat(objs=[
                all_out[file]["summary"]
                for file in outputs
            ])
            .reset_index(drop=True)
            .to_dict()
        )
    }
    with open(os.path.join(dir, out_file), mode="wt") as handle:
        json.dump(out, handle)
