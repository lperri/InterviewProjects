import os,glob
import csv
from sys import exit
import argparse

# obtain path to directory from user
parser = argparse.ArgumentParser(description='Get path to directory containing text files that you want to convert to CSVs')
parser.add_argument('in_path',type=str,help='path to directory containing all text files you want to convert to CSV')
parser.add_argument('--out_path',type=str,help='path to directory where you want to put CSVs; by default, will be placed in same directory as the text files being converted within subdirectory called "CSVs"; example:--out_path="~/Desktop/CSVfiles/"')
args = parser.parse_args()
# store path(s) as variable(s)
in_path = args.in_path
out_path = args.out_path

# dictionary of text file names as keys, column names as values
field_names_dict = {'DATA_SRC':['DataSrc_ID', 'Authors', 'Title', 'Year', 'Journal', 'Vol_City', 'Issue_State', 'Start_Page', 'End_Page'],
                'DATSRCLN':['NDB_No', 'Nutr_No', 'DataSrc_ID'], 
                'DERIV_CD':['Deriv_CD', 'Deriv_Desc'],
                'FD_GROUP':['FdGrp_Cd', 'FdGrp_Desc'],
                'FOOD_DES':['NBD_No', 'FdGrp_Cd', 'Long_Desc', 'Shrt_Desc', 'ComName', 'ManufacName', 'Survey', 'Ref_desc', 'Refuse', 'SciName', 'N_Factor', 'Pro_Factor', 'Fat_Factor', 'CHO_Factor'],
                'FOOTNOTE':['NBD_No', 'Footnt_No', 'Footnt_Typ', 'Nutr_No', 'Footnt_Txt'],
                'LANGDESC':['Factor_Code', 'Description'],
                'LANGUAL':['NDB_No', 'Factor_Code'],
                'NUT_DATA':['NDB_No', 'Nutr_No', 'Nutr_Val', 'Num_Data_Pts', 'Std_Error', 'Src_Cd', 'Deriv_Cd', 'Ref_NDB_No', 'Add_Nutr_Mark', 'Num_Studies', 'Min', 'Max', 'DF', 'Low_EB', 'Up_EB', 'Stat_cmt', 'AddMod_Date'],
                'NUTR_DEF':['Nutr_No', 'Units', 'Tagname', 'NutrDesc', 'Num_Dec', 'SR_Order'],
                'SRC_CD':['Src_Cd', 'SrcCd_Desc'],
                'WEIGHT':['NDB_No', 'Seq', 'Amount', 'Msre_Desc', 'Gm_Wgt', 'Num_Data_Pts', 'Std_Dev']
                }


def getPathsToTextFiles(in_path):
    """ Input verified path to directory containing text files that you want to convert to CSVs; return paths to individual text files. """
    # collect all files in verified directory that end in .txt file extension
    paths_to_text_files = [text_file_name for text_file_name in glob.glob(in_path+"/*.txt")]
    return paths_to_text_files


def nameOfFile(path_to_text_file):
    """ Input path to the text file; return string with name of file, minus .txt extension """
    # get name of file including file extension
    base = os.path.basename(path_to_text_file)
    # return file name without .txt extension
    return os.path.splitext(base)[0]    


def checkOutPathExistance(out_path):
    """ Input path to CSVs (if user specifies path to CSV dir, use that; otherwise, make dir called CSVs inside the dir containing the text files); ensures existence of this dir """
    if out_path == None:
        out_path = in_path + '/CSVs/'
    # if CSV dir doesn't yet exist, make it
    if os.path.isdir(out_path) == False:
        os.makedirs(out_path)


def convertTextToCSV(path_to_text_file,out_path):
    """ Input path to the text file and path to CSV dir; CSVs generated """
    # note: I did not use the Pandas library becuase it requires installation
    name_of_file = nameOfFile(path_to_text_file)
    field_names = field_names_dict[name_of_file]
    # if user specifies path to CSV dir, use that, but otherwise but it in the same dir as the text files in its own dir called CSVs
    if out_path == None:
        out_path = in_path + '/CSVs/'
    # if CSV dir doesn't yet exist, make it
    if os.path.isdir(out_path) == False:
        os.makedirs(out_path)
    # open the text file and an empty csv file and read lines in text file
    with open(path_to_text_file,'r') as text_file:
        with open(out_path+name_of_file+'.csv','w') as csv_file:
            csv_reader = csv.reader(text_file, delimiter='^', quotechar='~')
            # write CSVs
            writer = csv.writer(csv_file, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(field_names)
            for line in csv_reader:
                writer.writerow(line)


def main():    
    # check to make sure the path to the text files dir exists
    if os.path.isdir(in_path) == False:
        print 'Please specify a path to directory containing text files that exists. Exiting program...' 
        exit()
    # get paths to text files and make CSVs
    paths_to_text_files = getPathsToTextFiles(in_path)
    for path_to_text_file in paths_to_text_files:
        convertTextToCSV(path_to_text_file,out_path)


# run program
main()
