import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from numpy.typing import NDArray
from scipy.interpolate import griddata


def plot_giwaxs_with_missing_wedge(
    qr_2d: NDArray[np.float64],
    qz_2d: NDArray[np.float64],
    intensity_2d: NDArray[np.float64],
    grid_resolution: int = 500,
    log_scale: bool = True,
) -> None:
    """Resample GIWAXS 2D data onto a uniform grid to show the physical missing wedge."""

    # 1. Flatten original 2D coordinate matrices into 1D points
    points = np.column_stack((qr_2d.ravel(), qz_2d.ravel()))
    values = intensity_2d.ravel()

    # Filter out invalid values (e.g., negative or NaN)
    valid_mask = np.isfinite(values) & (values > 0)
    points = points[valid_mask]
    values = values[valid_mask]

    # 2. Define target uniform grid boundaries
    qr_min, qr_max = np.nanmin(qr_2d), np.nanmax(qr_2d)
    qz_min, qz_max = np.nanmin(qz_2d), np.nanmax(qz_2d)

    grid_qr = np.linspace(qr_min, qr_max, grid_resolution)
    grid_qz = np.linspace(qz_min, qz_max, grid_resolution)
    Grid_Qr, Grid_Qz = np.meshgrid(grid_qr, grid_qz)

    # 3. Interpolate data onto the uniform grid (Unmeasured regions will become NaN)
    intensity_grid = griddata(
        points, values, (Grid_Qr, Grid_Qz), method="linear", fill_value=np.nan
    )

    # 4. Set up plot
    fig, ax = plt.subplots(figsize=(8, 7), dpi=150)

    # Set background color to dark gray/black so the missing wedge stands out
    ax.set_facecolor("#2b2b2b")

    vmax = np.nanpercentile(intensity_grid, 99.5)
    vmin = np.nanpercentile(intensity_grid, 5) if log_scale else np.nanmin(intensity_grid)
    norm = LogNorm(vmin=vmin, vmax=vmax) if log_scale else None

    # Plot using imshow on uniform grid
    img = ax.imshow(
        intensity_grid,
        origin="lower",
        extent=[qr_min, qr_max, qz_min, qz_max],
        cmap="viridis",
        norm=norm,
        aspect="equal",
    )

    # Add colorbar
    cbar = fig.colorbar(img, ax=ax, pad=0.02)
    cbar.set_label(r"Intensity (a.u.)", rotation=270, labelpad=15)

    # Horizon line (Sample Surface, Qz = 0)
    ax.axhline(0, color="white", linestyle="--", linewidth=1, alpha=0.7, label="Sample Surface ($q_z=0$)")

    ax.set_xlabel(r"$q_r\ (\AA^{-1})$", fontsize=12)
    ax.set_ylabel(r"$q_z\ (\AA^{-1})$", fontsize=12)
    ax.set_title("GIWAXS Reciprocal Space Map (Missing Wedge Visible)", fontsize=13)
    ax.legend(loc="upper right", fontsize=9)

    plt.tight_layout()
    plt.show()

qz_matrix = np.loadtxt("G:/My Drive/Data/GIWAXS from Rice/MA-FPEA_GIWAXS/MA-FPEA_GIWAXS/text files/qz_coordinates.txt") 
qr_matrix = np.loadtxt("G:/My Drive/Data/GIWAXS from Rice/MA-FPEA_GIWAXS/MA-FPEA_GIWAXS/text files/qr_coordinates.txt") 
intensity = np.loadtxt("G:/My Drive/Data/GIWAXS from Rice/MA-FPEA_GIWAXS/MA-FPEA_GIWAXS/text files/P0484_AR_MA_ctrl_RT_xpos000_deg1000_eps0000_up_deg100_stitched.txt") 
intensity_corrected = intensity.T

# Usage:
plot_giwaxs_with_missing_wedge(qr_matrix, qz_matrix, intensity_corrected)

# if __name__ == "__main__":

#     qz_2d = np.loadtxt("G:/My Drive/Data/GIWAXS from Rice/MA-FPEA_GIWAXS/MA-FPEA_GIWAXS/text files/qz_coordinates.txt")       # shape: (981, 1043)
#     qr_2d = np.loadtxt("G:/My Drive/Data/GIWAXS from Rice/MA-FPEA_GIWAXS/MA-FPEA_GIWAXS/text files/qr_coordinates.txt")       # shape: (981, 1043)
#     intensity = np.loadtxt("G:/My Drive/Data/GIWAXS from Rice/MA-FPEA_GIWAXS/MA-FPEA_GIWAXS/text files/P0484_AR_MA_ctrl_RT_xpos000_deg1000_eps0000_up_deg100_stitched.txt")  # shape: (981, 1043)
#     plot_giwaxs_2d_coords(qz_2d, qr_2d, intensity)
    
#     # qz, qr, intensity = load_giwaxs_data("G:/My Drive/Data/GIWAXS from Rice/MA-FPEA_GIWAXS/MA-FPEA_GIWAXS/text files/qz_coordinates.txt", "G:/My Drive/Data/GIWAXS from Rice/MA-FPEA_GIWAXS/MA-FPEA_GIWAXS/text files/qr_coordinates.txt", "G:/My Drive/Data/GIWAXS from Rice/MA-FPEA_GIWAXS/MA-FPEA_GIWAXS/text files/P0484_AR_MA_ctrl_RT_xpos000_deg1000_eps0000_up_deg100_stitched.txt")
#     # fig = plot_giwaxs_map(qz, qr, intensity)
#     plt.show()
#     pass