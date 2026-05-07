.. image:: ../images/pVACsplice_logo_trans-bg_v4b.png
    :align: right
    :alt: pVACsplice logo
    :width: 175px

.. _pvacsplice_filter_commands:

Filtering Commands
==================

pVACsplice currently offers four filters: a binding filter, a coverage filter,
a transcript filter, and a top score filter.

These filters are always run automatically as part
of the pVACsplice pipeline using default cutoffs.

All filters can also be run manually on the filtered.tsv file to narrow the results down further,
or they can be run on the all_epitopes.tsv file to apply different filtering thresholds.

The binding filter is used to remove neoantigen candidates that do not meet desired peptide:MHC binding criteria.
The coverage filter is used to remove variants that do not meet desired read count and VAF criteria (in normal DNA
and tumor DNA/RNA). The transcript filter is used to remove variant annotations based on low quality
transcript annotations. The top score filter is used to select the most promising peptide candidate for each variant.
Multiple candidate peptides from a single somatic variant can be caused by multiple peptide lengths, registers, HLA alleles,
and transcript annotations.

Further details on each of these filters is provided below.

.. note::

   The default values for filtering thresholds are suggestions only. While they are based on review of the literature
   and consultation with our clinical and immunology colleagues, your specific use case will determine the appropriate values.

Binding Filter
--------------

.. program-output:: pvacsplice binding_filter -h

The binding filter removes variants that don't pass the chosen binding threshold.
The user can chose whether to apply this filter to the ``lowest`` or the ``median`` binding
affinity score by setting the ``--top-score-metric`` flag. The ``lowest`` binding
affinity score is recorded in the ``Best MT IC50 Score`` column and represents the lowest
ic50 score of all prediction algorithms that were picked during the previous pVACseq run.
The ``median`` binding affinity score is recorded in the ``Median MT IC50 Score`` column and
corresponds to the median ic50 score of all prediction algorithms used to create the report.
Be default, the binding filter runs on the ``median`` binding affinity.
An additional ``--top-score-metric2`` flag allows the user to choose whether to use IC50 or
Percentile scores. By default, IC50 is used.

When the ``--allele-specific-binding-thresholds`` flag is set, binding cutoffs specific to each
prediction's HLA allele are used instead of the value set via the ``--binding-threshold`` parameters.
For HLA alleles where no allele-specific binding threshold is available, the
binding threshold is used as a fallback. Alleles with allele-specific
threshold as well as the value of those thresholds can be printed by executing
the ``pvacsplice allele_specific_cutoffs`` command.

In addition to being able to filter on the IC50 score columns, the binding
filter also offers the ability to filter on the percentile score using the
``--percentile-threshold`` parameter. When the ``--top-score-metric`` is set
to ``lowest``, this threshold is applied to the ``Best MT Percentile`` column. When
it is set to ``median``, the threshold is applied to the ``Median MT
Percentile`` column.

When the ``--percentile-threshold`` flag is set, the candidate inclusion strategy can be
specified by using the ``--percentile-threshold-strategy`` parameter. The parameter has two
options ``conservative`` (default) and ``exploratory``. The 'conservative' option requires a candidate 
to pass BOTH the binding threshold and percentile threshold, while the 'exploratory' option requires
a candidate to pass EITHER the binding threshold or percentile threshold.

By default, entries with ``NA`` values will be included in the output. This
behavior can be turned off by using the ``--exclude-NAs`` flag.

Coverage Filter
---------------

.. program-output:: pvacsplice coverage_filter -h

If the pVACsplice input VCF contains readcount and/or expression annotations, then the coverage filter
can be run again on the filtered.tsv report file to narrow down the results even further.
You can also run this filter again on the all_epitopes.tsv report file to apply different cutoffs.

The general goals of these filters are to limit variants for neoepitope prediction to those
with good read support and/or remove possible sub-clonal variants. In some cases the input
VCF may have already been filtered in this fashion. This filter also allows for removal of
variants that do not have sufficient evidence of RNA expression.

For more details on how to prepare input VCFs that contain all of these annotations, refer to
the :ref:`pvacsplice_prerequisites_label` section for more information.

By default, entries with ``NA`` values will be included in the output. This
behavior can be turned off by using the ``--exclude-NAs`` flag.

Transcript Filter
-----------------

.. program-output:: pvacsplice transcript_filter -h

This filter is used to eliminate variant annotations based on poorly-supported transcripts. This assessed
based on whether the transcript is the MANE Select transcripts, whether it is
the canonical transcript or whether the transcript support level (TSL) meets the
``--maximum-transcript-support-level`` cutoff. The
``--transcript-prioritizatio-strategy`` parameter controlls which ones of these three
criteria are considered. A neoantigen candidate passes this filter if its
transcript passes at least one of the specified criteria.

Transcript with a TSL of ``Not Supported`` will pass the TSL criteria. These values occur if VEP was run
without the ``--tsl`` flag or if data is aligned to GRCh37 or older.

Top Score Filter
----------------

.. program-output:: pvacsplice top_score_filter -h

This filter picks the top epitope for each junction according to the following criteria:

- If ``--allow-inclomplete-transcripts`` flag is set, pick the entries without
  a ``Transcript CDS Flags`` set.
- Of the remaining entries, pick the entries where the ``Biotype`` is ``protein_coding``.
- Of the remaining entries, pick the entries that pass at least one of the transcript criteria selected in the
  ``--transcript-prioritization-strategy`` taking into consideration the
  ``--maximum-transcript-support-level`` if ``tsl`` is one of the selected
  criteria.
- Of the remaining entries, pick the entries with no ``Problematic Positions``.
- Sort the remaining entries by lowest ``Median|Best IC50 Score|Percentile``
  (depending on the selected ``--top-score-metric`` and
  ``--top-score-metric2``), ``MANE Select`` (True), ``Canonical`` (True),
  ``Transcript Support Level``, ``WT Protein Length``, and ``Transcript
  Expression``. Select the highest sorted entry.

Aggregate Report Filter
-----------------------

.. program-output:: pvacsplice aggregate_report_filter -h

This command filters the aggregate report to only those variants matching the
specified ``--include-tiers`` (default:Pass).
