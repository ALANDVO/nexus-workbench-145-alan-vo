---
name: Generate Sarek Samplesheet
description: Generate a Sarek pipeline samplesheet from FASTQ or BAM files
stability: stable
tags: ["sarek", "samplesheet", "nextflow", "bioinformatics"]
---

# Generate Sarek Samplesheet

This skill generates a valid samplesheet for the Sarek nextflow pipeline.

## Usage

Run the `generate_samplesheet.py` script with appropriate arguments.

## Parameters

- `input_dir`: Directory containing FASTQ or BAM files
- `pipeline`: Pipeline name (sarek)
- `input_type`: Type of input (fastq, bam, cram)
- `output`: Output CSV file path

## Example

```bash
python generate_samplesheet.py ./fastqs sarek --input-type fastq -o samplesheet.csv
```
