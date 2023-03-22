# PyCity Schools Analysis


As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (
585 per student).

As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).

As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school.


# Dependencies and Setup
import pandas as pd
import numpy as np


# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name"])

# Make a copy of the school_data and school_data_complete dataframe for analysis
df_student_data = student_data.copy()
df_school_data = school_data.copy()
df_school_data_complete = school_data_complete.copy()

df_school_data
df_school_data_complete.head()
Student ID	student_name	gender	grade	school_name	reading_score	math_score	School ID	type	size	budget
0	0	Paul Bradley	M	9th	Huang High School	66	79	0	District	2917	1910635
1	1	Victor Smith	M	12th	Huang High School	94	61	0	District	2917	1910635
2	2	Kevin Rodriguez	M	12th	Huang High School	90	60	0	District	2917	1910635
3	3	Dr. Richard Scott	M	12th	Huang High School	67	58	0	District	2917	1910635
4	4	Bonnie Ray	F	9th	Huang High School	97	84	0	District	2917	1910635


# District Summary
Calculate the total number of schools

Calculate the total number of students

Calculate the total budget

Calculate the average math score

Calculate the average reading score

Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2

Calculate the percentage of students with a passing math score (70 or greater)

Calculate the percentage of students with a passing reading score (70 or greater)

Create a dataframe to hold the above results

#  District Summary
 
# Calculate the total number of schools in the school district: this is a combination of district public and charter schools
#df_schools_type = df_school_data['type'].unique()
df_total_number_schools = df_school_data['type'].count()


#  Calculate the total number of students
total_number_students = df_school_data['size'].sum()


#  Calculate the total budget:

total_school_budget = df_school_data['budget'].sum()


#  Calculate the average math score: 
total_avg_math_scores = df_school_data_complete['math_score'].mean()


# Calculate the average reading score:
total_avg_reading_scores = df_school_data_complete['reading_score'].mean()


#  Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2 
overall_passing_rate = (total_avg_math_scores + total_avg_reading_scores)/2


#  Calculate the percentage of students with a passing math score (70 or greater)
pass_math = df_school_data_complete[df_school_data_complete['math_score'] >= 70]
# Count the number of students passing math 
passing_math_count = pass_math['Student ID'].count()
# Calculate average students passing math
avg_passing_math = (passing_math_count/total_number_students)*100


# Calculate the percentage of students with a passing reading score (70 or greater)
pass_reading = df_school_data_complete[df_school_data_complete['reading_score'] >= 70]
#  Count the number of students passing reading
passing_reading_count = pass_reading['Student ID'].count()
#  Calculate average students passing reading
avg_passing_reading = (passing_reading_count/total_number_students)*100


#  Calculate the overall passing
overall_passing = (avg_passing_math + avg_passing_reading)/2

# Create a dataframe to hold the above results 
#  First create a dictionary of lists 
df = {'Total Schools': [df_total_number_schools],
     'Total Students': [total_number_students],
     'Total Budget': [total_school_budget],
     'Average Math Score':[total_avg_math_scores],
     'Average Reading Score':[total_avg_reading_scores],
     '%Passing Math': [avg_passing_math],
     '%Passing Reading': [avg_passing_reading],
     '%Overall Passing Rate': [overall_passing]}

df


#  Then, create a dataframe to hold the above results
district_summary = pd.DataFrame(df)

# Organize columns
district_summary = district_summary[['Total Schools',
                                     'Total Students',
                                     'Total Budget',
                                     'Average Math Score',
                                     'Average Reading Score',
                                     '%Passing Math',
                                     '%Passing Reading',
                                     '%Overall Passing Rate' ]]


district_summary
Total Schools	Total Students	Total Budget	Average Math Score	Average Reading Score	%Passing Math	%Passing Reading	%Overall Passing Rate
0	15	39170	24649428	78.985371	81.87784	74.980853	85.805463	80.393158


# School Summary
Create an overview table that summarizes key metrics about each school, including:

School Name
School Type
Total Students
Total School Budget
Per Student Budget
Average Math Score
Average Reading Score
% Passing Math
% Passing Reading
Overall Passing Rate (Average of the above two)
Create a dataframe to hold the above results

# Top Performing Schools (By Passing Rate)
Sort and display the top five schools in overall passing rate

#  Create an overview table that summarizes key metrics about each school


#  Calculate budget per student and add a column (series) -'Per Student Budget'  to the output
df_school_data['Per Student Budget'] = df_school_data['budget']/df_school_data['size']
Per_Student_Budget = df_school_data['Per Student Budget']
#df_school_data['Per Student Budget'] = df_school_data['Per Student Budget'].astype(float).map('${:,.2f}'.format)

total_budget = df_school_data['budget']
#df_school_data['budget'] = df_school_data['budget'].astype(float).map('${:,.2f}'.format)


#  Calculate the average math and reading scores for each school
avg_passing_math_reading_ps = df_student_data.groupby(['school_name'])['reading_score','math_score'].mean().reset_index()
avg_passing_math_reading_ps


#  Merge the average_passing_math and average_passing_reading to the school dataframe
df_school_data = df_school_data.merge(avg_passing_math_reading_ps, on='school_name', how='outer')
df_school_data

#  Delete School ID
del df_school_data['School ID']


#  Calculate the number of students with passing reading score (70 or greater)
pass_math_metric = df_student_data[df_student_data['math_score'] >= 70]
# Group the total score by school_name 
passing_math_total_score = pass_math_metric.groupby(['school_name'])['math_score'].count().reset_index()


# Calculate the number of students with passing reading score (70 or greater)
pass_reading_metric = student_data[student_data['reading_score'] >= 70]
# Group the total score by school_name
passing_reading_total_score = pass_reading_metric.groupby(['school_name'])['reading_score'].count().reset_index()


#  Merge the passing_math_score and passing_reading_score, and rename score to total accordingly
passing_total_score = passing_math_total_score.merge(passing_reading_total_score,on='school_name',how='inner')
# Rename score to total accordingly
passing_score_renamed = passing_total_score.rename(columns = {'math_score':'math_total', 'reading_score':'reading_total' })


#  Merge passing count to school data dataframe
df_school_overall = df_school_data.merge(passing_score_renamed,on='school_name',how='outer')


# Calculate the % Passing math 
df_school_overall['% Passing Math'] = (df_school_overall['math_total']/df_school_overall['size'])*100
passing_math = df_school_overall['% Passing Math']

#  Calculate the % Passing reading 
df_school_overall['% Passing Reading'] = (df_school_overall['reading_total']/df_school_overall['size'])*100
passing_reading = df_school_overall['% Passing Reading']


#  Delete math_total and reading_total from the dataframe
del df_school_overall['math_total']
del df_school_overall['reading_total']

#  Set new index to school_name
df_school_overall = df_school_overall.set_index('school_name')
df_school_overall.index.name = None

# Calculate the % Overall Passing Rate (Average of % Passing math and reading) and add Overall Passing Rate series to the dataframe
df_school_overall['% Overall Passing Rate'] = (df_school_overall['% Passing Math'] + df_school_overall['% Passing Reading'])/2
overall_passing = df_school_overall['% Overall Passing Rate']

# Rename math_score and reading_score to Average... accordingly
renamed_df_school_overall= df_school_overall.rename(columns = {'school_name':'','type':'School Type','size':'Total Students','budget':'Total School Budget','math_score':'Average Math Score', 'reading_score':'Average Reading Score' })


#df_school_data['Per Student Budget'] = df_school_data['Per Student Budget'].astype(float).map('${:,.2f}'.format)
#df_school_data['budget'] = df_school_data['budget'].astype(float).map('${:,.2f}'.format)

#  Create a dataframe to hold the above results 
#  First create a dictionary of lists 
dfs = {'School Type': [type],
     'Per Student Budget':[Per_Student_Budget],
     'Total School Budget':[total_budget],
     'Average Math Score':[avg_passing_math],
     'Average Reading Score':[avg_passing_reading],
     '%Passing Math': [passing_math],
     '%Passing Reading': [passing_reading],
     '%Overall Passing Rate': [overall_passing]}

dfs



#  Then, create a dataframe to hold the above results
dfs_s = pd.DataFrame(dfs, index = ['school_name'])


#  Organize columns
dfs_s = dfs_s[['School Type',
               'Per Student Budget',
               'Total School Budget',
               'Average Math Score',
               'Average Reading Score',
               '%Passing Math',
               '%Passing Reading',
               '%Overall Passing Rate' ]]


#  Sort dataframe to display top performing schools
df_Top_Performing_Schools_By_Passsing_Rate = renamed_df_school_overall.sort_values(by=['% Overall Passing Rate'],ascending=False).head(5)
df_Top_Performing_Schools_By_Passsing_Rate
School Type	Total Students	Total School Budget	Per Student Budget	Average Reading Score	Average Math Score	% Passing Math	% Passing Reading	% Overall Passing Rate
Cabrera High School	Charter	1858	1081356	582.0	83.975780	83.061895	94.133477	97.039828	95.586652
Thomas High School	Charter	1635	1043130	638.0	83.848930	83.418349	93.272171	97.308869	95.290520
Pena High School	Charter	962	585858	609.0	84.044699	83.839917	94.594595	95.945946	95.270270
Griffin High School	Charter	1468	917500	625.0	83.816757	83.351499	93.392371	97.138965	95.265668
Wilson High School	Charter	2283	1319574	578.0	83.989488	83.274201	93.867718	96.539641	95.203679
Bottom Performing Schools (By Passing Rate)
Sort and display the five worst-performing schools

#  Sort dataframe to display first worst performing schools
df_Bottom_Performing_Schools_By_Passsing_Rate = renamed_df_school_overall.sort_values(by=['% Overall Passing Rate']).head(5)
df_Bottom_Performing_Schools_By_Passsing_Rate
School Type	Total Students	Total School Budget	Per Student Budget	Average Reading Score	Average Math Score	% Passing Math	% Passing Reading	% Overall Passing Rate
Rodriguez High School	District	3999	2547363	637.0	80.744686	76.842711	66.366592	80.220055	73.293323
Figueroa High School	District	2949	1884411	639.0	81.158020	76.711767	65.988471	80.739234	73.363852
Huang High School	District	2917	1910635	655.0	81.182722	76.629414	65.683922	81.316421	73.500171
Johnson High School	District	4761	3094650	650.0	80.966394	77.072464	66.057551	81.222432	73.639992
Ford High School	District	2739	1763916	644.0	80.746258	77.102592	68.309602	79.299014	73.804308
Math Scores by Grade
Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.

Create a pandas series for each grade. Hint: use a conditional statement.

Group each series by school

Combine the series into a dataframe

Optional: give the displayed data cleaner formatting

#  Group math scores by grade using pivot table
df_math_score_grade =pd.pivot_table(df_student_data,values=['math_score'],index=['school_name'],columns=['grade'])


# Arrange and reindex axis by grade
df_math_score_grade = df_math_score_grade.reindex(labels=['9th',
                                                                   '10th',
                                                                   '11th',
                                                                   '12th'],axis=1,level=1)
df_math_score_grade
math_score
grade	9th	10th	11th	12th
school_name				
Bailey High School	77.083676	76.996772	77.515588	76.492218
Cabrera High School	83.094697	83.154506	82.765560	83.277487
Figueroa High School	76.403037	76.539974	76.884344	77.151369
Ford High School	77.361345	77.672316	76.918058	76.179963
Griffin High School	82.044010	84.229064	83.842105	83.356164
Hernandez High School	77.438495	77.337408	77.136029	77.186567
Holden High School	83.787402	83.429825	85.000000	82.855422
Huang High School	77.027251	75.908735	76.446602	77.225641
Johnson High School	77.187857	76.691117	77.491653	76.863248
Pena High School	83.625455	83.372000	84.328125	84.121547
Rodriguez High School	76.859966	76.612500	76.395626	77.690748
Shelton High School	83.420755	82.917411	83.383495	83.778976
Thomas High School	83.590022	83.087886	83.498795	83.497041
Wilson High School	83.085578	83.724422	83.195326	83.035794
Wright High School	83.264706	84.010288	83.836782	83.644986
Reading Score by Grade
Perform the same operations as above for reading scores
#  Group reading scores by grade using pivot table
df_reading_score_grade =pd.pivot_table(df_student_data,values=['reading_score'],index=['school_name'],columns=['grade'])

#  Arrange and reindex axis by grade
df_reading_score_grade = df_reading_score_grade.reindex(labels=['9th',
                                                                   '10th',
                                                                   '11th',
                                                                   '12th'],axis=1,level=1)
df_reading_score_grade
reading_score
grade	9th	10th	11th	12th
school_name				
Bailey High School	81.303155	80.907183	80.945643	80.912451
Cabrera High School	83.676136	84.253219	83.788382	84.287958
Figueroa High School	81.198598	81.408912	80.640339	81.384863
Ford High School	80.632653	81.262712	80.403642	80.662338
Griffin High School	83.369193	83.706897	84.288089	84.013699
Hernandez High School	80.866860	80.660147	81.396140	80.857143
Holden High School	83.677165	83.324561	83.815534	84.698795
Huang High School	81.290284	81.512386	81.417476	80.305983
Johnson High School	81.260714	80.773431	80.616027	81.227564
Pena High School	83.807273	83.612000	84.335938	84.591160
Rodriguez High School	80.993127	80.629808	80.864811	80.376426
Shelton High School	84.122642	83.441964	84.373786	82.781671
Thomas High School	83.728850	84.254157	83.585542	83.831361
Wilson High School	83.939778	84.021452	83.764608	84.317673
Wright High School	83.833333	83.812757	84.156322	84.073171
Scores by School Spending
Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
Average Math Score
Average Reading Score
% Passing Math
% Passing Reading
Overall Passing Rate (Average of the above two)
# Create bins to hold values
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]
#  Make a copy of df_school_overall (a comprehensive dataframe with school dataframe and other computations) 
df_scores_by_school_spending = renamed_df_school_overall.copy()


# Slice the data, put in bins and place the data into a new column 
df_scores_by_school_spending['Spending Ranges (Per Student)'] = pd.cut(df_scores_by_school_spending['Per Student Budget'], spending_bins, labels=group_names)

#  Creat a group based off of the bins and get the average of each column within the GroupBy object
df_scores_by_school_spending.groupby(['Spending Ranges (Per Student)'])['Average Math Score', 
                                                                        'Average Reading Score',
                                                                        '% Passing Math',
                                                                        '% Passing Reading',
                                                                        '% Overall Passing Rate'].mean()
Average Math Score	Average Reading Score	% Passing Math	% Passing Reading	% Overall Passing Rate
Spending Ranges (Per Student)					
<$585	83.455399	83.933814	93.460096	96.610877	95.035486
$585-615	83.599686	83.885211	94.230858	95.900287	95.065572
$615-645	79.079225	81.891436	75.668212	86.106569	80.887391
$645-675	76.997210	81.027843	66.164813	81.133951	73.649382
Scores by School Size
Perform the same operations as above, based on school size.
#  Create bins to hold values
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
# Make a copy of df_school_overall (a comprehensive dataframe with school dataframe and other computations) 
df_scores_by_school_size = renamed_df_school_overall.copy()


#  Slice the data, put in bins and place the data into a new column 
df_scores_by_school_size['Total Students'] = pd.cut(df_scores_by_school_size['Total Students'], size_bins, labels=group_names)


# Creat a group based off of the bins and get the average of each column within the GroupBy object
df_scores_by_school_size.groupby(['Total Students'])['Average Math Score','Average Reading Score','% Passing Math','% Passing Reading','% Overall Passing Rate'].mean() 
Average Math Score	Average Reading Score	% Passing Math	% Passing Reading	% Overall Passing Rate
Total Students					
Small (<1000)	83.821598	83.929843	93.550225	96.099437	94.824831
Medium (1000-2000)	83.374684	83.864438	93.599695	96.790680	95.195187
Large (2000-5000)	77.746417	81.344493	69.963361	82.766634	76.364998
Scores by School Type
Perform the same operations as above, based on school type.
#  Make a copy of df_school_overall (a comprehensive dataframe with school dataframe and other computations) 
df_scores_by_school_type = renamed_df_school_overall.copy()


# Groupby School Type 
df_scores_by_school_type = df_scores_by_school_type.groupby(['School Type'])['Average Math Score', 'Average Reading Score','% Passing Math','% Passing Reading','% Overall Passing Rate'].mean().reset_index()


# Set new index to School Type
df_scores_by_school_type= df_scores_by_school_type.set_index('School Type')


df_scores_by_school_type  
Average Math Score	Average Reading Score	% Passing Math	% Passing Reading	% Overall Passing Rate
School Type					
Charter	83.473852	83.896421	93.620830	96.586489	95.103660
District	76.956733	80.966636	66.548453	80.799062	73.673757


# Observable trends based on the data.
Based on the provided data, I observed the following trends while analysing the data for PyCitySchools.

Scores by School Spending: As the spending range per student increases, the percentage overall passing rate decreases. Schools with smaller budget have relatively higher average Math and reading scores, and higher overall passing rate.

Scores by School Size: Small to medium school size performed better than large school size. As the school size increases, the percentage overall passing rate decreases or drops. This trend is observed also in the average math and reading score, as well as the percentage passing math and reading.

Scores by School Type: The performance of charter schools within all the criteria are better than public district schools. The percentage passing Math, Passing Reading and overall passing rate are significant higher in Charter schools compared to District schools

In conclusion: Charter schools with small size and small budget per student performed much better than District schools with higher budget per student.
