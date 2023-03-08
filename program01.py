#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One of the mechanisms used to store and manage large quantities of
data is databases. There are many types of databases, but the one that
has revolutionized the sector is the database organized according to
the relational model theorized by Codd half a century ago. According
to this model, the data are arranged in tables in direct relation, to
optimize memory requirements, promote data consistency and minimize
errors.

We need to design a set of functions that implements a simple
relational database for a training school, with four tables, namely
students, teachers, courses, and exams. The databases can be of three
sizes: small, medium, and large. The database tables of size dbsize
are in four JSON files <dbsize>_<table name>.json (for example, the
small DB consists of the files small_students.json,
small_teachers.json, small_courses.json, and small_exams.json). The
tables are implemented as lists of dictionaries (see, for example, the
file small_students.json) and have the following structures:
   - students: keys stud_code, stud_name, stud_surname, stud_email
   - teachers: keys teach_code, teach_name, teach_surname, teach_email
   - courses: keys course_code, course_name, teach_code
   - exams: keys exam_code, course_code, stud_code, date, grade.
The relationship between the tables implies that each row in each of
the tables have a reference to another table: an exam (exam_code)
corresponds to a grade given by the teacher (teach_code) to a student
(stud_code) for having taken an exam of a given course (course_code)
in a certain date. Every student can have taken several exams. Every
teacher can be responsible for several courses. However, exactly
one teacher is responsible for every course.

The field stud_code is the primary key for the students table since
it uniquely identifies a student; namely no two students have the same
stud_code. Similarly, teach_code is the primary key for the teachers table,
course_code for the courses table and exam_code for the exams tables.
Thus, they are used to realize the relationships between the tables.

The fields in all tables are never empty.

We must realize some functions to query databases of different sizes.
Then, every function always requires a 'dbsize' string type parameter, which can assume the values 'small,' 'medium,' and 'large.'
The functions are:

    - student_average(stud_code, dbsize), which receives the code of
      a student and returns the average of the grades of the exams
      taken by the student.

    - course_average(course_code, dbsize), which receives the code of
      a course and returns the average grade of the exams for that
      course, taken by all students.

    - teacher_average(teach_code, dbsize), which receives the code of
      a teacher and returns the average grade for all the exams taken
      in all of the teacher's courses.

    - top_students(dbisze), which returns the list of the 'stud_code's
      of those students with an average of taken exams, greater than
      or equal to 28. The stud_codes are sorted in descending order by
      average grade and, in case of a tie, in lexicographic order by
      the student's last name and first name, finally the stud_code
      in ascending order.

    - print_recorded_exams(stud_code, fileout, dbsize), which receives a
      stud_code of a student and saves in fileout the list of the exams
      taken by that student. The rows are sorted in ascending
      order by date of exam taken and, in case of the same date, by
      alphabetical order of the exam names. The file has an initial line
      with the text
"Exams taken by student <stud_surname> <stud_name>, student number <stud_code>",
      while the following lines have the following structure:
"<course_name>\t<date>\t<grade>",
      where the fields are aligned with the longest course name (i.e. all
      dates and grades are vertically aligned). The function returns the
      number of exams taken by the student.

    - print_top_students(fileout, dbsize), which saves in fileout a
      row for each student with an average grade greater than or equal
      to 28. The rows in the file are in descending order by average
      grade and, in case of a tie, in lexicographic order by the
      student's last name and first name.
      The rows in the file have the following structure:
"<stud_surname> <names>\t<average>",
      where the average values are vertically aligned for all rows. The
      function returns the number of rows saved in the file.

    - print_exam_record(exam_code, fileout, dbsize), which receives an
      exam_code of an exam and saves in fileout the information about that
      exam, using the following formula
"The student <stud_surname> <stud_name>, student number <stud_code>, took on <date> the <course_name> exam with the teacher <teach_surname> <teach_name> with grade <grade>."
      The function returns the exam grade associated with the exam_code
      received as input.

All averages are rounded to the second decimal place, before any sorting.
All files must have "utf8" encoding.
To easily print aligned rows, consider the format function with the
modifiers for alignment (https://pyformat.info/#string_pad_align)

"""

import json
def openar(filename,dbsize,*wanted):
    with open(dbsize + '_' + filename + '.json') as f:
        result= []
        data = json.load(f)
        for dicts in data:
            for k, v in dicts.items():
                if k == wanted[0]:
                    result.append(v)
                try:
                    if k == wanted[1]:
                        result.append(v)
                    if k == wanted[3]:
                        result.append(v)
                except:
                    continue
        return result
                    
#openar('exams','small','grade','date')                   
def student_average(stud_code, dbsize):
    stud_code = str(stud_code)
    result = 0
    count = 0
    with open(dbsize + '_exams' + '.json') as f:
        data = json.load(f)
        for dicts in data:
            if dicts['stud_code'] == stud_code:
                result += int(dicts['grade'])
                count += 1
        result = result/count
        return round(result,2)          
            

def course_average(course_code, dbsize):
    course_code = str(course_code)
    result = 0
    count = 0
    with open(dbsize + '_exams' + '.json') as f:
        data = json.load(f)
        for dicts in data:
            for v in dicts.values():
                if v == course_code:
                    result += int(dicts['grade'])
                    count += 1
        result = result/count
        return round(result,2)  

def teacher_average(teach_code, dbsize):
    teach_code = str(teach_code)
    result = 0
    count = 0
    course_list = []
    with open(dbsize + '_exams' + '.json') as f:
        data_exams = json.load(f)
    with open(dbsize + '_courses' + '.json') as f:
        data_courses = json.load(f)
    course_list = [ dicts['course_code'] for dicts in data_courses if dicts['teach_code'] == teach_code]
    print(course_list)
    for code in course_list:
        for dicts in data_exams:
            if dicts['course_code'] == code:
                result += int(dicts['grade'])
                count +=1
    result = result/count
    return round(result,2)

def top_students(dbsize):
    with open(dbsize + '_students' + '.json') as f:
        data_students = json.load(f)
        top_list = [ dicts['stud_code'] for dicts in data_students if student_average(dicts['stud_code'], dbsize) >= 28 ]
        def sorter(stud_code):
            for name in data_students:
                if name["stud_code"] == stud_code:
                    b = name['stud_name']
                    c = name['stud_surname']
                    a = -(student_average(stud_code,dbsize))
                    return (a,c,b,stud_code)
        top_list = sorted(top_list,key=sorter)
        return top_list

def print_recorded_exams(stud_code, dbsize, fileout):
    result = []
    num = []
    stud_code = str(stud_code)
    count = 0
    width2 = []
    with open(dbsize + '_students' + '.json') as ab:
        data_students = json.load(ab)
        for dicts in data_students:
            for k,v in dicts.items():
                if v == stud_code:
                    stud_surname = dicts['stud_surname']
                    stud_name = dicts['stud_name']
    with open(fileout,'w') as f:
        f.writelines(f"Exams taken by student {stud_surname} {stud_name}, student number {stud_code}"+'\n')
        with open(dbsize + '_exams' + '.json') as o:
            data = json.load(o)
            for dicts in data:
                for k,v in dicts.items():
                    if v == stud_code:
                        course_code = dicts['course_code']
                        date = dicts['date']
                        grade = dicts['grade']
                        with open(dbsize + '_courses' + '.json') as g:
                            data = json.load(g)
                            for dicts in data:
                                for k,v in dicts.items():
                                    if v == course_code: 
                                        course_name = dicts['course_name']
                                        count+=1
                                        num.append(course_name)
                                        num.append(date)
                                        num.append(grade)
                                        width2.append(len(course_name))
            z=max((width2))
            for i,j,k in zip(num[::3],num[1::3],num[2::3]):
                     result.append('{:<{}}\t{}\t{:>}'.format(i,z,j,k) +'\n')
 
            def sot(result):
                result=result.split('\t')
                return (result[-2],result)
            f.writelines(sorted(result,key= sot))
    return count

def print_top_students(dbsize, fileout):
    result2= []
    result3= []
    count = 0
    result=[]
    with open(dbsize + '_students' + '.json') as file:
        data2 = json.load(file)
        for dicts2 in data2:
            c=student_average(dicts2['stud_code'], dbsize)
            if c>=28:
                result.append((dicts2['stud_code'],c))
                result2.append(len(dicts2['stud_surname']+' '+dicts2['stud_name']))
                result3.append((-c, dicts2['stud_surname'] ,dicts2['stud_name']))
    z = max(result2)
    with open(fileout,'w') as de:
        for i in sorted(result3):
            count+=1
            de.writelines('{:<{}}\t{}\n'.format(i[-2] +' '+ i[-1], z, -i[0]))
    return count
"The student <stud_surname> <stud_name>, student number <stud_code>, took on <date> the <course_name> exam with the teacher <teach_surname> <teach_name> with grade <grade>."
def print_exam_record(exam_code, dbsize, fileout):
    with open(dbsize + '_exams' + '.json') as file:
        data = json.load(file)
        for dicts in data:
            if dicts['exam_code'] == exam_code:
                stud_code = dicts['stud_code']
                date = dicts['date']
                course_code = dicts['course_code']
                grade = dicts['grade']
    with open(dbsize + '_students' + '.json') as file:
        data = json.load(file)
        for dicts in data:
            if dicts['stud_code'] == stud_code:
                stud_name = dicts['stud_name']
                stud_surname = dicts['stud_surname']
    with open(dbsize + '_courses' + '.json') as file:
        data = json.load(file)
        for dicts in data:
            if dicts['course_code'] == course_code:
                course_name = dicts['course_name']
                teach_code = dicts['teach_code'] 
    with open(dbsize + '_teachers' + '.json') as file:
        data = json.load(file)
        for dicts in data:
            if dicts['teach_code'] == teach_code:
                teach_name = dicts['teach_name']
                teach_surname = dicts['teach_surname']
    with open(fileout,'w') as file:
        file.writelines("The student {} {}, student number {}, took on {} the {} exam with the teacher {} {} with grade {}.".format(stud_name,stud_surname,stud_code,date,course_name,teach_name,teach_surname,grade))
    return grade
                
    
    
    

