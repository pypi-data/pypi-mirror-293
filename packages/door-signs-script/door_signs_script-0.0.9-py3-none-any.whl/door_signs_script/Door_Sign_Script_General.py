# Install required packages not already available in Google Colab

import os
from datetime import date
import pandas as pd
import pdfrw
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
import io
import warnings
import sys
import shutil


def main() -> None:
    # Ignore warnings about deprecated packages, functions etc.
    warnings.filterwarnings("ignore")

    # Get users' division
    div = get_div()

    # Get users' specification on which labs to create door signs for
    response, buildings_list, specified_personnel_final, wanted_labs_final = begin_script()

    report_file_location, smartsheet_file_location, template_path, image_paths, \
        old_report_file_location, old_smartsheet_file_location, response, script_location, \
        base_path = get_file_locations(response, div)

    # Ensure file types are .csv
    if os.path.splitext(report_file_location)[1] == '.csv' and os.path.splitext(old_report_file_location)[1] == '.csv':
        current_report = pd.read_csv(report_file_location)
        old_report = pd.read_csv(old_report_file_location)
        current_report = clean_report(current_report, 'current')
        old_report = clean_report(old_report, 'old')
    else:
        _ = input("\nThe current Activity Manager Report file type is not readable. \n"
                  "It should be a .csv file.\n"
                  "Enter any key to close this script: ")
        sys.exit()

    # Ensure Smartsheet file types are .xlsx
    try:
        sheet_1 = pd.ExcelFile(smartsheet_file_location)
        sheet_2 = pd.ExcelFile(old_smartsheet_file_location)
        smartsheet_xls = pd.DataFrame(sheet_1.parse(0))
        old_smartsheet_xls = pd.DataFrame(sheet_2.parse(0))
    except ValueError:
        _ = input("The Smartsheet file was not readable. It is likely that it is not in the xlsx format.\n"
                  "Enter any key to close this script: ")
        sys.exit()

    # Notify user of inactive labs in Activity Manager since last door sign creation
    inactive_labs_check(current_report, old_report)

    changed_hazard_labs = changed_hazard_check(current_report, old_report)
    personnel_changed_labs = changed_personnel_check(smartsheet_xls, old_smartsheet_xls, div)

    # Get the final list of labs to create door signs for
    final_print_labs, door_sign_not_needed_labs, door_sign_needed_labs = final_print_labs_combined_edited(
        changed_hazard_labs,
        personnel_changed_labs,
        current_report,
        response, buildings_list,
        smartsheet_xls,
        specified_personnel_final,
        wanted_labs_final)

    # Create the relevant folders to input the door signs
    needed_loc, not_needed_loc = create_rel_folders(base_path)

    create_door_signs(final_print_labs, smartsheet_xls, template_path,
                      image_paths, door_sign_not_needed_labs, door_sign_needed_labs, needed_loc, not_needed_loc, div)

    delete_rem_files(script_location, div)


def get_div() -> str:
    """Get the users' division"""
    div = ''
    while div.upper() not in ['MSD', 'ALS']:
        div = input('Enter the division you are creating door signs for. '
                    'For example (MSD, ALS): ')
    return div.upper()


def begin_script() -> tuple[str, list[str], list[str], list[str]]:
    """Asks user if they would like to print all lab door signs or only ones with changed information"""

    print('\nThis script creates lab door signs.\n')

    acceptable_responses = ['1', '2', '3', '4', '5']
    response = input('Would you like to create door signs for:\n'
                     '1 - all labs\n'
                     '2 - labs with changed personnel or hazard ID info\n'
                     '3 - specific buildings\n'
                     '4 - specific LSLs or PIs\n'
                     '5 - specific labs (002-0212, 066-0209 etc.)\n'
                     'Your number: ')
    while response not in acceptable_responses:
        response = input('\nYour response was not the numbers 1, 2, 3, 4 or 5. \nPlease enter a valid number: ')

    buildings_list = []
    specified_personnel_final = []
    wanted_labs_final = []
    confirmation = 'n'

    # For specific buildings
    if response == '3':
        while confirmation.lower() == 'n':
            buildings = input('\nEnter the building(s) you would like to create door signs for:\n'
                              'Example: 002, 066, 033\n'
                              'Example: 062\n'
                              'Your building(s): ')

            # Clean the users building list if inputted incorrectly
            buildings_list = buildings.split()
            buildings_list = [building.strip() for building in buildings_list]
            buildings_list = [building.strip(',') for building in buildings_list]

            # Add 0s infront of buildings if needed
            for index, building in enumerate(buildings_list):
                if len(building) == 2:
                    buildings_list[index] = '0' + building
                elif len(building) == 1:
                    buildings_list[index] = '00' + building

            confirmation = input(f'\nThe building(s) you would like to create door signs for are: {buildings_list}\n'
                                 f'Is this correct? Enter \'y\' for yes and \'n\' for no.\n'
                                 f'Your letter: ')

            while confirmation not in ['y', 'n']:
                confirmation = input('The letter you entered was not \'n\' or \'y\'. \nYour letter: ')

    # For specific LSLs or PIs
    elif response == '4':
        while confirmation.lower() == 'n':
            specified_personnel = input('\nEnter the last name(s) of the LSL or PI you would like to create door signs '
                                        'for. Separate by space or comma (Ex: Helms Lanzara Rossi): ')

            # Split a string of names into a list of names
            specified_personnel_final = split_text(specified_personnel)

            confirmation = input(f'\nThe personnel you would like to create door signs for are: '
                                 f'{specified_personnel_final}\n'
                                 f'Is this correct? Enter \'y\' for yes and \'n\' for no.\n'
                                 f'Your letter: ')
            while confirmation not in ['y', 'n']:
                confirmation = input('The letter you entered was not \'n\' or \'y\'. \nYour letter: ')

    # For specific labs
    elif response == '5':
        while confirmation.lower() == 'n':
            wanted_labs = input('\nEnter the labs you would like to create door signs for.\n'
                                'Separate by a comma and space if needed (Ex: 002-0101, 062-0201B, 002-0258).\n'
                                'It is important that the format follows just as the example for stability: ')

            # Get lab list with ', ' as the separater
            wanted_labs_final = wanted_labs.split(', ')
            confirmation = input(f'\nThe lab(s) you would like to create door signs for are: '
                                 f'{wanted_labs_final}\n'
                                 f'Is this correct? Enter \'y\' for yes and \'n\' for no.\n'
                                 f'Your letter: ')
            while confirmation not in ['y', 'n']:
                confirmation = input('The letter you entered was not \'n\' or \'y\'. \nYour letter: ')

    print('\nDoor signs are now being created... This may take a minute.')
    return response, buildings_list, specified_personnel_final, wanted_labs_final


def get_file_locations(response: str, div: str) -> tuple[str, str, str, dict, str, str, str, str, str]:
    """Looks through the user's file system to find the necessary files."""

    base_path = f"/content/drive/MyDrive/{div}_Lab_Contact_and_Door_Signage_Database"

    script_location = base_path + "/Door_Sign_Creation_Files"
    old_report_file_location = ""
    old_smartsheet_file_location = ""

    if not os.path.exists(base_path):
        _ = input(f"The main folder location was not readable.\n"
                  f"It should be titled: \'{div}_Lab_Contact_and_Door_Signage_Database\'.\n"
                  f"It is possible that you did not correctly mount your Google Drive,\n"
                  f"or that you did not did not add a shortcut to your \'MyDrive\'.\n"
                  f"Enter any key to close this script: ")
        sys.exit()

    if not os.path.exists(script_location):
        _ = input(f"The Door_Sign_Creation_Files folder was not found.\n"
                  f"It should be titled: \'Door_Sign_Creation_Files\'.\n"
                  f"It should be in the main {div} folder titled: \'{div}_Lab_Contact_and_Door_Signage_Database\'.\n"
                  f"Enter any key to close this script: ")
        sys.exit()

    # Check to see if the Smartsheet is in the correct location
    if os.path.exists(script_location + f"/{div}_Lab_Safety_DB.xlsx"):
        smartsheet_file_location = script_location + f"/{div}_Lab_Safety_DB.xlsx"
    else:
        _ = input(f"\nThe most recent Smartsheet download was not found. \n"
                  f"Please review the documentation and run the script again.\n"
                  f"It is likely that the script is in the wrong file location or incorrectly named.\n"
                  f"It should be called \'{div}_Lab_Safety_DB.xlsx\' and in the Door_Sign_Creation_Files folder.\n"
                  f"Enter any key to close this script: ")
        sys.exit()

    # Check to see if the Activity Manager query is in the correct location
    if os.path.exists(script_location + "/QueryResult.csv"):
        report_file_location = script_location + "/QueryResult.csv"
    else:
        _ = input("\nThe most recent Activity Manager download was not found. \n"
                  "Please review the documentation and run the script again.\n"
                  "It is likely that the script is in the wrong file location or incorrectly named.\n"
                  "It should be called \'QueryResult.csv\' and in the Door_Sign_Creation_Files folder.\n"
                  "Enter any key to close this script: ")
        sys.exit()

    for file in os.listdir(script_location):
        if file[0:16] == 'OLD_QueryResult_':
            old_report_file_location = os.path.join(script_location, file)
        elif file[0:15] == 'OLD_smartsheet_':
            old_smartsheet_file_location = os.path.join(script_location, file)

    if not old_smartsheet_file_location:
        _ = input("\nThe OLD Smartsheet download was not found. \n"
                  "This script will still run with the newer Smartsheet download.\n"
                  "The script will also continue to print all labs for simplicity [response = 1].\n"
                  "Enter any key to continue: ")

        # If the OLD_smartsheet isn't found, copy the new smartsheet and print all labs (respone=1)
        shutil.copyfile(smartsheet_file_location,
                        base_path + "OLD_smartsheet_" + date.today().strftime("%m_%d_%Y") + ".xlsx")
        old_smartsheet_file_location = base_path + "OLD_smartsheet_" + date.today().strftime("%m_%d_%Y") + ".xlsx"
        response = '1'

    if not old_report_file_location:
        _ = input("\nThe OLD Activity Manager download was not found. \n"
                  "This script will still run with the newer Activity Manager download.\n"
                  "The script will also continue to print all labs for simplicity [response = 1].\n"
                  "Enter any key to continue: ")

        # If the OLD_QueryResult isn't found, copy the new report and print all labs (response=1)
        shutil.copyfile(report_file_location,
                        base_path + "OLD_QueryResult_" + date.today().strftime("%m_%d_%Y") + ".csv")
        old_report_file_location = base_path + "OLD_QueryResult_" + date.today().strftime("%m_%d_%Y") + ".csv"
        response = '1'

    template_path = script_location + "/Door_Sign_Template.pdf"
    if not os.path.exists(template_path):
        _ = input("\nThe door sign template was not found. \n"
                  "It is likely that the file was accidentally deleted or renamed.\n"
                  "It should be called \'Door_Sign_Template.pdf\' and in the Door_Sign_Creation_Files folder.\n"
                  "Enter any key to close this script: ")
        sys.exit()

    image_paths = {
        "Compressed_gas": script_location + "/Compressed_gas.png",
        "Corrosive_Materials": script_location + "/Corrosive_Materials.png",
        "Engineered_Nanomaterial": script_location + "/Engineered_Nanomaterial.jpg",
        "Flammable_Solvents": script_location + "/Flammable_Solvents.png",
        "Flammable_gas": script_location + "/Flammable_gas.png",
        "Highly_Toxic_Chemical": script_location + "/Highly_Toxic_Chemical.jpg",
        "MagneticField": script_location + "/MagneticField.jpg",
        "NIR001HazardIcon": script_location + "/NIR001HazardIcon.jpg",
        "NIR006HazardIcon": script_location + "/NIR006HazardIcon.jpg",
        "Pyrophoric_gas": script_location + "/Pyrophoric_gas.jpg",
        "Reproductive_Toxin": script_location + "/Reproductive_Toxin.jpg",
        "Select_Carcinogen": script_location + "/Select_Carcinogen.jpg",
        "Toxic_Chemicals": script_location + "/Toxic_Chemicals.png",
        "Ultraviolet_Light_Hazard": script_location + "/Ultraviolet_Light_Hazard.jpg",
        "Water_Reactive": script_location + "/Water_Reactive.jpg",
        "Cryogenic_Liquid": script_location + "/Cryogenic_Liquid.jpg"
    }

    # Check to see if the icons are all present
    for key, path in image_paths.items():
        if not os.path.exists(path):
            _ = input(f'The {key} icon was not found. It could have been accidentally deleted or renamed.\n'
                      f'Enter any key to close this script: ')
            sys.exit()

    return report_file_location, smartsheet_file_location, template_path, image_paths, old_report_file_location, \
        old_smartsheet_file_location, response, script_location, base_path


def clean_report(report, report_state: str):
    """Cleans the Activity Manager query to a format readable for door sign creation"""
    final_report = {}
    try:
        for lab in set(report['LOCATIONS SITE NAME']):
            hazards = report.loc[report['LOCATIONS SITE NAME'] == lab, 'HAZARD HAZARD ID'].tolist()
            wpcs = report.loc[report['LOCATIONS SITE NAME'] == lab, 'NUMBER'].tolist()

            # final_report example: {002-0101: [[CHM001, CHM007], [MS259, MS015]]}
            final_report[lab] = [hazards, wpcs]

    except KeyError:
        _ = input(f"\nThere is an error with the {report_state} Activity Manager Download.\n"
                  f"At least one of the LOCATIONS SITE NAME, HAZARD HAZARD ID, and/or NUMBER columns were not found.\n"
                  f"It is recommended to open the file in Excel/Google Sheets and make sure there are columns for lab, hazard ID, and WPC number with the titles above.\n"
                  f"Refer back to the instructions if needed.\n"
                  f"Enter any key to close this script: ")
        sys.exit()

    return final_report


def inactive_labs_check(current_report: dict, old_report: dict) -> None:
    """In the old report, check to see if labs are absent in current report, thus inactive."""

    inactive_labs = []
    for key, val in old_report.items():
        if key not in list(current_report.keys()):
            inactive_labs.append(key)

    if len(inactive_labs) == 1:
        print(f'\nThere is {len(inactive_labs)} lab that is now inactive in Activity Manager since the last door '
              f'sign creation', end='')
    else:
        print(f'\nThere are {len(inactive_labs)} labs that are now inactive in Activity Manager since the last door '
              f'sign creation', end='')
    if len(inactive_labs) >= 1:
        print(':', inactive_labs)
    else:
        print('.')


def changed_hazard_check(current_report: dict, old_report: dict) -> list:
    """Compare current report to old one to find labs with changed hazard IDs."""

    changed_hazard_labs = []
    for key, val in current_report.items():
        if key not in list(old_report.keys()):
            changed_hazard_labs.append(key)
            continue
        elif len(val[0]) != len(old_report[key][0]):
            changed_hazard_labs.append(key)
            continue
        for hazard in val[0]:
            if hazard not in old_report[key][0]:
                changed_hazard_labs.append(key)
                break
    return changed_hazard_labs


def changed_personnel_check(smartsheet_xls, old_smartsheet_xls, div: str) -> list:
    """Compare current Smartsheet to previous Smartsheet to assess changed personnel data."""

    changed_personnel_labs = []

    relevant_cols = ['Lab Safety Lead Name', 'Lab Safety Lead Office Location', 'Lab Safety Lead Office Phone Number',
                     'Lab Safety Lead Mobile Phone Number', 'Backup Safety Lead Name',
                     'Backup Safety Lead Office Location',
                     'Backup Safety Lead Office Phone Number', 'Backup Safety Lead Mobile Phone Number',
                     'Building Manager Name',
                     'Building Manager Office Location', 'Building Manager Office Phone Number',
                     'Building Manager Mobile Phone Number',
                     'Building and Lab Number', 'Door Sign Needed?']

    if div == 'ALS':
        append_cols = ['Minimum Area PPE', 'Secondary Backup Safety Lead Name',
                       'Secondary Backup Safety Lead Office Location',
                       'Secondary Backup Safety Lead Office Phone Number',
                       'Secondary Backup Safety Lead Mobile Phone Number',
                       'ALS Facility Manager Name', 'ALS Facility Manager Office Location',
                       'ALS Facility Manager Office Phone Number',
                       'ALS Facility Manager Mobile Phone Number', 'ALS Safety Coordinator Name',
                       'ALS Safety Coordinator Office Location',
                       'ALS Safety Coordinator Office Phone Number', 'ALS Safety Coordinator Mobile Phone Number']
        relevant_cols += append_cols

    elif div == 'MSD':
        append_cols = ['PI Name', 'PI Office Location', 'PI Office Phone Number', 'PI Mobile Phone Number',
                       'MSD EH&S Tech Name',
                       'MSD EH&S Tech Office Location', 'MSD EH&S Tech Office Phone Number',
                       'MSD EH&S Tech Mobile Phone Number',
                       'MSD Safety Coordinator Name', 'MSD Safety Coordinator Office Location',
                       'MSD Safety Coordinator Office Phone Number',
                       'MSD Safety Coordinator Mobile Phone Number']
        relevant_cols += append_cols

    # Make sure all the columns are titled correctly and still in the smartsheet
    col_error = False
    error_cols = []
    for col in relevant_cols:
        try:
            _ = smartsheet_xls[col]
            _ = old_smartsheet_xls[col]
        except (IndexError, ValueError, KeyError):
            error_cols.append(col)
            col_error = True
            continue
    if col_error:
        _ = input(f"\nOne of the current or old Smartsheet files has changed column headers.\n"
                  f"The following columns were not found: {error_cols}\n"
                  f"You should change the Smartsheet column headers back to as they were.\n"
                  f"Enter any key to close this script: ")
        sys.exit()

    # Compare Smartsheet personnel information, add it to changed_personnel_labs if different.
    for lab in smartsheet_xls["Building and Lab Number"].tolist():

        # Find which rows the labs are in
        new_index = list(smartsheet_xls["Building and Lab Number"]).index(lab)

        if lab in list(old_smartsheet_xls["Building and Lab Number"]):
            old_index = list(old_smartsheet_xls["Building and Lab Number"]).index(lab)
        else:
            # If lab not in old_Smartsheet, add it and continue.
            changed_personnel_labs.append(lab)
            continue

        for col in relevant_cols:
            # If both cells are empty continue
            if pd.isna(list(smartsheet_xls[col])[new_index]) and pd.isna(list(old_smartsheet_xls[col])[old_index]):
                continue

            # If new Smartsheet is empty and old is not empty
            elif pd.isna(list(smartsheet_xls[col])[new_index]) and not \
                    pd.isna(list(old_smartsheet_xls[col])[old_index]):
                changed_personnel_labs.append(lab)
                break

            # If old Smartsheet is empty and new is not empty
            elif pd.isna(list(old_smartsheet_xls[col])[old_index]) and not \
                    pd.isna(list(smartsheet_xls[col])[new_index]):
                changed_personnel_labs.append(lab)
                break

            # If both new and old have different data.
            elif smartsheet_xls.loc[new_index, col] != old_smartsheet_xls.loc[old_index, col]:
                changed_personnel_labs.append(lab)
                break
    return changed_personnel_labs


def split_text(names: str) -> list:
    old_index = 0
    names_final = []

    if pd.isna(names):
        return names_final

    for index, char in enumerate(names):

        # Find the index of the first non alpha character
        while not names[old_index].isalpha():
            old_index += 1

        # Add the first name to the names_final list
        if (not char.isalpha()) and (names[index - 1].isalpha()):
            names_final.append(names[old_index:index].lower())
            old_index = index + 1

        # Add the final name
        elif index == len(names) - 1:
            names_final.append(names[old_index:index + 1].lower())
    return names_final


def final_print_labs_combined_edited(changed_hazard_labs: list, changed_personnel_labs: list, current_report: dict,
                                     response: str, buildings_list: list, smartsheet,
                                     specified_personnel_final: list, wanted_labs_final: list) -> \
        tuple[dict, list, list]:
    """Refine the total_labs variable to include the final dict of labs to print, with values [hazards, wpcs]"""
    relevant_hazards = ["CHM001", "CHM004", "CHM007", "CHM011", "CHM016", "CHM019", "CHM022", "CHM027", "CHM030",
                        "CHM039", "CHM042", "CHM045", "GAS001", "GAS002", "GAS003", "GAS006", "GAS007", "GAS008",
                        "GAS009", "GAS010", "GAS011", "NIR001", "NIR002", "NIR006", "NIR009", "CRY001", "CRY003",
                        "CRY004", "CRY005", "CRY006", "CRY007", "CRY010", "CRY011"]
    total_labs = []

    # For all labs
    if response == '1':
        total_labs = list(current_report.keys())

    # Only for changed hazard or changed personnel labs
    elif response == '2':
        changed_personnel_labs = [x for x in changed_personnel_labs if x != 'nan' and not pd.isna(x)]
        changed_hazard_labs = [x for x in changed_hazard_labs if x != 'nan' and not pd.isna(x)]
        total_labs = changed_personnel_labs + changed_hazard_labs

    # For specific buildings
    elif response == '3':
        total_labs = []
        for lab in current_report.keys():
            end_index = lab.find('-')
            if lab[0:end_index] in buildings_list:
                total_labs.append(lab)

    # For specific personnel (last names)
    elif response == '4':
        last_names = []
        for num in range(len(smartsheet)):
            lsl_names = split_text(smartsheet['Lab Safety Lead Name'][num])
            pi_names = split_text(smartsheet['PI Name'][num])
            last_names.append(lsl_names + pi_names)
        last_names_dict = pd.DataFrame({'Building_Lab': smartsheet['Building and Lab Number'],
                                        'Last_Names': last_names})
        for name in specified_personnel_final:
            for index, last_names in enumerate(last_names_dict['Last_Names']):
                if name in last_names:
                    total_labs.append(last_names_dict['Building_Lab'][index])

    # For specific labs
    elif response == '5':
        total_labs = wanted_labs_final

    total_labs = sorted(set(total_labs))

    indices = smartsheet['Building and Lab Number'].isin(total_labs).tolist()
    smartsheet_subset = smartsheet.loc[indices]

    door_sign_not_needed_indices = pd.isna(smartsheet_subset['Door Sign Needed?']).tolist()
    door_sign_not_needed_rows = smartsheet_subset.iloc[door_sign_not_needed_indices]

    if len(door_sign_not_needed_rows) >= 1:
        door_sign_not_needed_labs = door_sign_not_needed_rows['Building and Lab Number'].tolist()
    else:
        door_sign_not_needed_labs = []

    door_sign_needed_indices = []
    for val in door_sign_not_needed_indices:
        if val:
            door_sign_needed_indices.append(False)
        else:
            door_sign_needed_indices.append(True)
    door_sign_needed_rows = smartsheet_subset.iloc[door_sign_needed_indices]

    if len(door_sign_needed_rows) >= 1:
        door_sign_needed_labs = door_sign_needed_rows['Building and Lab Number'].tolist()
    else:
        door_sign_needed_labs = []

    # Create final_labs[lab] = [hazards, wpcs]
    final_labs = {}
    inactive_labs = []
    for lab in total_labs:
        current_relevant_hazards = []
        if lab in list(current_report.keys()):
            for hazard in current_report[lab][0]:
                if hazard in relevant_hazards:
                    current_relevant_hazards.append(hazard)
            final_labs[lab] = [current_relevant_hazards, current_report[lab][1]]
        else:
            inactive_labs.append(lab)

    # Only include labs with active hazards
    final_labs_edited = {}
    for key, val in final_labs.items():
        if val[0]:
            final_labs_edited[key] = val

    changed_personnel_labs = [x for x in changed_personnel_labs if not pd.isna(x)]
    changed_hazard_labs = [x for x in changed_hazard_labs if not pd.isna(x)]

    if len(changed_personnel_labs) == 1:
        print(f'\nThere is {len(changed_personnel_labs)} lab that has changed personnel data in Smartsheet', end='')
    else:
        print(f'\nThere are {len(changed_personnel_labs)} labs that have changed personnel data in Smartsheet', end='')

    if len(changed_personnel_labs) >= 1:
        print(':\n', changed_personnel_labs)
    else:
        print('.')

    if len(changed_hazard_labs) == 1:
        print(f'\nThere is {len(changed_hazard_labs)} lab that has changed hazards in Activity Manager', end='')
    else:
        print(f'\nThere are {len(changed_hazard_labs)} labs that have changed hazards in Activity Manager', end='')

    if len(changed_hazard_labs) >= 1:
        print(':\n', changed_hazard_labs)
    else:
        print('.')

    return final_labs_edited, door_sign_not_needed_labs, door_sign_needed_labs


def list_to_string(element: list) -> str:
    """Return a list from a string with ', ' separator"""
    element = set(element)
    return ", ".join(str(item) for item in element)


def create_rel_folders(base_path: str) -> tuple[str, str]:
    """Creates the folders needed to place the door signs in"""

    # Create Door_Signs_Created_MM_DD_YYYY
    new_folder_loc = base_path + "/Door_Signs_Created_" + date.today().strftime("%m_%d_%Y")

    # If that folder already exists, create Door_Signs_Created_MM_DD_YYYY_vX
    if os.path.exists(new_folder_loc):
        new_folder_loc = new_folder_loc + "_v"
        for num in range(2, 100):
            if not os.path.exists(new_folder_loc + str(num)):
                os.makedirs(new_folder_loc + str(num))
                new_folder_loc = new_folder_loc + str(num)
                break
    else:
        os.makedirs(new_folder_loc)

    # Add the Door_Signs_Needed, and Door_Signs_Not_Needed folders within Door_Signs_Created_XX/XX/XXXX
    needed_loc = new_folder_loc + "/Door_Signs_Needed_" + date.today().strftime("%m_%d_%Y")
    not_needed_loc = new_folder_loc + "/Door_Signs_Not_Needed_" + date.today().strftime("%m_%d_%Y")

    try:
        os.makedirs(needed_loc)
        os.makedirs(not_needed_loc)
    except FileExistsError:
        pass
    except OSError:
        _ = input("You do not have the sharing permissions needed to create door signs.\n"
                  "If it is a shared Google Drive, you must have at least a Content Manager permission.\n"
                  "If it is a regular Google Drive shared with you, you must have at least editing permissions.\n"
                  "Enter any key to close this script: ")
        sys.exit()
    return needed_loc, not_needed_loc


def create_door_signs(final_print_labs: dict, smartsheet_xls, template_path: str, image_paths: dict,
                      door_sign_not_needed_labs: list, door_sign_needed_labs: list, needed_loc: str,
                      not_needed_loc: str, div: str) -> None:
    """Creates pdfs of the lab door signs from the template and hazard icons. Populate fields with Smartsheet data."""

    labs_wo_personnel_data = []
    long_writer_needed = pdfrw.PdfWriter()
    long_writer_not_needed = pdfrw.PdfWriter()

    print('\nLab door signs created for: ')
    counter = 1

    for key, val in final_print_labs.items():

        # If the building key is not in the 006-0152 format, continue
        if (key[0].isalpha()) or (',' in key):
            continue

        # Check if the lab needs a door sign or not and update output_path accordingly
        if key in door_sign_not_needed_labs:
            output_path = not_needed_loc + f"/{key}.pdf"
            not_needed = True
        else:
            output_path = needed_loc + f"/{key}.pdf"
            not_needed = False

        current_building, current_room = get_building_room(key)

        # images_list is a list of the image file locations
        images_list = get_relevant_hazards(val[0], image_paths, div)

        # Check if the lab has personnel data in Smartsheet, then add data to door sign
        if key in list(smartsheet_xls["Building and Lab Number"]):
            fields_to_fill = get_personnel_data(key, smartsheet_xls, current_building, current_room, val[1], div)
            input_data_to_pdf(template_path, fields_to_fill, output_path, no_personnel_data=False)
            add_images(images_list, output_path)
        else:
            labs_wo_personnel_data.append(key)
            fields_to_fill = {'Building': current_building, 'Room': current_room,
                              'Applicable_WPC': list_to_string(val[1]),
                              'Date_Completed': date.today().strftime("%m/%d/%Y")}
            input_data_to_pdf(template_path, fields_to_fill, output_path, no_personnel_data=True)
            add_images(images_list, output_path)

        # Print the door signs created
        if key == list(final_print_labs.keys())[-1]:
            print(key, end='\n')
        else:
            print(key, end=', ')

        counter += 1
        if counter % 10 == 0:
            print('\n')

        output_pdf = pdfrw.PdfReader(output_path)
        if not_needed:
            long_writer_not_needed.addpage(output_pdf.pages[0])
        else:
            long_writer_needed.addpage(output_pdf.pages[0])

    if door_sign_not_needed_labs:
        long_writer_not_needed.write(not_needed_loc + "/Door_Signs_Not_Needed_Long.pdf")
    if door_sign_needed_labs:
        long_writer_needed.write(needed_loc + "/Door_Signs_Needed_Long.pdf")

    print(f"\nThere are {len(labs_wo_personnel_data)} labs that do not have data in Smartsheet. You may still edit"
          f" and input data manually onto the door sign after downloading the file", end='')

    if len(labs_wo_personnel_data) >= 1:
        print(':\n')
        counter = 1
        for lab in labs_wo_personnel_data:
            if counter % 10 == 0:
                end = ',\n'
            elif lab == labs_wo_personnel_data[-1]:
                end = '\n'
            else:
                end = ', '
            print(lab, end=end)
            counter += 1
    else:
        print('.')


def input_data_to_pdf(template_path: str, fields_to_fill: dict, output_path: str, no_personnel_data: bool) -> None:
    """Inputs Smartsheet personnel and WPC data onto the door sign"""

    template_pdf = pdfrw.PdfReader(template_path)
    annotations = template_pdf.pages[0]["/Annots"]
    for annotation in annotations:
        if annotation["/Subtype"] == "/Widget":
            if annotation["/T"]:
                field = annotation["/T"][1:-1]
                if no_personnel_data and field not in ['Room', 'Building', 'Applicable_WPC', 'Date_Completed',
                                                       'Min_PPE_Req']:
                    continue
                final_field = ""
                for num in range(len(field)):
                    if field[num] in ["\\", "1", "3", "7"]:
                        if final_field[-1] != "_":
                            final_field += "_"
                        else:
                            continue
                    else:
                        final_field += field[num]
                if final_field in list(fields_to_fill.keys()):
                    if pd.isna(fields_to_fill[final_field]):
                        final_val = " "
                    else:
                        final_val = fields_to_fill[final_field]
                    annotation.update(pdfrw.PdfDict(V='{}'.format(final_val)))
                    annotation.update(pdfrw.PdfDict(AP=''))
                    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))

    writer = pdfrw.PdfWriter()
    writer.addpage(template_pdf.pages[0])
    writer.write(output_path)


def add_images(images_list: list, output_path: str) -> None:
    """Adds the hazard icons to the door sign"""

    if len(images_list) > 6:
        width = 150 - len(images_list) * 4.5
    else:
        width = 150 - len(images_list) * 6.33

    total_space = 600 - width

    # If there's less than 4 images, put them all in the middle equally spaced
    if len(images_list) < 4:
        y = 425
        for index, img_file in enumerate(images_list):
            x = ((total_space / (len(images_list) + 1)) * (index + 1)) + 10
            add_icon(x, y, width, img_file, output_path)

    else:
        total_space += width
        middle_sep = len(images_list) // 2

        # Separate into first and second row of icons
        first_row = images_list[:middle_sep]
        second_row = images_list[middle_sep:]

        # The denominator for the x coordinate below is not perfect, but works well.
        for index, img_file in enumerate(first_row):
            x = ((total_space / (len(first_row) + 1)) * (index + 1)) - (width / 2)
            y = 365
            add_icon(x, y, width, img_file, output_path)

        for index, img_file in enumerate(second_row):
            x = ((total_space / (len(second_row) + 1)) * (index + 1)) - (width / 2)
            y = 520
            add_icon(x, y, width, img_file, output_path)


def get_building_room(lab: str) -> tuple:
    """From the data dictionary keys (002-0101), return the building and room."""

    current_building = ""
    current_room = ""

    for num in range(len(lab)):
        if lab[num] == "-":
            current_room = lab[num + 1:]
            break
        else:
            current_building = current_building + lab[num]

    return current_building, current_room


def get_personnel_data(lab: str, smartsheet, building: str, room: str, wpcs: list, div: str) -> dict:
    """With the Smartsheet, return the personnel data needed for the door sign."""

    index = list(smartsheet["Building and Lab Number"]).index(lab)
    fields_to_fill = {}

    if div == 'MSD':
        fields_to_fill = {"Building": building,
                          "Room": room,
                          "Applicable_WPC": list_to_string(wpcs),
                          "PI_Name": list(smartsheet["PI Name"])[index],
                          "PI_Office_Location": list(smartsheet["PI Office Location"])[index],
                          "PI_Work_Phone": list(smartsheet["PI Office Phone Number"])[index],
                          "PI_Other_Phone": list(smartsheet["PI Mobile Phone Number"])[index],
                          "Area_Safety_Leader_Name": list(smartsheet["Lab Safety Lead Name"])[index],
                          "Area_Safety_Leader_Office_Location": list(smartsheet["Lab Safety Lead Office Location"])[
                              index],
                          "Area_Safety_Leader_Work_Phone": list(smartsheet["Lab Safety Lead Office Phone Number"])[
                              index],
                          "Area_Safety_Leader_Other_Phone": list(smartsheet["Lab Safety Lead Mobile Phone Number"])[
                              index],
                          "Additional_Contacts_Name": list(smartsheet["Backup Safety Lead Name"])[index],
                          "Additional_Contacts_Office_Location": list(smartsheet["Backup Safety Lead Office Location"])[
                              index],
                          "Additional_Contacts_Work_Phone": list(smartsheet["Backup Safety Lead Office Phone Number"])[
                              index],
                          "Additional_Contacts_Other_Phone": list(smartsheet["Backup Safety Lead Mobile Phone Number"])[
                              index],
                          "MSD_EHS_Tech_Name": list(smartsheet["MSD EH&S Tech Name"])[index],
                          "MSD_EHS_Tech_Office_Location": list(smartsheet["MSD EH&S Tech Office Location"])[index],
                          "MSD_EHS_Tech_Work_Phone": list(smartsheet["MSD EH&S Tech Office Phone Number"])[index],
                          "MSD_EHS_Tech_Other_Phone": list(smartsheet["MSD EH&S Tech Mobile Phone Number"])[index],
                          "Building_Manager_Name": list(smartsheet["Building Manager Name"])[index],
                          "Building_Manager_Office_Location": list(smartsheet["Building Manager Office Location"])[
                              index],
                          "Building_Manager_Work_Phone": list(smartsheet["Building Manager Office Phone Number"])[
                              index],
                          "Building_Manager_Other_Phone": list(smartsheet["Building Manager Mobile Phone Number"])[
                              index],
                          "Div_Safety_Coordinator_Name": list(smartsheet["MSD Safety Coordinator Name"])[index],
                          "Div_Safety_Coordinator_Office_Location":
                              list(smartsheet["MSD Safety Coordinator Office Location"])[index],
                          "Div_Safety_Coordinator_Work_Phone":
                              list(smartsheet["MSD Safety Coordinator Office Phone Number"])[index],
                          "Div_Safety_Coordinator_Other_Phone":
                              list(smartsheet["MSD Safety Coordinator Mobile Phone Number"])[index],
                          "Date_Completed": date.today().strftime("%m/%d/%Y")
                          }

    if div == 'ALS':
        fields_to_fill = {"Building": building,
                          "Room": room,
                          "Min_PPE_Req": list(smartsheet["Minimum Area PPE"])[index],
                          "Applicable_WPC": list_to_string(wpcs),
                          "Area_Safety_Leader_Name": list(smartsheet["Lab Safety Lead Name"])[index],
                          "Area_Safety_Leader_Office_Location": list(smartsheet["Lab Safety Lead Office Location"])[
                              index],
                          "Area_Safety_Leader_Work_Phone": list(smartsheet["Lab Safety Lead Office Phone Number"])[
                              index],
                          "Area_Safety_Leader_Other_Phone": list(smartsheet["Lab Safety Lead Mobile Phone Number"])[
                              index],
                          "Additional_Contacts_Name": list(smartsheet["Backup Safety Lead Name"])[index],
                          "Additional_Contacts_Office_Location": list(smartsheet["Backup Safety Lead Office Location"])[
                              index],
                          "Additional_Contacts_Work_Phone": list(smartsheet["Backup Safety Lead Office Phone Number"])[
                              index],
                          "Additional_Contacts_Other_Phone": list(smartsheet["Backup Safety Lead Mobile Phone Number"])[
                              index],
                          "Secondary_Contacts_Name": list(smartsheet["Secondary Backup Safety Lead Name"])[index],
                          "Secondary_Contacts_Office_Location":
                              list(smartsheet["Secondary Backup Safety Lead Office Location"])[index],
                          "Secondary_Contacts_Work_Phone":
                              list(smartsheet["Secondary Backup Safety Lead Office Phone Number"])[index],
                          "Secondary_Contacts_Other_Phone":
                              list(smartsheet["Secondary Backup Safety Lead Mobile Phone Number"])[index],
                          "ALS_Facility_Manager_Name": list(smartsheet["ALS Facility Manager Name"])[index],
                          "ALS_Facility_Manager_Office_Location":
                              list(smartsheet["ALS Facility Manager Office Location"])[index],
                          "ALS_Facility_Manager_Work_Phone":
                              list(smartsheet["ALS Facility Manager Office Phone Number"])[index],
                          "ALS_Facility_Manager_Other_Phone":
                              list(smartsheet["ALS Facility Manager Mobile Phone Number"])[index],
                          "Building_Manager_Name": list(smartsheet["Building Manager Name"])[index],
                          "Building_Manager_Office_Location": list(smartsheet["Building Manager Office Location"])[
                              index],
                          "Building_Manager_Work_Phone": list(smartsheet["Building Manager Office Phone Number"])[
                              index],
                          "Building_Manager_Other_Phone": list(smartsheet["Building Manager Mobile Phone Number"])[
                              index],
                          "Div_Safety_Coordinator_Name": list(smartsheet["ALS Safety Coordinator Name"])[index],
                          "Div_Safety_Coordinator_Office_Location":
                              list(smartsheet["ALS Safety Coordinator Office Location"])[index],
                          "Div_Safety_Coordinator_Work_Phone":
                              list(smartsheet["ALS Safety Coordinator Office Phone Number"])[index],
                          "Div_Safety_Coordinator_Other_Phone":
                              list(smartsheet["ALS Safety Coordinator Mobile Phone Number"])[index],
                          "Date_Completed": date.today().strftime("%m/%d/%Y")
                          }

    return fields_to_fill


def get_relevant_hazards(all_images: list, image_paths: dict, div: str) -> list:
    """Append the images needed depending on the hazards present."""

    # Each variable denotes the title of the hazard icon, and the list represents the hazards associated
    corrosive_hazards = ["CHM001", "CHM004", "CHM007", "CHM027", "GAS006"]
    flammable_solv_hazards = ["CHM011"]
    highly_toxic_hazards = ["CHM016", "CHM039", "CHM045", "GAS010"]
    reproductive_hazards = ["CHM019"]
    carcinogen_hazards = ["CHM022"]
    water_hazards = ["CHM030"]
    nanomaterial_hazards = ["CHM042"]
    uv_hazards = ["NIR001", "NIR009"]
    nir001_hazard = ["NIR001"]
    magnetic_hazard = ["NIR002"]
    nir006_hazard = ["NIR006"]
    compressed_hazards = ["GAS001", "GAS002", "GAS006", "GAS007", "GAS008", "GAS009", "GAS010", "GAS011"]
    flammable_gas_hazards = ["GAS003"]
    toxic_hazards = ["GAS006", "GAS009"]
    pyrophoric_hazards = ["GAS011"]
    cryogenic_hazards = ["CRY001", "CRY003", "CRY004", "CRY005", "CRY006", "CRY007", "CRY010", "CRY011"]

    if div == 'ALS':
        flammable_solv_hazards.append("CHM013")
        highly_toxic_hazards.append("CHM007")
        toxic_hazards.append("CHM055")
        toxic_hazards.append("GAS010")

    images_list = []
    for hazard in all_images:
        hazard = str(hazard)
        if hazard in corrosive_hazards:
            images_list.append(image_paths["Corrosive_Materials"])
        if hazard in flammable_solv_hazards:
            images_list.append(image_paths["Flammable_Solvents"])
        if hazard in highly_toxic_hazards:
            images_list.append(image_paths["Highly_Toxic_Chemical"])
        if hazard in reproductive_hazards:
            images_list.append(image_paths["Reproductive_Toxin"])
        if hazard in carcinogen_hazards:
            images_list.append(image_paths["Select_Carcinogen"])
        if hazard in water_hazards:
            images_list.append(image_paths["Water_Reactive"])
        if hazard in nanomaterial_hazards:
            images_list.append(image_paths["Engineered_Nanomaterial"])
        if hazard in uv_hazards:
            images_list.append(image_paths["Ultraviolet_Light_Hazard"])
        if hazard in nir001_hazard:
            images_list.append(image_paths["NIR001HazardIcon"])
        if hazard in magnetic_hazard:
            images_list.append(image_paths["MagneticField"])
        if hazard in nir006_hazard:
            images_list.append(image_paths["NIR006HazardIcon"])
        if hazard in compressed_hazards:
            images_list.append(image_paths["Compressed_gas"])
        if hazard in flammable_gas_hazards:
            images_list.append(image_paths["Flammable_gas"])
        if hazard in toxic_hazards:
            images_list.append(image_paths["Toxic_Chemicals"])
        if hazard in pyrophoric_hazards:
            images_list.append(image_paths["Pyrophoric_gas"])
        if hazard in cryogenic_hazards:
            images_list.append(image_paths["Cryogenic_Liquid"])

    images_list = list(set(images_list))
    return images_list


def add_icon(x: float, y: float, width: float, img_file: str, output_path: str) -> None:
    """Add hazard icons to the PDF."""

    in_pdf_file = output_path
    out_pdf_file = output_path
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    # Make subtle adjustments to image width depending on the image, because some have different orientation and size
    if (img_file[-18:] == "Compressed_gas.png") or (img_file[-18:] == "Water_Reactive.jpg") or \
            (img_file[-17:] == "Flammable_gas.png"):
        width = 0.7567 * width
        x += 11
    elif img_file[-27:] == "Engineered_Nanomaterial.jpg":
        width = 0.7535 * width
        x += 7
    elif (img_file[-20:] == "NIR006HazardIcon.jpg") or (img_file[-20:] == "NIR001HazardIcon.jpg"):
        width = 0.7567 * width
        x += 13
    elif img_file[-28:] == "Ultraviolet_Light_Hazard.jpg":
        width = 0.7067 * width
        x += 15

    can.drawImage(img_file, x, y, width=width, preserveAspectRatio=True, mask='auto', height=width)
    can.showPage()
    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # read the existing PDF
    existing_pdf = PdfReader(open(in_pdf_file, "rb"))
    output = PdfWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        page.merge_page(new_pdf.pages[i])
        output.add_page(page)

    output_stream = open(out_pdf_file, "wb")
    output.write(output_stream)
    output_stream.close()


def delete_rem_files(script_location: str, div: str) -> None:
    """This function creates a folder in shared MSD Drive with today's date, then puts lab door signs into there."""

    # Delete OLD_report, OLD_smartsheet, current report and current smartsheet.
    for file in os.listdir(script_location):
        if file[0:16] == 'OLD_QueryResult_':
            os.remove(script_location + "/" + file)
        elif file[0:15] == 'OLD_smartsheet_':
            os.remove(script_location + "/" + file)
        elif file[0:11] == 'QueryResult':
            os.rename(script_location + "/" + file,
                      script_location + '/OLD_QueryResult_' + date.today().strftime("%m_%d_%Y") + '.csv')
        elif file == f'{div}_Lab_Safety_DB.xlsx':
            os.rename(script_location + "/" + file,
                      script_location + '/OLD_smartsheet_' + date.today().strftime("%m_%d_%Y") + '.xlsx')
            shutil.copyfile(script_location + '/OLD_smartsheet_' + date.today().strftime("%m_%d_%Y") + '.xlsx',
                            f"/content/drive/MyDrive/{div}_Lab_Contact_and_Door_Signage_Database/Smartsheet_Archive/Smartsheet_" + date.today().strftime(
                                "%m_%d_%Y") + ".xlsx")

    _ = input('\nThe door signs have been uploaded to Google Drive!\n'
              'If you would like to change information on any door sign, download the file then open in Chrome or any other browser.\n'
              'Script created by AJHetherwick@lbl.gov, with assistance from LKing@lbl.gov\n'
              'Enter any key to close this script: ')


