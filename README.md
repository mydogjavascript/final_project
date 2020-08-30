# Team JavaScript Crash Data

## Google Slide Presentation Link

### https://docs.google.com/presentation/d/1rCUgGdReLXpcnDJisHFbRMw03b5xDLH4zoAbk-zz0tE/edit?usp=sharing

## Link for the Dashboard Storyboard

### https://docs.google.com/presentation/d/1jLxOb1EkOrz2bPw1YZ-Z6WS_bTuhQcq5VOKu3fQD41U/edit?usp=sharing

## Communication protocol

#### Team JavaScript will communicate through our JavaScript Team channel. We anticipate working collaboratively throughtout the project duration providing support in our strengths and requesting support in our weaknesses.

#### Team JavaScript plans to use class sessions to collaborate along with using office hours and tutoring to guide through the project in its entirety.

## Data Choice

#### Team JavaScript wanted to work with data that was relevent to anyone. Crash data is relevant to any driver, any parent with children who have earned their driver license, and anyone who uses public roadways. This data included factors we had a general interest in to include age and sex of injured individual, airbag deployment, seatbelt usage, and year of vehicle. This data allows us to learn more about crash safety. We are also looking forward to making connections to injury severity and vehicle specifications and driver/passenger attributes.

## Outline of Project

### 1. Determine the scope of the project

        a. Selected data
                i. "Airbag and other influences on accident fatalities"
                ii. Description: US data, for 1997-2002, from police-reported car crashes in which there is a harmful event (people or property), and from which at least one vehicle was towed. Taken from nassCDS with 26,217 observations before data cleanup.

        b. Determined topic of our research
                i. Crash data is relevant to any driver, any parent with
                   children who have earned their driver license, and
                   anyone who uses public roadways. We are also looking
                   forward to making connections to injury severity and
                   vehicle specifications and driver/passenger attributes.

        c. Selected the questions we wanted to answer
                i.  What is the likelihood of fatality in a car
                    accident given a variety of vehicle and passenger
                    factors?

        d. Identify data limitations
                i. There are coonsiderably less data for >40km/h
                   than <40km/h
                ii. Only driver and frontseat passengers are reflected in
                    the data, backseat passenger data was not collected.
                iii. Speed at impact is estimated
                iv. Data is for accidents occuring between 1997-2002
                v. Adjusted data instances where "ultimate outcome" is
                   "dead" but "injury_severity" is listed as "severe". In
                   these instances only, "injury_severity" was amended to
                   match "ultimate outcome" of "dead".

### 2. Review and understand the data

        a. Identify missing data

        b. Identify data that is not helpful for the project
                i. Columns removed include:
                   - 'weight': Value of unknown significance or origin
                   - 'yearacc': Year the accident occurred from 1997-2002
                      and is not relevant to the analysis
                   - 'caseid': Not unique identifiers,
                      numerous indicents assigned to single id's
                   - 'airbag' & 'deploy': Values are duplicated in the
                     'abcat' column

        c. Map the plan for cleaning data
                i. Remove null values
                ii. rename column names for user
                    clarity
                iii. renamed classification values for seatbelt
                     column for clarity
                iv. renamed classification values for frontal impact
                    to (1) and non-frontal impact to (0)

### 3. Data Cleaning

        a. Import data utilizing Pandas

        b. Using Jupyter Notebook, eliminate missing and un-needed data

        c. Transform the data as needed to binary values or binning
                i. Binning utilized for speed
                ii. Binary values used for "frontal" column for impact
                    location

### 4. Feature Engineering and Selection

        a. Feature engineering- there is no need for feature engineering with
           this data set

        b. Feature selection- 'est_impact_kmh',
                        'ultimate_outcome',
                        'airbag_available',
                        'front_impact',
                        'occupant_age',
                        'vehicle_year',
                        'airbag_deployment',
                        'occupant_role',
                        'injury_severity'
                These features were chosen for the relevance of answering
                our research question: "What factors are most relevant in
                prediciting survival rates in a car accident?"

        c. Make predictions on how feature engineering and selection may
           affect data later in the project.
                i. We believe removing "airbag" and "deploy" columns will
                   allow our data to increase in accuracy.   Whether an
                   airbag was installed and whether the airbag deployed
                   was already represented in the "airbag_deployment"
                   column.  Removing this redundancy allowed for more
                   concise learning for the model.
                ii. Removing the columns indicating weight, year of
                    accident and the case id will have no affect on our
                    data outcomes.  Weight is a previously indiciated
                    importance level from the original data collector and
                    has no place in our analysis.  The year of the
                    accident did not seem important because

### 5. Database Creation

        a. Import data utilizing SQLite
                i. Create 2 tables: "Occupants" & "Accidents"

        b. Joined databases using Natural Join

### 6. Machine Learning

        a. Import data utilizing Pandas

        b. Using Jupyter Notebook, choose Machine Learning Model
                i. We chose Random Oversampling as our ML model because we
                   have far less rows of "alive" that we do "dead".
                   Random oversampling manipulates the minority class
                   "dead" to allow for a resampled test and training
                   process.
                ii. Limitations of Random Over Sampling include a possible
                    low precision score for the minority class (dead).
                    The low precision score may indicate an inflated
                    accuracy score.

### 7. Dashboard Creation

        a. Use HTML and Javascript to create the dashboard

        b. Use Python and Flask to develop interactive elements
