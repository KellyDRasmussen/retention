"""
custom_viz_styling.py
A reusable module for consistent matplotlib/seaborn visualization styling
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import numpy as np

# Define the custom color palette based on preferred colors
TEAL = "#69C4C0"
BLUE = "#43AEFF"
ORANGE = "#E08800"  # For contrast/highlights
BG_LIGHT = "#F5FFE5"
BG_WHITE = "#F8FAFB"

# Extended color palette (variations of the main colors)
COLORS = {
    'teal': TEAL,
    'teal_light': '#A7DEDA',
    'teal_dark': '#419693',
    'blue': BLUE,
    'blue_light': '#9AD2FF',
    'blue_dark': '#1C87D6',
    'orange': ORANGE,
    'orange_light': '#FFBC66',
    'orange_dark': '#B36D00',
    'bg_light': BG_LIGHT,
    'bg_white': BG_WHITE,
    'gray_light': '#EEEEEE',
    'gray': '#CCCCCC',
    'gray_dark': '#888888',
    'text': '#333333'
}

# Create custom colormaps
teal_cmap = LinearSegmentedColormap.from_list('teal_cmap', [COLORS['bg_white'], COLORS['teal']])
blue_cmap = LinearSegmentedColormap.from_list('blue_cmap', [COLORS['bg_white'], COLORS['blue']])
teal_blue_cmap = LinearSegmentedColormap.from_list('teal_blue_cmap', [COLORS['teal'], COLORS['blue']])
teal_orange_cmap = LinearSegmentedColormap.from_list('teal_orange_cmap', [COLORS['teal'], COLORS['orange']])

# Default color sequence for multiple series
COLOR_CYCLE = [TEAL, BLUE, ORANGE, COLORS['teal_dark'], COLORS['blue_dark'], 
               COLORS['teal_light'], COLORS['blue_light'], COLORS['orange_light']]

def setup_styling():
    """
    Set up the custom matplotlib style settings.
    Call this at the beginning of your notebook.
    """
    # Check if Georgia is available, otherwise fall back to serif
    font_family = 'Georgia'
    available_fonts = set(f.name for f in mpl.font_manager.fontManager.ttflist)
    if 'Georgia' not in available_fonts:
        font_family = 'serif'
    
    # Create custom style dictionary
    custom_style = {
        # Figure
        'figure.figsize': (10, 6),
        'figure.facecolor': BG_WHITE,
        'figure.dpi': 100,
        
        # Fonts
        'font.family': font_family,
        'font.size': 11,
        'axes.titlesize': 16,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        
        # Axes
        'axes.facecolor': BG_WHITE,
        'axes.edgecolor': COLORS['gray'],
        'axes.linewidth': 1.0,
        'axes.grid': True,
        'axes.prop_cycle': plt.cycler('color', COLOR_CYCLE),
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.axisbelow': True,  # This ensures grid lines are drawn behind plot elements
        
        # Grid
        'grid.color': COLORS['gray_light'],
        'grid.linestyle': '--',
        'grid.linewidth': 0.5,
        'grid.alpha': 0.7,
        
        # Ticks
        'xtick.color': COLORS['text'],
        'ytick.color': COLORS['text'],
        'xtick.major.size': 3.5,
        'ytick.major.size': 3.5,
        
        # Legend
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.edgecolor': COLORS['gray_light'],
        'legend.facecolor': BG_WHITE,
        
        # Saving figures
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.facecolor': BG_WHITE,
    }
    
    # Apply style
    plt.rcParams.update(custom_style)
    
    # Create a custom seaborn color palette
    sns.set_palette(COLOR_CYCLE)
    
    print("Custom visualization styling applied successfully.")

def create_custom_cmap(start_color, end_color, name='custom_cmap'):
    """
    Create a custom colormap between two colors
    
    Parameters:
    -----------
    start_color, end_color : str
        Hex color codes for the start and end of the colormap
    name : str
        Name for the colormap
        
    Returns:
    --------
    cmap : matplotlib.colors.LinearSegmentedColormap
        The custom colormap
    """
    return LinearSegmentedColormap.from_list(name, [start_color, end_color])

def apply_chart_style(ax, title=None, xlabel=None, ylabel=None, 
                      legend_title=None, legend_loc='best',
                      grid=True, spines=True, tight_layout=True):
    """
    Apply consistent styling to a chart
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes to style
    title, xlabel, ylabel : str, optional
        Text for title and axis labels
    legend_title : str, optional
        Title for the legend
    legend_loc : str, default='best'
        Location for the legend
    grid : bool, default=True
        Whether to show the grid
    spines : bool, default=True
        If False, remove all spines
    tight_layout : bool, default=True
        Whether to apply tight layout
    """
    # Set title and labels if provided
    if title:
        ax.set_title(title, fontsize=16, pad=15)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
        
    # Configure legend if there is one
    if ax.get_legend():
        if legend_title:
            ax.legend(title=legend_title, loc=legend_loc, frameon=True, 
                      facecolor=BG_WHITE, edgecolor=COLORS['gray_light'])
        else:
            ax.legend(loc=legend_loc, frameon=True, 
                      facecolor=BG_WHITE, edgecolor=COLORS['gray_light'])
    
    # Make sure grid lines appear behind plot elements
    ax.set_axisbelow(True)
    
    # Grid settings
    ax.grid(grid, linestyle='--', alpha=0.7, color=COLORS['gray_light'])
    
    # Spine settings
    if not spines:
        for spine in ax.spines.values():
            spine.set_visible(False)
    else:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['gray'])
        ax.spines['bottom'].set_color(COLORS['gray'])
    
    # Apply tight layout if requested
    if tight_layout:
        plt.tight_layout()

def savefig_with_background(fig, filename, dpi=300, facecolor=BG_WHITE):
    """
    Save figure with proper background color and tight bbox
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure to save
    filename : str
        Path to save the figure
    dpi : int, default=300
        DPI for the saved figure
    facecolor : str, default=BG_WHITE
        Background color
    """
    fig.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor=facecolor)

# Seaborn theme function
def set_seaborn_theme():
    """
    Apply a custom seaborn theme that matches our style
    """
    sns.set_theme(
        style="ticks",
        palette=COLOR_CYCLE,
        font=plt.rcParams['font.family'],
        rc={
            "figure.facecolor": BG_WHITE,
            "axes.facecolor": BG_WHITE,
            "grid.color": COLORS['gray_light'],
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.axisbelow": True,  # Ensure grid lines are below plot elements
        }
    )
    # Remove top and right spines
    sns.despine()
