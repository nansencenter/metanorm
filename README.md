[![Build Status](https://travis-ci.org/nansencenter/metanorm.svg?branch=master)](https://travis-ci.org/nansencenter/metanorm)
[![Coverage Status](https://coveralls.io/repos/github/nansencenter/metanorm/badge.svg?branch=init)](https://coveralls.io/github/nansencenter/metanorm?branch=master)

# Metadata normalizing tool

The purpose of this tool is to extract a defined set of parameter from raw metadata. It is meant
primarily for use with geo-spatial datasets, but can be extend to process any kind of data.

## Principle

**Input**:
  - a list of parameter for which values must be found
  - raw metadata attributes in the form of a dictionary

**Output**: a dictionary in which the parameter names given as input are associated with the values
found in the raw attributes.

The actual work of associating attribute values to the parameters is done by **normalizers**. Each
normalizer is able to fill in the values of some parameters, if the corresponding attribute(s) are
found in the raw metadata.

The raw metadata attributes are processed in a chain of normalizers, each of which will attempt to
find a value for the parameters it knows.

At the end of the chain, if a value was found for all the
parameters, a dictionary is returned, otherwise an exception is raised. In order to ensure this
behavior, the last normalizer in the chain **must** inherit from the `BaseDefaultMetadataNormalizer`
class.
