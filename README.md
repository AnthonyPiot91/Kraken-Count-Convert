# Kraken Count Convert
Convert Kraken read count to nucleotide count

## Step 1: Create kraken inspect file
Before running `convert_kraken_report_read_count_to_bases.py` or `convert_kraken_log_read_count_to_bases.py` you will need to run `kraken-inspect` on the database you used to obtain you Kraken results using the `--use-mpa-style` option.

> kraken-inspect --db <your_DB> --use-mpa-style > kraken2-inspect_results

## Step 2: Convert the read count in the report file to a nucleotide count
The report file needs to be in MPA style (`--use-mpa-style`)
> python convert_kraken_report_read_count_to_bases.py <kraken_result_folder_path> <kraken_results_prefix> <kraken-inspect_report_file_path> <output_files_path>

## Step 3 (Optional): Convert the read count in the log file to a nucleotide count
> python convert_kraken_log_read_count_to_bases.py <kraken_result_folder_path> <kraken_results_prefix> <output_files_path>
