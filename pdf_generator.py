from fpdf import FPDF
import database as db
import os

class PDF(FPDF):
    def header(self):
        # Logo could go here
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Little KITEs Special Training - Performance Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def get_skill_description(activity):
    mapping = {
        "Layers Split": "Proficient in OpenToonz layer management and scene composition.",
        "Loop Logic": "Demonstrated understanding of animation loops and frame timing.",
        "Export Success": "Mastered OpenToonz export settings and video rendering.",
        "Arrow Logic": "Implemented coordinate-based sprite movement (X/Y axis logic) in Scratch.",
        "Mouse Follow": "Created interactive event loops and mouse-tracking logic.",
        "Debugging": "Demonstrated logical thinking by identifying and fixing code bugs independently.",
        "Resistor Safety": "Safely constructed LED circuits with proper resistor placement.",
        "Upload Mode": "Successfully compiled and uploaded code to Arduino hardware.",
        "Servo Test": "Programmed servo motors for precise angular control."
    }
    return mapping.get(activity, f"Completed activity: {activity}")

def generate_report(student_id):
    # Fetch Student Data
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT name, admission_no, school_unit FROM students WHERE id = ?", (student_id,))
    student = c.fetchone()
    conn.close()
    
    if not student:
        return None
        
    name, adm_no, school = student
    
    # Fetch Progress
    # We want all sessions
    sessions = ["Animation", "Programming", "Robotics"]
    
    pdf = PDF()
    pdf.add_page()
    
    # Student Details
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Name: {name}", 0, 1)
    pdf.cell(0, 10, f"Admission No: {adm_no}", 0, 1)
    pdf.cell(0, 10, f"School Unit: {school}", 0, 1)
    pdf.line(10, 55, 200, 55)
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Skills Acquired", 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    
    skills_count = 0
    total_stars = 0
    
    for session in sessions:
        p_df = db.get_student_progress(student_id, session)
        # Filter for Done
        done_activities = p_df[p_df['status'] == 'Done']
        
        if not done_activities.empty:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, session, 0, 1)
            pdf.set_font('Arial', '', 11)
            for _, row in done_activities.iterrows():
                skill = get_skill_description(row['activity_name'])
                stars = int(row['stars'])
                total_stars += stars
                
                star_str = "⭐" * stars if stars else ""
                pdf.cell(10) # Indent
                pdf.multi_cell(0, 8, f"- {skill} {star_str}")
                skills_count += 1
            pdf.ln(3)

    if skills_count == 0:
        pdf.cell(0, 10, "No completed activities recorded.", 0, 1)

    pdf.ln(20)
    
    # Trainer Signature
    pdf.line(10, pdf.get_y(), 80, pdf.get_y())
    pdf.cell(0, 10, "Trainer Signature", 0, 1)
    
    # Teacher Comments (Placeholder for now)
    # pdf.multi_cell(0, 10, "Teacher's Comment: Excellent performance in robotics.")
    
    filename = f"report_{adm_no}_{name.replace(' ', '_')}.pdf"
    output_path = f"reports/{filename}"
    
    if not os.path.exists("reports"):
        os.makedirs("reports")
        
    pdf.output(output_path)
    return output_path
