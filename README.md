[![Unit tests and builds](https://github.com/nansencenter/metanorm/actions/workflows/ci.yml/badge.svg)](https://github.com/nansencenter/metanorm/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/nansencenter/metanorm/badge.svg?branch=init)](https://coveralls.io/github/nansencenter/metanorm?branch=master)

# Metadata normalizing tool

The purpose of this tool is to extract a defined set of parameter from raw metadata. It is meant
primarily for use with geo-spatial datasets, but can be extend to process any kind of data.

## Principle

**Input**: raw metadata attributes in the form of a dictionary

**Output**: a dictionary in which normalized parameter names are associated with values found in the
raw metadata.

The actual work of extracting attribute values from the raw metadata is done by **normalizers**.

Each normalizer is a class able to deal with a particular type of metadata. In the case of
geo-spatial datasets, a normalizer is typically able to deal with the metadata format of a
particular data provider.

## Usage

Although normalizers can be used directly, the easiest way to normalize metadata is to use a
`MetadataHandler`. A metadata handler is initialized using a base normalizer class.

When trying to normalize metadata (using the handler's `get_parameters()` method), the handler tries
all normalizers which inherit from this base class. The first normalizer which is able to deal with
the metadata is used.

To determine if a normalizer is able to deal with a dictionary of raw metadata, the handler calls
its `check()` method.

Example to normalize data for use in
[django-geo-spaas](https://github.com/nansencenter/django-geo-spaas):

```python
import metanorm.handlers as handlers
import metanorm.normalizers as normalizers

metadata_to_normalize = {
  'foo': 'bar,
  'baz': 'qux'
}

m = handlers.MetadataHandler(normalizers.geospaas.GeoSPaaSMetadataNormalizer)
normalized_metadata = m.get_parameters(metadata_to_normalize)
```
