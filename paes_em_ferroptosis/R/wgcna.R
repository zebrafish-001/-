#!/usr/bin/env Rscript
# WGCNA hook: exact-method module detection for the training dataset.
# Usage: Rscript wgcna.R <processed_dir> <results_dir> <accession>
# Requires: WGCNA (BiocManager::install("WGCNA"))
suppressMessages({ library(WGCNA); options(stringsAsFactors = FALSE) })
args <- commandArgs(trailingOnly = TRUE)
processed <- args[1]; results <- args[2]; acc <- args[3]

expr <- read.csv(file.path(processed, paste0(acc, "_expr.csv")), row.names = 1)
groups <- read.csv(file.path(processed, paste0(acc, "_groups.csv")), row.names = 1)
trait <- as.numeric(groups$group == "EM")

mad_v <- apply(expr, 1, mad)
expr <- expr[order(mad_v, decreasing = TRUE)[seq_len(min(5000, nrow(expr)))], ]
datExpr <- t(expr)

powers <- 1:20
sft <- pickSoftThreshold(datExpr, powerVector = powers, RsquaredCut = 0.85,
                         verbose = 0)
beta <- ifelse(is.na(sft$powerEstimate), 6, sft$powerEstimate)

net <- blockwiseModules(datExpr, power = beta, TOMType = "unsigned",
                        minModuleSize = 30, mergeCutHeight = 0.25,
                        numericLabels = TRUE, verbose = 0)
MEs <- moduleEigengenes(datExpr, colors = net$colors)$eigengenes
cor_t <- cor(MEs, trait, use = "p")
p_t <- corPvalueStudent(cor_t, nrow(datExpr))

mt <- data.frame(module = sub("^ME", "", rownames(cor_t)),
                 trait_cor = as.numeric(cor_t), trait_p = as.numeric(p_t))
write.csv(mt, file.path(results, "s04_module_trait.csv"), row.names = FALSE)
write.csv(data.frame(gene = colnames(datExpr), module = net$colors),
          file.path(results, "s04_modules.csv"), row.names = FALSE)

key_mods <- mt$module[mt$trait_p < 0.05]
key_genes <- colnames(datExpr)[net$colors %in% as.numeric(key_mods)]
writeLines(jsonlite::toJSON(key_genes),
           file.path(processed, "wgcna_key_genes.json"))
cat("WGCNA done: beta=", beta, " key modules=", length(key_mods), "\n")
