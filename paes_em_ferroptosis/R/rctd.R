#!/usr/bin/env Rscript
# SCTransform + RCTD hook: spatial deconvolution with scRNA-seq reference.
# Usage: Rscript rctd.R <raw_dir> <results_dir>
# Requires: Seurat, spacexr (install_github("dmcable/spacexr"))
suppressMessages({ library(Seurat); library(spacexr) })
args <- commandArgs(trailingOnly = TRUE)
raw <- args[1]; results <- args[2]

sc_counts <- as.matrix(read.csv(file.path(raw, "sc_counts.csv"), row.names = 1))
sc_meta <- read.csv(file.path(raw, "sc_meta.csv"))
sp_counts <- as.matrix(read.csv(file.path(raw, "spatial_counts.csv"), row.names = 1))
coords <- read.csv(file.path(raw, "spatial_coords.csv"))

reference <- Reference(sc_counts,
                       setNames(factor(sc_meta$cell_type), sc_meta$cell))
puck <- SpatialRNA(data.frame(row.names = coords$spot,
                              x = coords$x, y = coords$y), sp_counts)
rctd <- create.RCTD(puck, reference, max_cores = 2)
rctd <- run.RCTD(rctd, doublet_mode = "full")
weights <- normalize_weights(rctd@results$weights)
write.csv(as.matrix(weights), file.path(results, "s09_rctd_weights.csv"))
cat("RCTD done\n")
