import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Fellowship Notes Viewer", layout="wide")

# Navigation
page = st.sidebar.selectbox("Choose a page", ["Standup Notes", "Retrospectives"])

if page == "Standup Notes":
    st.title("Fellow Standup Notes Viewer")
    
    uploaded_file = st.file_uploader("Upload your standup notes CSV file", type=["csv"], key="standup_file")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Ensure column names are trimmed and consistent
        df.columns = df.columns.str.strip()
        
        # Sort by Date so navigation makes sense
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.sort_values(by='Date').reset_index(drop=True)
        
        # Create a session state index to track current fellow
        if 'current_index_standup' not in st.session_state:
            st.session_state.current_index_standup = 0
        
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
                st.markdown(f"{achievements}")
            else:
                st.info("No achievements recorded")
            
            st.markdown("")  # Add spacing
            
            # Blockers Section
            st.markdown("### 🚧 **Current Blockers**")
            blockers = get_column_value(fellow, ['What blockers are you currently encountering?', 'Blockers', 'Current blockers'])
            if blockers != "N/A":
                st.markdown(f"{blockers}")
            else:
                st.success("No blockers - smooth sailing!")
            
            st.markdown("")  # Add spacing
            
            # Priorities Section
            st.markdown("### 🎯 **Priorities**")
            priorities = get_column_value(fellow, [
                'What are your priorities youll contribute to until the next stand up?',
                'What are your priorities you\'ll contribute to until the next stand up?',
                'Priorities',
                'Next priorities'
            ])
            if priorities != "N/A":
                st.markdown(f"{priorities}")
            else:
                st.warning("No priorities set")
            
            st.markdown("")  # Add spacing
            
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
                    st.markdown(f"{progress}")
                else:
                    st.info("No progress update")
            
            with col_shouts:
                st.markdown("### 👏 **Shoutouts**")
                shoutouts = get_column_value(fellow, ['Shoutouts', 'Shout-outs'])
                if shoutouts != "N/A":
                    st.markdown(f"{shoutouts}")
                else:
                    st.info("No shoutouts")
                
        col1, col2, col3 = st.columns([1,6,1])
        
        with col1:
            if st.button("⬅️", key="standup_prev"):
                if st.session_state.current_index_standup > 0:
                    st.session_state.current_index_standup -= 1
        
        with col3:
            if st.button("➡️", key="standup_next"):
                if st.session_state.current_index_standup < total_fellows - 1:
                    st.session_state.current_index_standup += 1
        
        show_fellow(st.session_state.current_index_standup)
    else:
        st.info("Please upload a CSV file to begin.")

elif page == "Retrospectives":
    st.title("Fellow Retrospectives Viewer")
    
    uploaded_file = st.file_uploader("Upload your retrospectives CSV file", type=["csv"], key="retro_file")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Ensure column names are trimmed and consistent
        df.columns = df.columns.str.strip()
        
        # Sort by Date so navigation makes sense
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.sort_values(by='Date').reset_index(drop=True)
        
        # Create a session state index to track current fellow
        if 'current_index_retro' not in st.session_state:
            st.session_state.current_index_retro = 0
        
        total_fellows = len(df)
        
        # Helper function to safely get column values
        def get_column_value_retro(fellow, possible_names):
            for name in possible_names:
                if name in df.columns:
                    value = fellow[name]
                    if pd.isna(value):
                        return "N/A"
                    return str(value)
            return "N/A"
        
        def show_fellow_retro(idx):
            fellow = df.iloc[idx]
            st.subheader(f"Fellow {idx + 1} of {total_fellows}: {get_column_value_retro(fellow, ['User full name', 'Full name', 'Name'])}")
            st.markdown(f"**Group:** {get_column_value_retro(fellow, ['Groups', 'Group'])}")
            
            # Handle date display
            date_value = get_column_value_retro(fellow, ['Date', 'Timestamp'])
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
            st.markdown("### 🏆 **What did you achieve this week?**")
            achievements = get_column_value_retro(fellow, ['What did you achieve this week?', 'Achievements'])
            if achievements != "N/A":
                st.markdown(f"{achievements}")
            else:
                st.info("No achievements recorded")
            
            st.markdown("")  # Add spacing
            
            # What went well Section
            st.markdown("### ✅ **What went well this week?**")
            went_well = get_column_value_retro(fellow, ['What went well this week past week?', 'What went well this week?', 'Went well'])
            if went_well != "N/A":
                st.markdown(f"{went_well}")
            else:
                st.info("No highlights recorded")
            
            st.markdown("")  # Add spacing
            
            # What could've gone better Section
            st.markdown("### 🔄 **What could've gone better?**")
            could_improve = get_column_value_retro(fellow, ['What could\'ve gone better this past week?', 'What could have gone better?', 'Improvements'])
            if could_improve != "N/A":
                st.markdown(f"{could_improve}")
            else:
                st.success("Everything went smoothly!")
            
            st.markdown("")  # Add spacing
            
            # Two-column layout for Learning and Puzzles
            col_learning, col_puzzles = st.columns(2)
            
            with col_learning:
                st.markdown("### 📚 **What have you learned?**")
                learning = get_column_value_retro(fellow, ['What have you learned this week?', 'Learning', 'Learnings'])
                if learning != "N/A":
                    st.markdown(f"{learning}")
                else:
                    st.info("No learning notes")
            
            with col_puzzles:
                st.markdown("### 🤔 **What still puzzles you?**")
                puzzles = get_column_value_retro(fellow, ['What still puzzles you?', 'Puzzles', 'Questions'])
                if puzzles != "N/A":
                    st.markdown(f"{puzzles}")
                else:
                    st.success("No puzzles - all clear!")
                
        col1, col2, col3 = st.columns([1,6,1])
        
        with col1:
            if st.button("⬅️", key="retro_prev"):
                if st.session_state.current_index_retro > 0:
                    st.session_state.current_index_retro -= 1
        
        with col3:
            if st.button("➡️", key="retro_next"):
                if st.session_state.current_index_retro < total_fellows - 1:
                    st.session_state.current_index_retro += 1
        
        show_fellow_retro(st.session_state.current_index_retro)
    else:
        st.info("Please upload a retrospectives CSV file to begin.")
