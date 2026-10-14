#!/usr/bin/env Rscript
# scTenifoldKnk hook: virtual knockout of the key gene in fibroblasts.
# Usage: Rscript sctenifoldknk.R <raw_dir> <results_dir> [gene] [cell_type]
# Requires: scTenifoldKnk (install.packages("scTenifoldKnk"))
suppressMessages(library(scTenifoldKnk))
args <- commandArgs(trailingOnly = TRUE)
raw <- args[1]; results <- args[2]
gene <- ifelse(length(args) >= 3, args[3], "ARF6")
ctype <- ifelse(length(args) >= 4, args[4], "Fibroblasts")

counts <- as.matrix(read.csv(file.path(raw, "sc_counts.csv"), row.names = 1))
meta <- read.csv(file.path(raw, "sc_meta.csv"))
cells <- meta$cell[meta$cell_type == ctype]
res <- scTenifoldKnk(countMatrix = counts[, cells], gKO = gene)
write.csv(res$diffRegulation, file.path(results, "s10_perturbation.csv"),
          row.names = FALSE)
cat("scTenifoldKnk done for", gene, "in", ctype, "\n")
