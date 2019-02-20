# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 17:51:11 2018

@author: Jackie
"""

#20181029

#import cProfile
import os
from os import listdir
from os.path import isfile, join
import xlrd
import re
import shutil
import MySQLdb

def FileNameInformation(myfilename):
    Gator = re.compile('Gator|GATOR')
    Chinese_Alligator = re.compile('Chinese Alligator|ChineseALI')
    Human = re.compile('Human')
    Crab = re.compile('Crab')
    Dwarf_Crocodile = re.compile('Dwarf Croc')
    Komodo_Dragon = re.compile('Komodo')
    Gharial = re.compile('Gharial')
    timestampregex = re.compile('(\d\d)(\d\d)(\d\d)')
    NYU = re.compile('NYU')    
    GMU = re.compile('GMU')    
    JHU = re.compile('JHU')
    MCD = re.compile('MCD|MD|Megan')
    NN = re.compile('NN')
    YZ = re.compile('YZ')
    JD = re.compile('JD|JDBB')
    CHO = re.compile('CHO')
    
    if Gator.search(myfilename):
        Species = "Gator"
    elif Chinese_Alligator.search(myfilename):
        Species = "Chinese Alligator"
    elif Human.search(myfilename):
        Species = "Human"
    elif Crab.search(myfilename):
        Species = "Crab"
    elif Dwarf_Crocodile.search(myfilename):
        Species = "Dwarf_Crocodile"
    elif Komodo_Dragon.search(myfilename):
        Species = "Komodo_Dragon"
    elif Gharial.search(myfilename):
        Species = "Gharial"
    else:
        Species = ''
    
    locatedate = timestampregex.search(myfilename)
    if locatedate:
        Date_Raw_Data_Acquired = locatedate.group()
    else:
        Date_Raw_Data_Acquired = ''
    
    if NYU.search(myfilename):
        Location = "NYU"
    elif GMU.search(myfilename):
        Location = "GMU"
    elif JHU.search(myfilename):
        Location = "JHU"
    else:
        Location = ''
    
    if MCD.search(myfilename):
        Author = "MCD"
    elif NN.search(myfilename):
        Author = "NN"
    elif YZ.search(myfilename):
        Author = "YZ"
    elif JD.search(myfilename):
        Author = "JD"
    elif CHO.search(myfilename):
        Author = "CHO"
    else:
        Author = ''
    return Species, Date_Raw_Data_Acquired, Location, Author

def DBColumnCheck(myrow):
    yesno = re.compile('Y|N') #column must either have 'Y' or 'N'
    NAMP = re.compile('N?AMP') #column must either have 'NAMP' or 'AMP'
    NC = re.compile('NC') #column just have 'NC'
    PosFloats = re.compile('[0-9]+(\.[0-9]+)?') #column contains a float
    NegFloats = re.compile('-?[0-9]+(\.[0-9]+)?') #columns contains a float. it may be negative
    PosInts = re.compile('[0-9]+') #column contains an integer

    if isinstance(myrow[0], str) is not True: #'ID'
        print('Column error [0]')
        return False
    if isinstance(myrow[1], str) is not True: #'Peptide'
        print('Column error [1]')
        return False
    if PosFloats.match(myrow[2]): #'Peaks_Probability_Score'
        pass
    else:
        print('Column error [2]')
        return False    
    if NegFloats.match(myrow[3]): #'ppm'
        pass
    else:
        print('Column error [3]')
        return False    
    if PosFloats.match(myrow[4]): #'m_over_z'
        pass
    else:
        print('Column error [4]')
        return False
    if PosFloats.match(myrow[5]): #'rt'
        pass
    else:
        print('Column error [5]')
        return False    
    if PosInts.match(myrow[6]): #'scan'
        pass
    else:
        print('Column error [6]')
        return False    
    if isinstance(myrow[7], str) is not True: #'accession'
        print('Column error [7]')
        return False    
    if yesno.match(myrow[8]):  #'PTM'
        pass
    else:
        print('Column error [8]')
        return False    
    if PosFloats.match(myrow[9]): #'Mass'
        pass
    elif NC.match(myrow[9]):
        myrow[9] = None
    else:
        print('Column error [9]')
        return False
    if isinstance(myrow[10], float) is True: #'pI'
        pass
    elif NC.match(myrow[10]):
        myrow[10] = None
    else:
        print('Column error [10]')
        return False    
    if isinstance(myrow[11], float) is True: #'Length'
        pass
    elif NC.match(myrow[11]):
        myrow[11] = None
    else:
        print('Column error [11]')
        return False    
    if isinstance(myrow[12], float) is True: #'Aliphatic_Index'
        pass
    elif NC.match(myrow[12]):
        myrow[12] = None
    else:
        print('Column error [12]')
        return False    
    if isinstance(myrow[13], float) is True: #'Net_Charge'
        pass
    elif NC.match(myrow[13]):
        myrow[13] = None
    else:
        print('Column error [13]')
        return False    
    if isinstance(myrow[14], float) is True: #'Hydropathy'
        pass
    elif NC.match(myrow[14]):
        myrow[14] = None
    else:
        print('Column error [14]')
        return False        
    if isinstance(myrow[15], float) is True: #'Charge_Per_Residue'
        pass
    elif NC.match(myrow[15]):
        myrow[15] = None
    else:
        print('Column error [15]')
        return False    
    if NAMP.match(myrow[16]): #'SVM_Class'
        pass
    elif NC.match(myrow[16]):
        myrow[16] = None
    else:
        print('Column error [16]')
        return False
    if isinstance(myrow[17], float) is True: #'SVM_AMP_Prob'
        pass
    elif NC.match(myrow[17]):
        myrow[17] = None
    else:
        print('Column error [17]')
        return False
    if NAMP.match(myrow[18]): #'RF_Class'
        pass
    elif NC.match(myrow[18]):
        myrow[18] = None
    else:
        print('Column error [18]')
        return False
    if isinstance(myrow[19], float) is True: #'RF_AMP_Prob'
        pass
    elif NC.match(myrow[19]):
        myrow[19] = None
    else:
        print('Column error [19]')
        return False

def DNColumnCheck(myrow):
    yesno = re.compile('Y|N') #column must either have 'Y' or 'N'
    NAMP = re.compile('N?AMP') #column must either have 'NAMP' or 'AMP'
    NC = re.compile('NC') #column just have 'NC'
    PosFloats = re.compile('[0-9]+(\.[0-9]+)?') #column contains a float
    NegFloats = re.compile('-?[0-9]+(\.[0-9]+)?') #columns contains a float. it may be negative
    PosInts = re.compile('[0-9]+') #column contains an integer
    Mode = re.compile('CID|ETD|HCD') #ETD or HCD or CID mode in mass spec

    if isinstance(myrow[0], str) is not True: #'ID'
        print('Column error [0]')
        return False
    if PosInts.match(myrow[1]): #'Scan'
        pass
    else:
        print('Column error [1]')
        return False
    if isinstance(myrow[2], str) is not True: #'Peptide'
        print('Column error [2]')
        return False    
    if PosInts.match(myrow[3]): #'Tag_length'
        pass
    else:
        print('Column error [3]')
        return False
    if PosInts.match(myrow[4]): #'ALC %'
        pass
    else:
        print('Column error [4]')
        return False
    if PosFloats.match(myrow[5]): #'M_over_Z'
       pass
    else:
        print('Column error [5]')
        return False
    if PosInts.match(myrow[6]): #'Z'
       pass
    else:
       return False
    if PosFloats.match(myrow[7]): #'RT'
       pass
    else:
        print('Column error [7]')
        return False
    if NegFloats.match(myrow[8]): #'ppm'
       pass
    else:
        print('Column error [8]')
        return False
    if yesno.match(myrow[9]):  #'PTM'
        pass
    else:
        print('Column error [9]')
        return False    
    if PosInts.match(myrow[10]): #'Local confidence'
        pass
    else:
        print('Column error [10]')
        return False
    if isinstance(myrow[11], str) is not True: #'Tag'
        print('Column error [11]')
        return False
    if Mode.match(myrow[12]): #'Mode'
        pass
    else:
        print('Column error [12]')
        return False
    if PosInts.match(myrow[13]): #'Mass'
        pass
    elif NC.match(myrow[13]): 
        myrow[13] = None
    else:
        print('Column error [13]')
        return False
    if isinstance(myrow[14], float) is True: #'pI'
        pass
    elif NC.match(myrow[14]): 
        myrow[14] = None
    else:
        print('Column error [14]')
        return False    
    if isinstance(myrow[15], float) is True: #'Length'
        pass
    elif NC.match(myrow[15]):
        myrow[15] = None
    else:
        print('Column error [15]')
        return False    
    if isinstance(myrow[16], float) is True: #'Aliphatic_Index'
        pass
    elif NC.match(myrow[16]):
        myrow[16] = None
    else:
        print('Column error [16]')
        return False    
    if isinstance(myrow[17], float) is True: #'Net_Charge'
        pass
    elif NC.match(myrow[17]):
        myrow[17] = None
    else:
        print('Column error [17]')
        return False    
    if isinstance(myrow[18], float) is True: #'Hydropathy'
        pass
    elif NC.match(myrow[18]):
        myrow[18] = None
    else:
        print('Column error [18]')
        return False        
    if isinstance(myrow[19], float) is True: #'Charge_Per_Residue'
        pass
    elif NC.match(myrow[19]):
        myrow[19] = None
    else:
        print('Column error [19]')
        return False    
    if NAMP.match(myrow[20]): #'SVM_Class'
        pass
    elif NC.match(myrow[20]):
        myrow[20] = None
    else:
        print('Column error [20]')
        return False
    if isinstance(myrow[21], float) is True: #'SVM_AMP_Prob'
        pass
    elif NC.match(myrow[21]):
        myrow[21] = None
    else:
        print('Column error [21]')
        return False
    if NAMP.match(myrow[22]): #'RF_Class'
        pass
    elif NC.match(myrow[22]):
        myrow[22] = None
    else:
        print('Column error [22]')
        return False
    if isinstance(myrow[23], float) is True: #'RF_AMP_Prob'
        pass
    elif NC.match(myrow[23]):
        myrow[23] = None
    else:
        print('Column error [23]')
        return False
    if NAMP.match(myrow[24]): #'DA_Class'
        pass
    elif NC.match(myrow[24]): 
        myrow[24] = None
    else:
        print('Column error [24]')
        return False
    if isinstance(myrow[25], float) is True: #'DA_AMP_Prob'
        pass
    elif NC.match(myrow[25]):
        myrow[25] = None
    else:
        print('Column error [25]')
        return False
    return True

def UPLOADFUNCTION():
    mypath = 'C:/Users/jsarna/Documents/historical ShayScript outputs/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    db = MySQLdb.connect(user='', password='', host='', port=, database='')
    c = db.cursor()
    for myfile in onlyfiles:
        if '.xls' and 'novo' in myfile:
            src = mypath + myfile
            dst = 'C:/Users/jsarna/Documents/historical ShayScript outputs/de_novo/'
            shutil.move(src, dst)
            xl = xlrd.open_workbook(dst + myfile)
            worksheet = xl.sheet_by_name("Raw Data")
            myfilename = os.path.basename(myfile)
            myfilename = myfilename.split('.')
            myfilename = myfilename[0]
            FileDestination2 = 'C:/Users/jsarna/Documents/historical ShayScript outputs/de_novo_processed'
            for i in range(2, worksheet.nrows):
                FileNameInformation(myfilename)
                myrow = worksheet.row_values(i)
                myrow.append(myfilename)
                myrow.append(i+1)
                myrow.append(myfilename + str(i+1))
                myrow.extend(FileNameInformation(myfilename))
                PutDeNovoExcelInSQL = '''INSERT INTO De_Novo(DNID,Scan,Peptide,Tag_length,ALC,M_over_Z,Z,RT,ppm,PTM,Local_Confidence,tag,mode,Mass,pI,Length,Aliphatic_Index,Net_Charge,Hydropathy,Charge_Per_Residue,SVM_Class,SVM_AMP_Prob,RF_Class,RF_AMP_Prob,DA_Class,DA_AMP_Prob,Filename,Myrowid,UniqueID,Species,Date_Raw_Data_Acquired,Location,Author) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                if DNColumnCheck(myrow) is True:
                    try:
                        c.execute(PutDeNovoExcelInSQL, myrow)
                        print('processing:', myfilename, i)
                    except MySQLdb.IntegrityError as err:
                        print("an error was thrown", err, myfilename, i)
                        FileDestination2 = 'C:/Users/jsarna/Documents/historical ShayScript outputs/duplicates/'
                        break
                else:
                    print("Incorrect formatting: You are entering data into the wrong column", myfilename, i)
                    FileDestination2 = 'C:/Users/jsarna/Documents/historical ShayScript outputs/bad_de_novo_columns'
                    break
            source2 = dst
            src2 = source2 + myfile
            shutil.move(src2, FileDestination2)
            db.commit()
            print('db.commit: values saved')
        elif '.xls' in myfile:
            xl = xlrd.open_workbook(mypath + myfile)
            worksheet = xl.sheet_by_name("Raw Data")
            myfilename = os.path.basename(myfile)
            myfilename = myfilename.split('.')
            myfilename = myfilename[0]
            FileDestination =  'C:/Users/jsarna/Documents/historical ShayScript outputs/processed'
            for i in range(2, worksheet.nrows):
                FileNameInformation(myfilename)
                myrow = worksheet.row_values(i)
                myrow.append(myfilename)
                myrow.append(i+1)
                myrow.append(myfilename + str(i+1))
                myrow.extend(FileNameInformation(myfilename))
                PutExcelInSQL = '''INSERT INTO Raw_Data(ID,Peptide,Peaks_Probability_Score,ppm,m_over_z,RT,Scan,Accession,PTM,Mass,pI,Length,Aliphatic_Index,Net_Charge,Hydropathy,Charge_Per_Residue,SVM_Class,SVM_AMP_Prob,RF_Class,RF_AMP_Prob,DA_Class,DA_AMP_Prob,Filename,Myrowid,UniqueID,Species,Date_Raw_Data_Acquired,Location,Author) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                if DBColumnCheck(myrow) is True:
                    try:
                        c.execute(PutExcelInSQL, myrow)
                        print('processing:', myfilename, i)
                    except MySQLdb.IntegrityError as err:
                        print("an error was thrown", err, myfilename, i)
                        FileDestination = 'C:/Users/jsarna/Documents/historical ShayScript outputs/duplicates/'
                        break
                else:
                    print("Incorrect formatting: You are entering data into the wrong column", myfilename, i)
                    FileDestination = 'C:/Users/jsarna/Documents/historical ShayScript outputs/bad_columns'
                    break
            source = mypath
            src = source + myfile
            shutil.move(src, FileDestination)
            db.commit()
            print('db.commit: values saved')
    db.close()

UPLOADFUNCTION()

#while 1 > 0:
#    UPLOADFUNCTION()
#    time.sleep(30)

 #cProfile.run('UPLOADFUNCTION()') 
