---
name: Run Sarek Pipeline
description: Execute the Sarek variant calling pipeline with generated samplesheet
stability: experimental
tags: ["sarek", "nextflow", "variant-calling", "bioinformatics"]
---

# Run Sarek Pipeline

This skill runs the Sarek nextflow pipeline for variant calling.

## Usage

Execute nextflow with the Sarek pipeline and a samplesheet.

## Parameters

- `samplesheet`: Path to samplesheet CSV
- `outdir`: Output directory
- `profile`: Nextflow profile (docker, singularity, etc.)

## Example

```bash
nextflow run nf-core/sarek -profile docker --input samplesheet.csv --outdir results
```
