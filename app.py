import streamlit as st
import pandas as pd

st.title("Fellow Standup Notes Viewer")

uploaded_file = st.file_uploader("Upload your standup notes CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)


    # Ensure column names are trimmed and consistent
    df.columns = df.columns.str.strip()

    # Sort by Date so navigation makes sense
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.sort_values(by='Date').reset_index(drop=True)

    # Create a session state index to track current fellow
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    total_fellows = len(df)

    # Helper function to safely get column values
    def get_column_value(fellow, possible_names):
        for name in possible_names:
            if name in df.columns:
                value = fellow[name]
                if pd.isna(value):
                    return "N/A"
                return str(value)
        return "N/A"

    def show_fellow(idx):
        fellow = df.iloc[idx]
        st.subheader(f"Fellow {idx + 1} of {total_fellows}: {get_column_value(fellow, ['User full name', 'Full name', 'Name'])}")
        st.markdown(f"**Group:** {get_column_value(fellow, ['Groups', 'Group'])}")
        
        # Handle date display
        date_value = get_column_value(fellow, ['Date', 'Timestamp'])
        if date_value != "N/A" and pd.notnull(date_value):
            try:
                formatted_date = date_value.strftime('%A, %d %B %Y, %I:%M %p')
                st.markdown(f"**Date:** {formatted_date}")
            except:
                st.markdown(f"**Date:** {date_value}")
        else:
            st.markdown(f"**Date:** {date_value}")
            
        st.markdown("---")
        
        # Achievements Section
        st.markdown("### 🎉 **Achievements**")
        achievements = get_column_value(fellow, ['What have you achieved since the last stand up?', 'Achievements'])
        if achievements != "N/A":
            st.markdown(f"> {achievements}")
        else:
            st.info("No achievements recorded")
        
        st.markdown("")  
        
        # Blockers Section
        st.markdown("### 🚧 **Current Blockers**")
        blockers = get_column_value(fellow, ['What blockers are you currently encountering?', 'Blockers', 'Current blockers'])
        if blockers != "N/A":
            st.markdown(f"> {blockers}")
        else:
            st.success("No blockers!")
        
        st.markdown("")  
        
        # Priorities Section
        st.markdown("### 🎯 **Priorities**")
        priorities = get_column_value(fellow, [
            'What are your priorities youll contribute to until the next stand up?',
            'What are your priorities you\'ll contribute to until the next stand up?',
            'Priorities',
            'Next priorities'
        ])
        if priorities != "N/A":
            st.markdown(f"> {priorities}")
        else:
            st.warning("No priorities set")
        
        st.markdown("") 
        
        # Two-column layout for Progress and Shoutouts
        col_progress, col_shouts = st.columns(2)
        
        with col_progress:
            st.markdown("### 📈 **Progress**")
            progress = get_column_value(fellow, [
                'Since the last stand up, Ive made progress relating to my project/curriculum?',
                'Since the last stand up, I\'ve made progress relating to my project/curriculum?',
                'Progress'
            ])
            if progress != "N/A":
                st.markdown(f"> {progress}")
            else:
                st.info("No progress update")
        
        with col_shouts:
            st.markdown("### 👏 **Shoutouts**")
            shoutouts = get_column_value(fellow, ['Shoutouts', 'Shout-outs'])
            if shoutouts != "N/A":
                st.markdown(f"> {shoutouts}")
            else:
                st.info("No shoutouts")
            
    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        if st.button("⬅️"):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1

    with col3:
        if st.button("➡️"):
            if st.session_state.current_index < total_fellows - 1:
                st.session_state.current_index += 1

    show_fellow(st.session_state.current_index)
else:
    st.info("Please upload a CSV file to begin.")
