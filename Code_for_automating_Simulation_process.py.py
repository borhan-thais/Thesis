from pyaedt import Hfss
import pandas as pd
import os
import sqlite3
from datetime import datetime
import random

base_box_size = [15, 15, 2]
base_box2_size = [15, 15, 15]
base_box3_size = [15, 15, 0.035]
# Base substance size
base_substance_size = [13, 13]

# Base rectangle size
base_rectangle1_size = [11, 1.5]
base_rectangle2_size = [11, 2]
base_rectangle3_size = [1.5, 2.5]
base_rectangle4_size = [3.5, 2.5]
base_rectangle5_size = [2.5, 7]


# Base substance positions
base_substance_origin = [1, 1, base_box_size[2]]

# Base rectangle positions
base_rectangle1_origin = [2 ,2 , base_box_size[2]]
base_rectangle2_origin = [2 ,11.5, base_box_size[2]]
base_rectangle3_origin = [2 ,4.5, base_box_size[2]]
base_rectangle4_origin = [2 ,8, base_box_size[2]]
base_rectangle5_origin = [11.5 ,4.5, base_box_size[2]]




# Create database connection
def create_database():
    conn = sqlite3.connect('E:\\Paper\\Thesis\\meta\\simulation_results.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS simulation_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        design_number INTEGER,
        box_size_x REAL, box_size_y REAL, box_size_z REAL,
        box2_size_x REAL, box2_size_y REAL, box2_size_z REAL,
        box3_size_x REAL, box3_size_y REAL, box3_size_z REAL,
        box_size_xp REAL, box_size_yp REAL, box_size_zp REAL,
        box2_size_xp REAL, box2_size_yp REAL, box2_size_zp REAL,
        box3_size_xp REAL, box3_size_yp REAL, box3_size_zp REAL,
        s_x REAL, s_y REAL,
        s_xp REAL, s_yp REAL, s_zp REAL,
        r1_x REAL, r1_y REAL,
        r1_xp REAL, r1_yp REAL, r1_zp REAL,
        r2_x REAL, r2_y REAL,
        r2_xp REAL, r2_yp REAL, r2_zp REAL,
        r3_x REAL, r3_y REAL,
        r3_xp REAL, r3_yp REAL, r3_zp REAL,
        r4_x REAL, r4_y REAL,
        r4_xp REAL, r4_yp REAL, r4_zp REAL,
        r5_x REAL, r5_y REAL,
        r5_xp REAL, r5_yp REAL, r5_zp REAL,
        freq_s11 REAL,
        min_s11 REAL,
        freq_s21 REAL,
        min_s21 REAL
    )
    ''')
    
    conn.commit()
    return conn

def save_to_database(conn, design_num, box_size, box2_size, box3_size, substance_size, substance_origin, rectangles_data, min_s11, freq_s11, min_s21, freq_s21):
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO simulation_results (
        design_number, 
        box_size_x, box_size_y, box_size_z,
        box2_size_x, box2_size_y, box2_size_z,
        box3_size_x, box3_size_y, box3_size_z,
        box_size_xp, box_size_yp, box_size_zp,
        box2_size_xp, box2_size_yp, box2_size_zp,
        box3_size_xp, box3_size_yp, box3_size_zp,
        s_x, s_y, s_xp, s_yp, s_zp,
        r1_x, r1_y, r1_xp, r1_yp, r1_zp,
        r2_x, r2_y, r2_xp, r2_yp, r2_zp,
        r3_x, r3_y, r3_xp, r3_yp, r3_zp,
        r4_x, r4_y, r4_xp, r4_yp, r4_zp,
        r5_x, r5_y, r5_xp, r5_yp, r5_zp,
        freq_s11, min_s11, freq_s21, min_s21
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        design_num,
        box_size[0], box_size[1], box_size[2],
        box2_size[0], box2_size[1], box2_size[2],
        box3_size[0], box3_size[1], box3_size[2],
        0, 0, 0,
        0, 0,-6.5,
        0, 0, 0,
        substance_size[0], substance_size[1], substance_origin[0], substance_origin[1], substance_origin[2],
        rectangles_data['rect1']['size'][0], rectangles_data['rect1']['size'][1], rectangles_data['rect1']['origin'][0], rectangles_data['rect1']['origin'][1], rectangles_data['rect1']['origin'][2],
        rectangles_data['rect2']['size'][0], rectangles_data['rect2']['size'][1], rectangles_data['rect2']['origin'][0], rectangles_data['rect2']['origin'][1], rectangles_data['rect2']['origin'][2],
        rectangles_data['rect3']['size'][0], rectangles_data['rect3']['size'][1], rectangles_data['rect3']['origin'][0], rectangles_data['rect3']['origin'][1], rectangles_data['rect3']['origin'][2],
        rectangles_data['rect4']['size'][0], rectangles_data['rect4']['size'][1], rectangles_data['rect4']['origin'][0], rectangles_data['rect4']['origin'][1], rectangles_data['rect4']['origin'][2],
        rectangles_data['rect5']['size'][0], rectangles_data['rect5']['size'][1], rectangles_data['rect5']['origin'][0], rectangles_data['rect5']['origin'][1], rectangles_data['rect5']['origin'][2],
        freq_s11, min_s11, freq_s21, min_s21    
        ))
    
    conn.commit()

def run_hfss_simulation(design_number, 
                       box_size=[18, 20, 2], 
                       box2_size=[18, 20, 15],
                       box3_size=[18, 20, 0.035],
                       substance_size=[16, 18], 
                       substance_origin=[0.9, 1.3, 2],
                       rectangles_data=None,
                       save_path="E:\Paper\Thesis\meta\Designs and csv",
                       conn=None):
    
    # Default rectangles data if not provided
    if rectangles_data is None:
        rectangles_data = {
            'rect1': {'size': [8.5, 1.2], 'origin': [2.7, 3.2, box_size[2]]},
            'rect2': {'size': [8.5, 2.2], 'origin': [2.7, 14, box_size[2]]},
            'rect3': {'size': [2.2, 2.2], 'origin': [3.7, 5.25, box_size[2]]},
            'rect4': {'size': [3.2, 2.2], 'origin': [3.7, 10.5, box_size[2]]},
            'rect5': {'size': [3.2, 4], 'origin': [11, 6, box_size[2]]},
            
        }
    
    # Create a new HFSS instance
    hfss = Hfss(
        project=f"Project_{design_number}",
        design=f"Design_{design_number}",
        specified_version="2025.2",
        student_version=True,
        new_desktop=True
    )

    # Create a box
    box = hfss.modeler.create_box(
        [0, 0, 0],
        box_size,
        name="Box1",
        material="FR4_epoxy"
    )

    # Create substance rectangle
    substance = hfss.modeler.create_rectangle(
        orientation=hfss.PLANE.XY,
        origin=substance_origin,
        sizes=substance_size,
        name="Substance",
        material="vacuum"
    )

    # Create rectangles
    rectangles = {}
    for i, (key, data) in enumerate(rectangles_data.items(), 1):
        rectangles[key] = hfss.modeler.create_rectangle(
            orientation=hfss.PLANE.XY,
            origin=data['origin'],
            sizes=data['size'],
            name=f"Rectangle{i}",
            material="vacuum"
        )

    # Assign perfect E to all sheets
    sheet_names = [substance.name] + [rect.name for rect in rectangles.values()]
    hfss.assign_perfecte_to_sheets(sheet_names, "PerfectEFromSheet")

    # Create air box
    box2 = hfss.modeler.create_box(
        [0, 0, -6.5],
        box2_size,
        name="Box2",
        material="air"
    )
    # Create a thin box for the top
    box3 = hfss.modeler.create_box(
        [0, 0, 0],
        box3_size,
        name="Box3",
        material="copper"
    )
    # Get faces for boundary conditions
    ids = [face.id for face in hfss.modeler["Box2"].faces]

    # Assign boundaries
    hfss.assign_perfecte_to_sheets(ids[1], f"PerfectE1_{design_number}")
    hfss.assign_perfecte_to_sheets(ids[3], f"PerfectE2_{design_number}")
    hfss.assign_perfecth_to_sheets(ids[0], f"PerfectH1_{design_number}")
    hfss.assign_perfecth_to_sheets(ids[4], f"PerfectH2_{design_number}")

    hfss.solution_type = "Modal"
    
    # Assign wave ports
    hfss.wave_port(
        assignment=ids[5],
        integration_line=[[box_size[0], 0, box_size[2]], [box_size[0], box_size[1], box_size[2]]],
        name=f"WavePort1_{design_number}",
        renormalize=False
    )

    hfss.wave_port(
        assignment=ids[2],
        integration_line=[[0, 0, box_size[2]], [0, box_size[1], box_size[2]]],
        name=f"WavePort2_{design_number}",
        renormalize=False
    )

    # Create Analysis Setup
    setup_name = f"Setup_{design_number}"
    setup = hfss.create_setup(setup_name)
    setup.props["Frequency"] = "28GHz"
    setup.props["MaxDeltaS"] = 0.02
    setup.props["MaximumPasses"] = 20
    setup.props["MinimumPasses"] = 1
    setup.props["MinimumConvergedPasses"] = 1
    setup.props["PercentRefinement"] = 30
    setup.props["BasisOrder"] = 1
    setup.props["DoLambdaRefine"] = True
    setup.props["DoMaterialLambda"] = True
    setup.props["DrivenSolverType"] = "Direct Solver"
    setup.props["SaveAnyFields"] = True
    setup.props["IESolverType"] = "Auto"
    setup.update()

    # Add frequency sweep
    sweep_name = f"sweep_{design_number}"
    sweep = setup.add_sweep(sweep_name)
    sweep.props["RangeType"] = "LinearStep"
    sweep.props["RangeStart"] = "1GHz"
    sweep.props["RangeEnd"] = "20GHz"
    sweep.props["RangeStep"] = "0.001GHz"
    sweep.props["Type"] = "Interpolating"
    sweep.props["InterpTolerance"] = 0.5
    sweep.props["InterpMaxSolns"] = 250
    sweep.props["InterpUseS"] = True
    sweep.props["EnforcePassivity"] = True
    sweep.update()

    # Save the project
    project_path = f"{save_path}\\Project_{design_number}.aedt"
    hfss.save_project(project_path)

    # Analyze the setup
    hfss.analyze_setup(setup_name)

    # Generate reports
    hfss.post.create_report(
        expressions=["dB(S(1,1))", "dB(S(2,1))"],
        domain="Sweep",
        primary_sweep_variable="Freq",
        report_category="Modal Solution Data",
        plot_type="Rectangular Plot",
        plot_name=f"S Parameter Plot {design_number}",
    )

    hfss.post.create_report(
        expressions=["dB(S(1,1))", "ang_rad(S(1,1))"],
        domain="Sweep",
        primary_sweep_variable="Freq",
        report_category="Modal Solution Data",
        plot_type="Data Table",
        plot_name=f"S Parameter Table 1 (p-{design_number})",
    )

    hfss.post.create_report(
        expressions=["dB(S(2,1))", "ang_rad(S(2,1))"],
        domain="Sweep",
        primary_sweep_variable="Freq",
        report_category="Modal Solution Data",
        plot_type="Data Table",
        plot_name=f"S Parameter Table 2 (p-{design_number})",
    )

    # Export reports
    csv_file_1 = f"{save_path}\\S Parameter Table 1 (p-{design_number}).csv"
    csv_file_2 = f"{save_path}\\S Parameter Table 2 (p-{design_number}).csv"
    
    hfss.post.export_report_to_file(save_path, f"S Parameter Table 1 (p-{design_number})", ".csv")
    hfss.post.export_report_to_file(save_path, f"S Parameter Table 2 (p-{design_number})", ".csv")

    # Process results
    results = {'Design': design_number}
    
    # Read S11 data
    try:
        if os.path.exists(csv_file_1):
            df = pd.read_csv(csv_file_1)
            mag_s11_col = None
            freq_col = None
            
            for col in df.columns:
                if 'dB(S(1,1)) []' in col or 'dB(S(WavePort1,WavePort1))' in col:
                    mag_s11_col = col
                if 'Freq [GHz]' in col:
                    freq_col = col
            
            if mag_s11_col and freq_col:
                min_idx = df[mag_s11_col].idxmin()
                min_value = df.loc[min_idx, mag_s11_col]
                corresponding_freq = df.loc[min_idx, freq_col]
                
                results.update({
                    'Min_mag_S11': min_value,
                    'Corresponding_Freq_GHz_S11': corresponding_freq,
                    'CSV_File_S11': csv_file_1
                })
                
                print(f"Design {design_number}: Minimum mag(S(1,1)) = {min_value:.6f} at Frequency = {corresponding_freq:.3f} GHz")
            else:
                print(f"Design {design_number}: Could not find required columns in CSV file 1")
    except Exception as e:
        print(f"Design {design_number}: Error reading CSV file 1: {str(e)}")

    # Read S21 data
    try:
        if os.path.exists(csv_file_2):
            df2 = pd.read_csv(csv_file_2)
            mag_s21_col = None
            freq_col2 = None
            
            for col in df2.columns:
                if 'dB(S(2,1)) []' in col or 'dB(S(WavePort2,WavePort1))' in col:
                    mag_s21_col = col
                if 'Freq [GHz]' in col:
                    freq_col2 = col
            
            if mag_s21_col and freq_col2:
                min_idx2 = df2[mag_s21_col].idxmin()
                min_value2 = df2.loc[min_idx2, mag_s21_col]
                corresponding_freq2 = df2.loc[min_idx2, freq_col2]
                
                results.update({
                    'Min_mag_S21': min_value2,
                    'Corresponding_Freq_GHz_S21': corresponding_freq2,
                    'CSV_File_S21': csv_file_2
                })
                
                print(f"Design {design_number}: Minimum mag(S(2,1)) = {min_value2:.6f} at Frequency = {corresponding_freq2:.3f} GHz")
            else:
                print(f"Design {design_number}: Could not find required columns in CSV file 2")
    except Exception as e:
        print(f"Design {design_number}: Error reading CSV file 2: {str(e)}")

    # Save to database if connection provided
    if conn and 'Min_mag_S11' in results and 'Min_mag_S21' in results:
        save_to_database(conn, design_number,
                        box_size, box2_size, box3_size,
                        substance_size, substance_origin, rectangles_data, 
                        results['Min_mag_S11'], results['Corresponding_Freq_GHz_S11'], 
                        results['Min_mag_S21'], results['Corresponding_Freq_GHz_S21'])

    # Release resources
    # hfss.release_desktop()
    
    return results

if __name__ == "__main__":
    # Create database connection (once)
    conn = create_database()
    
    # Store all results
    all_results = []
    
    # Run 100 iterations with random rect1 and rect3 sizes
    print("Starting 100 HFSS simulations with random rect1 and rect3 sizes...")
    print("=" * 80)
    
    for i in range(645, 655):  # Design numbers 1 to 100
        print(f"Running Design {i}/100...")
        
        # Generate random sizes for rect1 and rect3
        # rect1: random size between [8-13, 1-2.5]
        rect1_x = random.uniform(9.0, 11.0)
        rect1_y = random.uniform(1.3, 2.0)
        
        # rect3: random size between [1-3, 2-4]
        rect3_x = random.uniform(2.2, 3.5)
        rect3_y = random.uniform(2.3, 3.0)
        
        # Create custom rectangles with random rect1 and rect3 sizes
        custom_rectangles = {
            'rect1': {'size': [rect1_x, rect1_y], 'origin': [3.7 ,3.2 ,2]},
            'rect2': {'size': base_rectangle2_size, 'origin': [3.7 ,14 ,2]},  # Keep original
            'rect3': {'size': [rect3_x, rect3_y], 'origin': [4.7 , 6.25 , 2]},
            'rect4': {'size': base_rectangle4_size, 'origin': [4.7 ,10.5 ,2]},  # Keep original
            'rect5': {'size': base_rectangle5_size, 'origin': [12 ,6 ,2]}   # Keep original
        }
        
        print(f"  rect1 size: [{rect1_x:.3f}, {rect1_y:.3f}]")
        print(f"  rect3 size: [{rect3_x:.3f}, {rect3_y:.3f}]")
        
        try:
            # Run simulation with custom rectangles
            result = run_hfss_simulation(
                design_number=i, 
                rectangles_data=custom_rectangles,
                conn=conn
            )
            
            # Add the random sizes to the result for tracking
            result['rect1_size_x'] = rect1_x
            result['rect1_size_y'] = rect1_y
            result['rect3_size_x'] = rect3_x
            result['rect3_size_y'] = rect3_y
            
            all_results.append(result)
            
            print(f"  Design {i} completed successfully!")
            
        except Exception as e:
            print(f"  Error in Design {i}: {str(e)}")
            # Continue with next design even if one fails
            continue
        
        print("-" * 40)
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY OF ALL DESIGNS:")
    print("="*80)
    
    successful_designs = 0
    for result in all_results:
        if 'Design' in result:
            successful_designs += 1
            print(f"Design {result['Design']}:")
            print(f"  rect1 size: [{result.get('rect1_size_x', 'N/A'):.3f}, {result.get('rect1_size_y', 'N/A'):.3f}]")
            print(f"  rect3 size: [{result.get('rect3_size_x', 'N/A'):.3f}, {result.get('rect3_size_y', 'N/A'):.3f}]")
            if 'Min_mag_S11' in result:
                print(f"  Min mag(S(1,1)) = {result['Min_mag_S11']:.6f} at {result['Corresponding_Freq_GHz_S11']:.3f} GHz")
            if 'Min_mag_S21' in result:
                print(f"  Min mag(S(2,1)) = {result['Min_mag_S21']:.6f} at {result['Corresponding_Freq_GHz_S21']:.3f} GHz")
            print()
    
    print(f"Total successful designs: {successful_designs}/100")
    

    conn.close()
    print("Database connection closed.")