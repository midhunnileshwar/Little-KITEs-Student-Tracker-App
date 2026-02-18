import streamlit as st
import pandas as pd
import database as db

# Page Config
st.set_page_config(page_title="Little KITEs Tracker", page_icon="🪁", layout="wide")

# Load Custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Helper for local IP
import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Sidebar Navigation
st.sidebar.title("Little KITEs Tracker 🪁")
st.sidebar.markdown(f"**Network URL:** `http://{get_ip()}:8501`")

menu = st.sidebar.radio("Navigate", ["Student Management", "Track Progress", "Generate Reports"])

if 'school_unit' not in st.session_state:
    st.session_state.school_unit = "Rajahs H.S.S Nileshwar"

def toggle_status(student_id, session, activity, current_status):
    new_status = "Done" if current_status != "Done" else "Not Done"
    # Default 3 stars if done, else 0
    stars = 3 if new_status == "Done" else 0
    db.update_progress(student_id, session, activity, new_status, stars)
    # Force reload data
    st.rerun()

def rate_skill(student_id, session, activity, stars):
    db.update_progress(student_id, session, activity, "Done", stars)
    st.rerun()

# --- Student Management ---
if menu == "Student Management":
    st.title("Student Management")
    
    tab1, tab2, tab3 = st.tabs(["View Students", "Add Student", "Import from Sheets"])
    
    with tab1:
        st.subheader(f"Students: {st.session_state.school_unit}")
        df = db.get_all_students()
        st.dataframe(df, use_container_width=True)
        st.info(f"Total Students: {len(df)}")
    
    with tab2:
        st.subheader("Add New Student")
        with st.form("add_student"):
            name = st.text_input("Name")
            adm_no = st.text_input("Admission No")
            submitted = st.form_submit_button("Add Student")
            if submitted and name and adm_no:
                if db.add_student(adm_no, name):
                    st.success(f"Added {name}")
                    st.rerun()
                else:
                    st.error("Admission Number already exists.")

    with tab3:
        st.subheader("Import from Google Sheets")
        st.markdown("Paste the Google Sheet ID (ensure it's public or shared) to import students.")
        sheet_id = st.text_input("Google Sheet ID")
        if st.button("Import"):
            st.warning("Google Sheet Import logic reserved for authenticated setup. (Placeholder)")

# --- Track Progress ---
elif menu == "Track Progress":
    st.title("Classroom Tracker")

    # Student Selection
    students_df = db.get_all_students()
    if students_df.empty:
        st.warning("No students found. Go to 'Student Management' to add some.")
    else:
        # Searchable Dropdown
        student_options = [f"{row.admission_no} - {row.name}" for row in students_df.itertuples()]
        selected_option = st.selectbox("Search Student (Type Name or ID)", student_options)
        
        if selected_option:
            selected_adm = selected_option.split(" - ")[0]
            student = students_df[students_df['admission_no'] == selected_adm].iloc[0]
            st.session_state.current_student = student
            
            # Retrieve Progress
            # We need a helper to get specific activity status quickly
            def get_status(session, activity):
                p_df = db.get_student_progress(student.id, session)
                row = p_df[p_df['activity_name'] == activity]
                if not row.empty:
                    return row.iloc[0]['status'], row.iloc[0]['stars']
                return "Not Done", 0

            st.markdown(f"### 👤 {student.name} <span style='font-size:0.8em;color:grey'>({student.admission_no})</span>", unsafe_allow_html=True)
            
            # Tabs for Sessions
            tab1, tab2, tab3 = st.tabs(["Animation", "Programming", "Robotics"])
            
            # --- Session 1: Animation ---
            with tab1:
                st.info("Time: 30 Mins | Output: exported video file")
                
                # Activity 1.3: Layers
                c1, c2 = st.columns([3, 1])
                current_status, stars = get_status("Animation", "Layers Split")
                with c1:
                    st.markdown("**Act 1.3: Layers & Columns**")
                    st.caption("Check 'Column' window. Sky/Clouds separate?")
                with c2:
                    if st.button("Layers OK" if current_status == "Done" else "Mark Layers", key="btn_1_3", type="primary" if current_status == "Done" else "secondary"):
                        toggle_status(student.id, "Animation", "Layers Split", current_status)

                st.divider()

                # Activity 1.2: Loop Logic
                c1, c2 = st.columns([3, 1])
                current_status, stars = get_status("Animation", "Loop Logic")
                with c1:
                    st.markdown("**Act 1.2: Loop Logic (Car/Clouds)**")
                    st.caption("Smooth movement? No flickering?")
                with c2:
                    # Star Rating equivalent buttons
                    cols = st.columns(3)
                    if cols[0].button("⭐ 1", key="s1_1"): rate_skill(student.id, "Animation", "Loop Logic", 1)
                    if cols[1].button("⭐ 2", key="s1_2"): rate_skill(student.id, "Animation", "Loop Logic", 2)
                    if cols[2].button("⭐ 3", key="s1_3"): rate_skill(student.id, "Animation", "Loop Logic", 3)
                    st.write(f"Current: {stars} ⭐")

                st.divider()

                # Activity 1.1: Export
                c1, c2 = st.columns([3, 1])
                current_status, stars = get_status("Animation", "Export Success")
                with c1:
                    st.markdown("**Act 1.1: Export Success**")
                    st.caption("MP4/AVI file exists on Desktop?")
                with c2:
                     if st.button("Export Verified" if current_status == "Done" else "Check Export", key="btn_1_1", type="primary" if current_status == "Done" else "secondary"):
                        toggle_status(student.id, "Animation", "Export Success", current_status)

            # --- Session 2: Programming ---
            with tab2:
                st.info("Time: 30 Mins | Check: Green Flag Run")
                
                # Act 2.1 Arrow Logic
                c1, c2 = st.columns([3, 1])
                current_status, stars = get_status("Programming", "Arrow Logic")
                with c1:
                    st.markdown("**Act 2.1: Arrow Keys (X/Y)**")
                    st.caption("Up/Down (Y), Left/Right (X) correct?")
                with c2:
                     if st.button("Logic OK" if current_status == "Done" else "Check Logic", key="btn_2_1", type="primary" if current_status == "Done" else "secondary"):
                        toggle_status(student.id, "Programming", "Arrow Logic", current_status)
                
                st.divider()

                # Act 2.2 Mouse Follow
                c1, c2 = st.columns([3, 1])
                current_status, stars = get_status("Programming", "Mouse Follow")
                with c1:
                    st.markdown("**Act 2.2: Mouse Follow**")
                    st.caption("Sprite sticks to cursor? No lag?")
                with c2:
                     if st.button("Follow OK" if current_status == "Done" else "Check Follow", key="btn_2_2", type="primary" if current_status == "Done" else "secondary"):
                        toggle_status(student.id, "Programming", "Mouse Follow", current_status)
                
                st.divider()
                
                # Debugging Skill
                c1, c2 = st.columns([3, 1])
                current_status, stars = get_status("Programming", "Debugging")
                with c1:
                    st.markdown("**Bonus: Debugging Skill**")
                    st.caption("Fixed off-screen sprite or other bug?")
                with c2:
                     if st.button("Debugged" if current_status == "Done" else "Mark Bonus", key="btn_2_3", type="primary" if current_status == "Done" else "secondary"):
                        toggle_status(student.id, "Programming", "Debugging", current_status)

            # --- Session 3: Robotics ---
            with tab3:
                 st.info("Time: 1 Hour | Critical: Hardware Safety")
                 
                 # Act 3.1 Resistor Safety
                 c1, c2 = st.columns([3, 1])
                 current_status, stars = get_status("Robotics", "Resistor Safety")
                 with c1:
                    st.markdown("### ⚠️ SAFETY CHECK")
                    st.caption("**Act 3.1: Resistor Present? Long leg to Pin?**")
                 with c2:
                    # Red button logic
                    if current_status == "Done":
                        btn_label = "✅ SAFE"
                        btn_type = "primary"
                    else:
                        btn_label = "⚠️ HAZARD CHECK"
                        btn_type = "secondary" # We'll need CSS to make this RED if possible, or just rely on label
                    
                    if st.button(btn_label, key="btn_3_1", type=btn_type):
                        toggle_status(student.id, "Robotics", "Resistor Safety", current_status)
                 
                 if current_status != "Done":
                     st.error("DO NOT ALLOW USB CONNECTION YET!")
                 else:
                     st.success("Approved for USB Connection.")

                 st.divider()

                 # Act 3.2 Upload Mode
                 c1, c2 = st.columns([3, 1])
                 current_status, stars = get_status("Robotics", "Upload Mode")
                 with c1:
                    st.markdown("**Act 3.2: Upload Mode**")
                    st.caption("Student is in 'Upload Mode' (not Stage)?")
                 with c2:
                     if st.button("Mode OK" if current_status == "Done" else "Check Mode", key="btn_3_2", type="primary" if current_status == "Done" else "secondary"):
                        toggle_status(student.id, "Robotics", "Upload Mode", current_status)

                 st.divider()

                 # Act 3.3 Servo
                 c1, c2 = st.columns([3, 1])
                 current_status, stars = get_status("Robotics", "Servo Test")
                 with c1:
                    st.markdown("**Act 3.3: Servo 180°**")
                    st.caption("Accurate 0-180 sweep?")
                 with c2:
                     if st.button("Servo OK" if current_status == "Done" else "Check Servo", key="btn_3_3", type="primary" if current_status == "Done" else "secondary"):
                        toggle_status(student.id, "Robotics", "Servo Test", current_status)

elif menu == "Generate Reports":
    st.title("Student Reports")
    
    import pdf_generator as pdf_gen
    
    students_df = db.get_all_students()
    
    if students_df.empty:
        st.warning("No students available. Add students first.")
    else:
        student_options = [f"{row.admission_no} - {row.name}" for row in students_df.itertuples()]
        selected_option = st.selectbox("Select Student for Report", student_options)
        
        if selected_option:
            selected_adm = selected_option.split(" - ")[0]
            student = students_df[students_df['admission_no'] == selected_adm].iloc[0]
            
            if st.button("Generate PDF Report"):
                report_path = pdf_gen.generate_report(student.id)
                st.success(f"Report generated: {report_path}")
                
                with open(report_path, "rb") as f:
                    pdf_bytes = f.read()
                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name=report_path.split("/")[-1],
                        mime="application/pdf"
                    )

