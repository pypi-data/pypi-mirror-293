# comtrade-pysharp
A Python wrapper to the Gemstone COMTRADE reader (C#, hence pysharp). This should make it much faster than pure python.
Additionally, it tries to keep the RAM usage fairly low, though the entire file is loaded at once.

Depending on the size of the files to be read, the time to read can be reduced by 50x.

**This package does not follow the COMTRADE standard**. In terms of data representation, we consider ``signal names``
to be the relevant part, not ``signal id``. Similarly, typically the data and names are simply put in independent lists,
and users have to re-map the arrays by themselves.
We provide the data as 2 dictionaries (one for analog, one for digital) and a list of timestamps.

In theory, all COMTRADE formats should be supported, but it's not tested. Same for different OS, architectures,
python versions.

# How it works

## C#

Internals/FileReader contains two items:
- ReaderDll, which provides a simplification layer to the [GSF.COMTRADE](https://github.com/GridProtectionAlliance/gsf)
- FileReader, which just uses the one above

The ReaderDll builds to a single dll, this is done with [ILRepack](https://github.com/gluck/il-repack).

## Python

We use the ReaderDll and access it there.
The data is then converted to [numpy](https://numpy.org/) arrays and the memory of the C# object is freed.

# data

Contains two COMTRADE files:
- One example of a big file
- One example taken from from [comtrade](https://github.com/drewsilcock/comtrade/tree/main/tests/comtrade_files)

# How to use

To use this, once installed. Call

```
from comtrade_pysharp import read_comtrade
file = "C:/my_comtrade.cfg"
data = read_comtrade(file)
```

You can also pass the following arguments ``analog_channels`` or ``digital_channels`` to keep only these channels, this
reduces the RAM usage. As well as ``subsampling`` which will do a basic subsampling of the file to further reduce RAM usage.


# licensing

No idea, everything is open source and redistributable as far as I can tell, but there's some nuget packages in there that have other licenses, so do your due diligence. Everything is put "as is" on here...
Some seem to be BSD (Antlr3 and another one)

# Warning

## First

I have no idea what I'm doing :).

![](cat.gif)

## Testing

I only tested this against one of the files I'm using, in the one version of Python I'm using (3.9.13-32 bits). There's no reason it wouldn't work for other versions, but I haven't even tried.

## Maintenance/issues

I did this "for fun" to evaluate how much faster I could make a reader using a multi-language approach. You can report issues but this is not something I want to maintain significantly, unless I see it gain a lot of traction.

# todo

## FileReader

* 	Seems the example throws an exception at the end. This appeared once I merged all dlls, not sure why.


## Python

* 	Figure out the proper way to create the package (copy the dll and make it available on pypi)
