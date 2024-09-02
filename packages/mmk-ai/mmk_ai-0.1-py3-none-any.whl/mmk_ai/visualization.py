import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

COLOR_THEMES = [
    "Viridis", "Plasma", "Inferno", "Magma", "Cividis",
    "Twilight", "Turbo", "Deep", "Paired", "Set2"
]

def univariate_visualization(df, theme="Viridis"):
    if theme not in COLOR_THEMES:
        theme = "Viridis"
        
    for column in df.columns:
        fig = px.histogram(df, x=column, nbins=30, title=f'Univariate Analysis of {column}', color_discrete_sequence=px.colors.sequential.__getattribute__(theme))
        fig.show()

def bivariate_visualization(df, target_column, theme="Viridis"):
    if theme not in COLOR_THEMES:
        theme = "Viridis"
        
    for column in df.columns:
        if column != target_column:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=target_column, y=column, data=df, palette=theme.lower())
            plt.title(f'Bivariate Analysis of {column} vs {target_column}')
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
