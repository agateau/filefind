# Filefind

Filefind is an easy-to-use, source-code friendly file finder.

## Usage

### Listing files

To specify which files to list, use the `--include` and `--exclude` options:

    ff --include '*.cpp' --include '*.h' --exclude 'test/*'

As a special case you can also specify include values with the `--include`, so

    ff '*.cpp' '*.h'

is the same as:

    ff --include '*.cpp' --include '*.h'

### Running a command on matching files

You can use the `--exec` option to run a command on a temporary file containing
all the matched files. For example:

    ff --include '*.cpp' --include '*.h' --exclude 'test/*' --exec 'command @filelist'

### Configuration files

Options can be stored in a configuration file, so you could store all filters
in a file named `filefind.cfg` with the following content:

```
include *.cpp
include *.h

# Exclude tests
exclude test/*
```

And then list files with:

    ff --config filefind.cfg

A configuration file can refer to another configuration file with the `config`
keyword, so for example you can create `filelist.cfg` with this content:

```
include *.cpp
include *.h

# Exclude tests
exclude test/*
```

And `codestyle.cfg` which refers to it and reformats your code:

```
config filelist.cfg

exec uncrustify --replace --no-backup -F @filelist
```

Now you can reformat your code with `ff -c codestyle.cfg`.

### submodules

If you want to exclude files inside Git submodules, use the
`--exclude-submodules` option.

## Installation

    ./setup.py install

## Testing

If you want to run tests, first install the development requirements with:

    pip install -r requirements-dev.txt

Then run tests with:

    pytest

## License

Apache 2.0
