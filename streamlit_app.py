import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Add the project root to the path for imports
sys.path.append(os.path.dirname(__file__))

from absa_main import ABSAAnalyzer

# Configure page
st.set_page_config(
    page_title="Aspect-Based Sentiment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for ABSA analyzer
if 'analyzer_loaded' not in st.session_state:
    st.session_state.analyzer_loaded = False
    st.session_state.analyzer = None

# Load ABSA analyzer on startup
@st.cache_resource
def load_absa_analyzer():
    """Initialize the ABSA analyzer with all required models"""
    try:
        with st.spinner("Initializing ABSA models (this may take a moment)..."):
            analyzer = ABSAAnalyzer()
            if analyzer.is_ready():
                return analyzer, True
            else:
                return None, False
    except Exception as e:
        st.error(f"Error initializing ABSA analyzer: {str(e)}")
        return None, False

def analyze_single_text(text, analyzer):
    """Analyze a single text using the ABSA analyzer"""
    try:
        results = analyzer.analyze_with_details(text)
        return results['aspects'] if results['aspects'] else []
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        return []

def analyze_batch_texts(texts, analyzer):
    """Analyze multiple texts and return results as DataFrame"""
    all_results = []
    
    for text_id, text in enumerate(texts):
        try:
            results = analyzer.analyze_with_details(text)
            for aspect_info in results['aspects']:
                all_results.append({
                    'text_id': text_id,
                    'text': text[:100] + "..." if len(text) > 100 else text,
                    'aspect': aspect_info['aspect'],
                    'sentiment': aspect_info['sentiment_label'],
                    'score': aspect_info['sentiment_score'],
                    'confidence': abs(aspect_info['sentiment_score'])  # Use absolute score as confidence
                })
        except Exception as e:
            st.error(f"Error analyzing text {text_id + 1}: {str(e)}")
            continue
    
    return pd.DataFrame(all_results)

def format_results_for_display(results):
    """Format analysis results for display in Streamlit"""
    if not results:
        return pd.DataFrame()
    
    formatted_data = []
    for aspect_info in results:
        formatted_data.append({
            'Aspect': aspect_info['aspect'],
            'Sentiment': aspect_info['sentiment_label'],
            'Score': round(aspect_info['sentiment_score'], 3),
            'Confidence': round(abs(aspect_info['sentiment_score']), 3)
        })
    
    return pd.DataFrame(formatted_data)

# Title and description
st.title("📊 Aspect-Based Sentiment Analysis")
st.markdown("Analyze sentiment across different aspects of your text using advanced NLP techniques.")

# Load ABSA analyzer
analyzer, analyzer_loaded = load_absa_analyzer()
if analyzer_loaded:
    st.success("✅ ABSA Analyzer initialized successfully!")
    st.session_state.analyzer = analyzer
    st.session_state.analyzer_loaded = True
else:
    st.error("❌ Failed to initialize ABSA analyzer. Please check your environment setup.")
    st.stop()

# Sidebar
st.sidebar.header("Configuration")
analysis_type = st.sidebar.selectbox(
    "Choose Analysis Type",
    ["Single Text", "Batch Analysis", "File Upload"]
)

# Main content based on selection
if analysis_type == "Single Text":
    st.header("Single Text Analysis")
    
    # Text input
    user_text = st.text_area(
        "Enter your text for analysis:",
        placeholder="e.g., The food was delicious but the service was terrible and the ambiance was okay...",
        height=150
    )
    
    if st.button("Analyze", type="primary") and user_text:
        with st.spinner("Analyzing text for aspects and sentiments..."):
            try:
                # Analyze the user input
                results = analyze_single_text(user_text, analyzer)
                
                if results:
                    # Format results for display
                    results_df = format_results_for_display(results)
                    
                    # Display results
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("Aspect-Sentiment Results")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name="sentiment_analysis_results.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        st.subheader("Sentiment Distribution")
                        if len(results_df) > 0:
                            # Create color mapping
                            color_map = {
                                "Positive": "#2E8B57",
                                "Negative": "#DC143C", 
                                "Neutral": "#708090"
                            }
                            
                            fig = px.bar(
                                results_df, 
                                x="Aspect", 
                                y="Score", 
                                color="Sentiment",
                                color_discrete_map=color_map,
                                title="Sentiment Scores by Aspect"
                            )
                            fig.update_layout(xaxis_tickangle=-45)
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Additional visualizations
                    st.subheader("📊 Detailed Analysis")
                    
                    col3, col4 = st.columns([1, 1])
                    
                    with col3:
                        # Pie chart for sentiment distribution
                        sentiment_counts = results_df['Sentiment'].value_counts()
                        if len(sentiment_counts) > 0:
                            fig_pie = px.pie(
                                values=sentiment_counts.values,
                                names=sentiment_counts.index,
                                title="Overall Sentiment Distribution",
                                color_discrete_map=color_map
                            )
                            st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col4:
                        # Confidence scores
                        if 'Confidence' in results_df.columns:
                            fig_conf = px.bar(
                                results_df,
                                x="Aspect",
                                y="Confidence",
                                title="Confidence Scores by Aspect",
                                color_discrete_sequence=["#1f77b4"]
                            )
                            fig_conf.update_layout(xaxis_tickangle=-45)
                            st.plotly_chart(fig_conf, use_container_width=True)
                    
                    # Text insights
                    st.subheader("📝 Text Insights")
                    st.write(f"**Text Length**: {len(user_text)} characters")
                    st.write(f"**Word Count**: {len(user_text.split())} words")
                    st.write(f"**Aspects Detected**: {len(results)} aspects")
                    
                else:
                    st.warning("No aspects detected in the provided text. Try adding more descriptive content.")
                    
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")

elif analysis_type == "Batch Analysis":
    st.header("Batch Text Analysis")
    
    # Multiple text inputs
    texts = []
    num_texts = st.number_input("Number of texts to analyze:", min_value=1, max_value=10, value=3)
    
    for i in range(num_texts):
        text = st.text_area(f"Text {i+1}:", key=f"text_{i}", height=100)
        if text.strip():
            texts.append(text)
    
    if st.button("Analyze All", type="primary") and texts:
        with st.spinner(f"Analyzing {len(texts)} texts..."):
            try:
                # Analyze all texts
                batch_results = analyze_batch_texts(texts, analyzer)
                
                if not batch_results.empty:
                    st.success(f"✅ Analyzed {len(texts)} texts successfully!")
                    
                    # Display individual results
                    st.subheader("Individual Results")
                    for i, text in enumerate(texts):
                        with st.expander(f"Text {i+1} Results"):
                            text_results = batch_results[batch_results['text_id'] == i]
                            if not text_results.empty:
                                st.write(f"**Original Text**: {text[:100]}...")
                                display_df = text_results[['aspect', 'sentiment', 'score', 'confidence']].copy()
                                display_df.columns = ['Aspect', 'Sentiment', 'Score', 'Confidence']
                                st.dataframe(display_df)
                    
                    # Aggregate results
                    st.subheader("📈 Aggregate Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Average sentiment by aspect
                        avg_sentiment = batch_results.groupby('aspect')['score'].mean().reset_index()
                        avg_sentiment.columns = ['Aspect', 'Average_Score']
                        
                        fig1 = px.bar(
                            avg_sentiment, 
                            x="Aspect", 
                            y="Average_Score",
                            title="Average Sentiment Score by Aspect"
                        )
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        # Aspect frequency
                        aspect_freq = batch_results['aspect'].value_counts().reset_index()
                        aspect_freq.columns = ['Aspect', 'Frequency']
                        
                        fig2 = px.pie(
                            aspect_freq, 
                            values="Frequency", 
                            names="Aspect",
                            title="Aspect Mention Frequency"
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    # Download batch results
                    csv_batch = batch_results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Batch Results",
                        data=csv_batch,
                        file_name="batch_analysis_results.csv",
                        mime="text/csv"
                    )
                    
                else:
                    st.warning("No aspects detected in any of the provided texts.")
                    
            except Exception as e:
                st.error(f"Error during batch analysis: {str(e)}")

elif analysis_type == "File Upload":
    st.header("File Upload Analysis")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file with a 'text' column containing reviews or comments"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("📄 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            st.write(f"**Total rows**: {len(df)}")
            
            if 'text' in df.columns:
                # Sample size selection
                max_rows = min(len(df), 100)  # Limit for demo
                sample_size = st.slider(
                    "Select number of rows to analyze (for performance):",
                    min_value=1,
                    max_value=max_rows,
                    value=min(10, max_rows)
                )
                
                if st.button("Analyze File", type="primary"):
                    with st.spinner(f"Processing {sample_size} rows..."):
                        try:
                            # Sample the data
                            sample_df = df.head(sample_size)
                            texts_to_analyze = sample_df['text'].tolist()
                            
                            # Analyze the texts
                            file_results = analyze_batch_texts(texts_to_analyze, analyzer)
                            
                            if not file_results.empty:
                                st.success(f"✅ File analyzed successfully! Processed {sample_size} rows.")
                                
                                # Results overview
                                st.subheader("📊 Analysis Overview")
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Total Texts", sample_size)
                                with col2:
                                    st.metric("Aspects Found", len(file_results['aspect'].unique()))
                                with col3:
                                    avg_score = file_results['score'].mean()
                                    st.metric("Average Sentiment", f"{avg_score:.2f}")
                                
                                # Visualizations
                                st.subheader("📈 Results Visualization")
                                
                                tab1, tab2, tab3 = st.tabs(["Sentiment Timeline", "Aspect Analysis", "Raw Data"])
                                
                                with tab1:
                                    # Sentiment timeline
                                    timeline_data = file_results.groupby('text_id')['score'].mean().reset_index()
                                    timeline_data['index'] = range(len(timeline_data))
                                    
                                    fig_timeline = px.line(
                                        timeline_data,
                                        x='index',
                                        y='score',
                                        title='Sentiment Trend Across Texts',
                                        labels={'index': 'Text Index', 'score': 'Average Sentiment Score'}
                                    )
                                    st.plotly_chart(fig_timeline, use_container_width=True)
                                
                                with tab2:
                                    # Aspect analysis
                                    aspect_summary = file_results.groupby('aspect').agg({
                                        'score': ['mean', 'count'],
                                        'confidence': 'mean'
                                    }).round(3)
                                    aspect_summary.columns = ['Avg_Score', 'Count', 'Avg_Confidence']
                                    aspect_summary = aspect_summary.reset_index()
                                    
                                    st.dataframe(aspect_summary, use_container_width=True)
                                    
                                    # Aspect sentiment heatmap
                                    pivot_data = file_results.pivot_table(
                                        values='score',
                                        index='aspect',
                                        columns='sentiment',
                                        aggfunc='count',
                                        fill_value=0
                                    )
                                    
                                    if not pivot_data.empty:
                                        fig_heatmap = px.imshow(
                                            pivot_data,
                                            title="Aspect-Sentiment Distribution Heatmap",
                                            color_continuous_scale="RdYlBu"
                                        )
                                        st.plotly_chart(fig_heatmap, use_container_width=True)
                                
                                with tab3:
                                    # Raw results
                                    st.dataframe(file_results, use_container_width=True)
                                    
                                    # Download file results
                                    csv_file = file_results.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download Complete Results",
                                        data=csv_file,
                                        file_name="file_analysis_results.csv",
                                        mime="text/csv"
                                    )
                            else:
                                st.warning("No aspects detected in the uploaded file.")
                                
                        except Exception as e:
                            st.error(f"Error processing file: {str(e)}")
            else:
                st.error("❌ Please ensure your CSV file has a 'text' column.")
                st.info("💡 Your CSV should have headers and one column named 'text' containing the text to analyze.")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

# Footer with model status
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("Built with Streamlit • Aspect-Based Sentiment Analysis")
with col2:
    if analyzer_loaded:
        st.success("🤖 Model: Active")
    else:
        st.error("🤖 Model: Unavailable")
