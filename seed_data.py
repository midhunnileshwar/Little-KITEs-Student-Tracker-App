import sqlite3
import pandas as pd

# Data for Rajahs H.S.S Nileshwar
rajahs_data = """
1,ABDUL WAJID PALAKKI,38266
2,ABHINAV K T,38272
3,ADHISH A,36274
4,ADIL,39017
5,AGNEY VINOD K,36287
6,AHAMMED RIFAI .M,36718
7,AMEYA K,36399
8,AMEYA SHAJI,38632
9,AMEYA VINOD,37045
10,AMINATH SHAHANA.B,36383
11,ANANTH KRISHNAN K,36228
12,ANVITHA P,38460
13,ASWAJITH P P,37139
14,AYANA SHAIVI,37035
15,AYISHATH FAZMIYA C K,36423
16,AYSHA SIDDIQUE.C,36220
17,DEVANANDHA T,38540
18,DIYA T,38466
19,FATHIMATH SHAMNA T K,36562
20,GAUTHAM S BABU,36237
21,HIRANMAYI K,36480
22,JISHNU. M,36290
23,KARTHIK K P,39133
24,KHADEEJATHUL KUBRA. P,38459
25,KRISHNENDU S,38457
26,MEHRAN MANSOOR,37942
27,MOHAMMED AJAS FADI,36536
28,MUHAMMED AMEEN M,38146
29,MUHAMMED ANFAS .K,36446
30,MUHAMMED SINAN K,36557
31,NANDHAKISHORE K P,36261
32,NIHAL SUBRAMANIAN,36602
33,OMHARI P V,39183
34,RIFA. K.K,36379
35,ROHAN T P,38362
36,SAHALA.K,38568
37,SHAHRUL SHAN,36414
38,SHIVAJITH .H.G,36222
39,SIDHARTH.K,38377
40,SOUPARNIKA K,36589
41,SREE NANDA.M,36253
42,THANUSHA.K,36271
43,VAIGA S,38427
"""

# Data for G V H S S KOTTAPURAM
kottapuram_data = """
1,AYISHA.P.P,6407
2,AYSHATHUL LUBNA. E.K,6551
3,FATHIMA ABNA.P.P,6279
4,FATHIMA HIBA.P,6510
5,FATHIMA.,6543
6,FATHIMA.E.K,6300
7,FATHIMATH AFLA .A,6514
8,FATHIMATH RAZVANA. A.P,6517
9,HASEENA K M,6425
10,MOHAMMED ARIF. C,6505
11,MOHAMMED K N,6506
12,MOHAMMED NISHAN,6503
13,MUHAMED MUFEED MUSTHAFA T,6523
14,MUHAMMAD IMTHIYAZ . A,6327
15,MUHAMMED NABEER.P,6564
16,MUHAMMED SHIFAS,6513
17,MUHAMMED SINAN,6292
18,NAJA FATHIMA C K,6667
19,NAJA FATHIMA E K,6268
20,SAFA.P.M.H,6518
21,ZAINABA.P,6562
"""

CONTRIBUTING_SCHOOLS = [
    {"name": "Rajahs H.S.S Nileshwar", "data": rajahs_data},
    {"name": "G V H S S KOTTAPURAM", "data": kottapuram_data}
]

def seed_database(db_path="students.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create Tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            admission_no TEXT UNIQUE,
            name TEXT,
            school_unit TEXT DEFAULT 'Rajahs H.S.S Nileshwar'
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            student_id INTEGER,
            session_name TEXT,
            activity_name TEXT,
            status TEXT DEFAULT 'Not Done',
            stars INTEGER DEFAULT 0,
            PRIMARY KEY (student_id, session_name, activity_name),
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    # Process Raw Data for each school
    for school in CONTRIBUTING_SCHOOLS:
        school_name = school["name"]
        raw_cvs_data = school["data"]
        
        print(f"Seeding data for {school_name}...")
        lines = raw_cvs_data.strip().split('\n')
        for line in lines:
            parts = line.split(',')
            if len(parts) >= 3:
                # Format: Sl No, Name, Admission No
                sl_no = parts[0].strip()
                name = parts[1].strip()
                adm_no = parts[2].strip()
                
                try:
                    # Check if student exists to avoid overwriting school_unit on existing ones if we just want to insert new
                    # But if we want to ensure school_unit is correct, we might want to update it.
                    # For now, let's use INSERT OR IGNORE and assume unique admission_no
                    # However, we need to insert school_unit now. 
                    
                    # We can use INSERT OR REPLACE if we want to update details, but that might wipe other fields if they existed.
                    # Let's stick to INSERT OR IGNORE but include school_unit.
                    
                    c.execute("INSERT OR IGNORE INTO students (admission_no, name, school_unit) VALUES (?, ?, ?)", (adm_no, name, school_name))
                    
                    # If we want to update the school_unit for existing students (in case of data correction), we could do:
                    # c.execute("UPDATE students SET school_unit = ? WHERE admission_no = ?", (school_name, adm_no))
                    
                except sqlite3.IntegrityError:
                    pass
                
    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()
