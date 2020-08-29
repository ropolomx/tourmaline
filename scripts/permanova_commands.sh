#!/bin/bash

#bray-curtis
qiime diversity beta-group-significance \
--i-distance-matrix 04-diversity/dada2-pe/bray_curtis_distance_matrix.qza \
--m-metadata-file 00-data/metadata.tsv \
--m-metadata-column treatment \
--p-method permanova \
--p-pairwise \
--p-permutations 999 \
--o-visualization 04-diversity/dada2-pe/bray-curtis-permanova.qzv

#jaccard
qiime diversity beta-group-significance \
--i-distance-matrix 04-diversity/dada2-pe/jaccard_distance_matrix.qza \
--m-metadata-file 00-data/metadata.tsv \
--m-metadata-column treatment \
--p-method permanova \
--p-pairwise \
--p-permutations 999 \
--o-visualization 04-diversity/dada2-pe/jaccard-permanova.qzv

#unweighted
qiime diversity beta-group-significance \
--i-distance-matrix 04-diversity/dada2-pe/unweighted_unifrac_distance_matrix.qza \
--m-metadata-file 00-data/metadata.tsv \
--m-metadata-column treatment \
--p-method permanova \
--p-pairwise \
--p-permutations 999 \
--o-visualization 04-diversity/dada2-pe/unweighted-unifrac-permanova.qzv

#weighted
qiime diversity beta-group-significance \
--i-distance-matrix 04-diversity/dada2-pe/weighted_unifrac_distance_matrix.qza \
--m-metadata-file 00-data/metadata.tsv \
--m-metadata-column treatment \
--p-method permanova \
--p-pairwise \
--p-permutations 999 \
--o-visualization 04-diversity/dada2-pe/weighted-unifrac-permanova.qzv

# pielou's evenness template --> FROM QIIIME2-2020.6
# qiime diversity-lib pielou-evenness \
# --i-table ARTIFACT FeatureTable[Frequency | RelativeFrequency]
# --p-drop-undefined-samples / --p-no-drop-undefined-samples
# --o-vector ARTIFACT SampleData[AlphaDiversity]

#pielou's evenness -- too new for current qiime2
#qiime diversity pielou-evenness \
#--i-table 02-denoised/dada2-pe/table.qza \
#--p-drop-undefined-samples \
#--o-vector 04-diversity/dada2-pe/pielous_evenness_vector.qza