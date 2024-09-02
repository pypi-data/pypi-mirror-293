import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import math

COLOR_THEMES = [
    "Viridis", "Plasma", "Inferno", "Magma", "Cividis",
    "Twilight", "Turbo", "Deep", "Paired", "Set2"
]

def univariate_visualization(df, theme="Viridis"):
    if theme not in COLOR_THEMES:
        theme = "Viridis"

    num_columns = df.shape[1]
    num_rows = math.ceil(num_columns / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, column in enumerate(df.columns):
        sns.histplot(df[column], bins=30, ax=axes[i], kde=False, color=theme.lower())
        axes[i].set_title(f'Univariate Analysis of {column}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def bivariate_visualization(df, target_column, theme="Viridis"):
    if theme not in COLOR_THEMES:
        theme = "Viridis"

    num_columns = len([col for col in df.columns if col != target_column])
    num_rows = math.ceil(num_columns / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, column in enumerate(df.columns):
        if column != target_column:
            sns.boxplot(x=target_column, y=column, data=df, ax=axes[i], palette=theme.lower())
            axes[i].set_title(f'Bivariate Analysis of {column} vs {target_column}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def multivariate_visualization(df, theme="Viridis"):
    if theme not in COLOR_THEMES:
        theme = "Viridis"

    sns.pairplot(df, palette=theme.lower())
    plt.title('Multivariate Analysis')
    plt.show()

def correlation_heatmap(df, theme="coolwarm"):
    plt.figure(figsize=(12, 10))
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap=theme)
    plt.title("Correlation Matrix")
    plt.show()

def interactive_heatmap(df, theme="Viridis"):
    corr_matrix = df.corr().values
    labels = df.columns.tolist()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=labels,
        y=labels,
        colorscale=theme
    ))
    fig.update_layout(title="Interactive Correlation Matrix")
    fig.show()

def kde_plot(data, continuous_vars, hue=None, theme="Viridis"):
    if theme not in COLOR_THEMES:
        theme = "Viridis"

    num_vars = len(continuous_vars)
    num_rows = math.ceil(num_vars / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, var in enumerate(continuous_vars):
        sns.kdeplot(data=data, x=var, hue=hue, fill=True, ax=axes[i], palette=theme.lower())
        axes[i].set_title(f'KDE Plot for {var}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def boxen_plot(data, continuous_vars, hue=None, theme="Viridis"):
    if theme not in COLOR_THEMES:
        theme = "Viridis"

    num_vars = len(continuous_vars)
    num_rows = math.ceil(num_vars / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, var in enumerate(continuous_vars):
        sns.boxenplot(data=data, x=var, hue=hue, ax=axes[i], palette=theme.lower())
        axes[i].set_title(f'Boxen Plot for {var}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def count_plot(data, categorical_vars, hue=None, theme="Viridis"):
    if theme not in COLOR_THEMES:
        theme = "Viridis"

    num_vars = len(categorical_vars)
    num_rows = math.ceil(num_vars / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, var in enumerate(categorical_vars):
        sns.countplot(data=data, x=var, hue=hue, ax=axes[i], palette=theme.lower())
        axes[i].set_title(f'Count Plot for {var}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def scatter_3d_plot(data, continuous_vars, hue=None):
    if len(continuous_vars) < 3:
        raise ValueError("3D scatter plot requires at least 3 continuous variables.")

    fig = px.scatter_3d(data, x=continuous_vars[0], y=continuous_vars[1], z=continuous_vars[2], color=hue)
    fig.update_layout(title=f'3D Scatter Plot of {continuous_vars[0]}, {continuous_vars[1]}, {continuous_vars[2]}')
    fig.show()
