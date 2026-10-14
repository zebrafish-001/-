#!/usr/bin/env Rscript
# limma hook: exact-method differential expression (EM vs Control).
# Usage: Rscript limma_de.R <processed_dir> <results_dir> <accession>
suppressMessages(library(limma))
args <- commandArgs(trailingOnly = TRUE)
processed <- args[1]; results <- args[2]; acc <- args[3]

expr <- read.csv(file.path(processed, paste0(acc, "_expr.csv")), row.names = 1)
groups <- read.csv(file.path(processed, paste0(acc, "_groups.csv")), row.names = 1)
design <- model.matrix(~0 + factor(groups$group, levels = c("Control", "EM")))
colnames(design) <- c("Control", "EM")
fit <- eBayes(contrasts.fit(lmFit(expr, design),
                            makeContrasts(EM - Control, levels = design)))
tab <- topTable(fit, number = Inf)
write.csv(tab, file.path(results, "s03_de_full.csv"))
sig <- tab[tab$adj.P.Val < 0.05 & abs(tab$logFC) > 0.5, ]
write.csv(sig, file.path(results, "s03_degs.csv"))
cat("limma done:", nrow(sig), "DEGs\n")
