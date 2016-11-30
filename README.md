# processall

## Goal

Apply various processors to files inside a project.

## Usage

To list files to process:

    processall --include '*.cpp' --include '*.h' --exclude 'test/*'

To actually process files:

    processall --include '*.cpp' --include '*.h' --exclude 'test/*' --exec 'command @filelist'

Options can be stored in a configuration file, so you could store all filters
in a file named `processall.cfg` with the following content:

```
include *.cpp
include *.h

# Exclude tests
exclude test/*
```

And then list files with:

    processall --config processall.cfg

And process files with:

    process --config processall.cfg --exec 'command @filelist'

You can even define the `exec` option in the configuration file if you want.

## Installation

    ./setup.py install

## Testing

If you want to run tests, first install the development requirements with

    pip install -r requirements-dev.txt

Then run tests with:

    pytest
