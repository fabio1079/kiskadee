A common static analysis report notation
========================================

Since we want to compare and rank static analysis warnings, we want to store
our static analysis reports in the same notation for each single static
analyzer we run in a software package. Thus, kiskadee uses `firehose
<https://github.com/fedora-static-analysis/firehose>`_. All reports stored in
kiskadee database are in firehose JSON format and each static analyzer run by
kiskadee must have a parser included in firehose upstream.
