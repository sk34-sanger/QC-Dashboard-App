"""Table registry for QC dashboard screen datasets."""

from __future__ import annotations

from pathlib import Path

SCREEN_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "screen"

# Map variable names used in pages/screen.py to the source TSV file name.
SCREEN_DATASET_FILES: dict[str, str] = {
    "ss_df": "sample_sheet.tsv",
    "sample_qc_meta_df": "sample_qc_meta.tsv",
    "sample_qc_read_length_df": "sample_qc_read_length.tsv",
    "sample_qc_stats_missing_var_df": "sample_qc_stats_missing.tsv",
    "missing_variants_in_library_df": "missing_variants_in_library.tsv",
    "sample_qc_stats_total_df": "sample_qc_stats_total.tsv",
    "sample_qc_stats_accepted_df": "sample_qc_stats_accepted.tsv",
    "sample_qc_stats_coverage_df": "sample_qc_stats_coverage.tsv",
    "sample_qc_stats_pos_coverage_df": "sample_qc_stats_pos_coverage.tsv",
    "sample_qc_stats_pos_counts_df": "sample_qc_stats_pos_counts.tsv",
    "sample_qc_position_cov_data_df": "sample_qc_position_cov_data.tsv",
    "sample_qc_cutoffs_df": "sample_qc_cutoffs.tsv",
    "sample_qc_position_anno_df": "sample_qc_position_anno_data.tsv",
    "sample_qc_stats_pos_percentage_df": "sample_qc_stats_pos_percentage.tsv",
    "sample_data_df": "sample_data.tsv",
    "correlation_matrix_df": "correlation_matrix.tsv",
    "experiment_qc_corr_df": "experiment_qc_corr.tsv",
    "col_data_df": "exp_qc_pca_data/col_data.tsv",
    "pca_center_df": "exp_qc_pca_data/pca_center.tsv",
    "pca_scale_df": "exp_qc_pca_data/pca_scale.tsv",
    "pca_sdev_df": "exp_qc_pca_data/pca_sdev.tsv",
    "pca_rotation_df": "exp_qc_pca_data/pca_rotation_loadings.tsv",
    "pca_x_scores_df": "exp_qc_pca_data/pca_x_scores.tsv",
}

# Map variable names used in pages/screen.py to PostgreSQL table names.
SCREEN_DATASET_TABLES: dict[str, str] = {
    "ss_df": "sample_sheet",
    "sample_qc_meta_df": "sample_qc_meta",
    "sample_qc_read_length_df": "sample_qc_read_length",
    "sample_qc_stats_missing_var_df": "sample_qc_stats_missing",
    "missing_variants_in_library_df": "missing_variants_in_library",
    "sample_qc_stats_total_df": "sample_qc_stats_total",
    "sample_qc_stats_accepted_df": "sample_qc_stats_accepted",
    "sample_qc_stats_coverage_df": "sample_qc_stats_coverage",
    "sample_qc_stats_pos_coverage_df": "sample_qc_stats_pos_coverage",
    "sample_qc_stats_pos_counts_df": "sample_qc_stats_pos_counts",
    "sample_qc_position_cov_data_df": "sample_qc_position_cov_data",
    "sample_qc_cutoffs_df": "sample_qc_cutoffs",
    "sample_qc_position_anno_df": "sample_qc_position_anno_data",
    "sample_qc_stats_pos_percentage_df": "sample_qc_stats_pos_percentage",
    "sample_data_df": "sample_data",
    "correlation_matrix_df": "correlation_matrix",
    "experiment_qc_corr_df": "experiment_qc_corr",
    "col_data_df": "exp_qc_pca_col_data",
    "pca_center_df": "exp_qc_pca_center",
    "pca_scale_df": "exp_qc_pca_scale",
    "pca_sdev_df": "exp_qc_pca_sdev",
    "pca_rotation_df": "exp_qc_pca_rotation_loadings",
    "pca_x_scores_df": "exp_qc_pca_x_scores",
}
