#!/usr/bin/env Rscript
# Seurat + CytoTRACE + Monocle2 hook (exact paper methods).
# Usage: Rscript singlecell.R <raw_dir> <results_dir>
# Requires: Seurat, CytoTRACE, monocle (Bioconductor / GitHub installs).
suppressMessages({ library(Seurat) })
args <- commandArgs(trailingOnly = TRUE)
raw <- args[1]; results <- args[2]

counts <- read.csv(file.path(raw, "sc_counts.csv"), row.names = 1)
obj <- CreateSeuratObject(counts = as.matrix(counts),
                          min.cells = 3, min.features = 200)
obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^MT-")
obj <- subset(obj, subset = percent.mt < 20)
obj <- NormalizeData(obj) |> FindVariableFeatures() |> ScaleData() |>
  RunPCA(verbose = FALSE) |> FindNeighbors(dims = 1:20) |>
  FindClusters(resolution = 0.5) |> RunUMAP(dims = 1:20)
write.csv(obj@meta.data, file.path(results, "s08_cell_meta.csv"))

# CytoTRACE stemness
if (requireNamespace("CytoTRACE", quietly = TRUE)) {
  ct <- CytoTRACE::CytoTRACE(as.matrix(counts))
  write.csv(data.frame(cell = names(ct$CytoTRACE),
                       stemness = ct$CytoTRACE),
            file.path(results, "s08_cytotrace.csv"), row.names = FALSE)
}

# Monocle2 pseudotime
if (requireNamespace("monocle", quietly = TRUE)) {
  suppressMessages(library(monocle))
  cds <- newCellDataSet(as.matrix(counts),
                        phenoData = new("AnnotatedDataFrame", obj@meta.data))
  cds <- estimateSizeFactors(cds); cds <- estimateDispersions(cds)
  cds <- reduceDimension(cds, method = "DDRTree")
  cds <- orderCells(cds)
  write.csv(data.frame(cell = colnames(cds),
                       pseudotime = cds$Pseudotime, state = cds$State),
            file.path(results, "s08_pseudotime.csv"), row.names = FALSE)
}
cat("single-cell R hook done\n")
