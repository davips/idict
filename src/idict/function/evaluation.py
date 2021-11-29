#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the i-dict project.
#  Please respect the license - more about this in the section (*) below.
#
#  i-dict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  i-dict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with i-dict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and it is unethical regarding the effort and
#  time spent here.
#

def split(input=["X", "y"], output=["Xtr", "ytr", "Xts", "yts"],
          config={"test_size": 33, "shuffle": True, "stratify": "y", "random_state": 0}, **kwargs):
    if input != ["X", "y"] or output != ["Xtr", "ytr", "Xts", "yts"]:
        # TODO create a way in ldict to accept a dynamic dict as return value
        raise Exception(f"Not implemented for input/output different from default values: "
                        f"{input} / {output}")
    from sklearn.model_selection import train_test_split

    # Multidynamic input is only detected when the kwargs index is also indexed by something.
    args = {field: kwargs[field] for i, field in enumerate(input)}
    if "stratify" in config and isinstance(config["stratify"], str):
        if config["stratify"] not in input:  # pragma: no cover
            raise Exception(f"Missing field {config['stratify']} for stratification.")
        config["stratify"] = args[config["stratify"]]
    Xtr, Xts, ytr, yts = train_test_split(*args.values(), **config)
    return {"Xtr": Xtr, "ytr": ytr, "Xts": Xts, "yts": yts, "_history": ...}


split.metadata = {
    "id": "split----------------------sklearn-1.0.1",
    "name": "split",
    "description": "Split data in two sets.",
    "parameters": ...,
    "code": ...,
}
