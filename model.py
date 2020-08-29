# Import Dependencies for Machine Learning

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy
import sqlite3 as sq
from imblearn.combine import SMOTEENN
from imblearn.under_sampling import ClusterCentroids
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler
from imblearn.ensemble import EasyEnsembleClassifier
from imblearn.metrics import classification_report_imbalanced
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import balanced_accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# Import Initial Dataset

# Import the dataset from Google Drive:
url = ('https://drive.google.com/file/d/1t3Z8Blgy2BPmBB4FqrQkC_jie9IwYuQb/view?usp=sharing')
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
crash_1 = pd.read_csv(path, index_col=0)
crash_1.head()

# Perform Data Cleaning

# Remove columns not needed for this analysis:

# 'weight': Value of unknown significance or origin
# 'yearacc': Year the accident occurred from 1997-2002
# 'caseid': Not individual accident identifiers, numerous indicents assigned to single id's
# 'airbag' & 'deploy': Values are duplicated in the 'abcat' column

crash_2 = crash_1.drop(
    ['weight', 'yearacc', 'caseid', 'airbag', 'deploy'], axis=1)

# Rename the column titles for better clarity:
crash_2.rename(columns={'dvcat': 'est_impact_kmh',
                        'dead': 'ultimate_outcome',
                        'airbag': 'airbag_available',
                        'frontal': 'front_impact',
                        'ageOFocc': 'occupant_age',
                        'yearacc': 'accident_year',
                        'yearVeh': 'vehicle_year',
                        'abcat': 'airbag_deployment',
                        'occRole': 'occupant_role',
                        'injSeverity': 'injury_severity'}, inplace=True)

# Drop the all rows with null values:
crash_3 = crash_2.dropna()

# Rename values:
crash_3['est_impact_kmh'] = crash_3['est_impact_kmh'].replace({
                                                              '1-9km/h': '1-9'})
crash_3['seatbelt'] = crash_3['seatbelt'].replace({'none': 'not_belted'})
crash_3['front_impact'] = crash_3['front_impact'].replace({1: 'yes', 0: 'no'})
crash_3 = crash_3[crash_3['injury_severity'] < 5.0]
crash_3.index.name = 'index'

# Rename the database that has been cleaned:
crash_cleaned = crash_3

# Export Cleaned Data to SQLite Database

crash_cleaned_copy = crash_cleaned.copy()

# Export the accidents data:
accidents_data = crash_cleaned
accidents_data = crash_cleaned.drop(
    ['ultimate_outcome', 'sex', 'occupant_age', 'occupant_role', 'injury_severity'], axis=1)

# Export the occupants data:
occupants_data = crash_cleaned
occupants_data = crash_cleaned.drop(
    ['est_impact_kmh', 'front_impact', 'vehicle_year', 'seatbelt', 'airbag_deployment'], axis=1)

sql_data = 'crash2.sqlite'


# Create connection & push the data:

conn = sq.connect(sql_data)
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS "ACCIDENTS";
CREATE TABLE "ACCIDENTS" (
	"index" INTEGER PRIMARY KEY AUTOINCREMENT,
	"est_impact_kmh" TEXT NOT NULL,
	"front_impact" TEXT NOT NULL,
	"vehicle_year" INTEGER NOT NULL,
	"seatbelt" TEXT NOT NULL,
	"airbag_deployment" TEXT NOT NULL
);

DROP TABLE IF EXISTS "OCCUPANTS";
CREATE TABLE "OCCUPANTS" (
	"index" INTEGER PRIMARY KEY AUTOINCREMENT,
	"ultimate_outcome" TEXT NOT NULL,
	"sex" INTEGER NOT NULL,
	"occupant_age" TEXT NOT NULL,
	"occupant_role" TEXT NOT NULL,
	"injury_severity" INTEGER NOT NULL
);

''')
# conn.commit()
accidents_data.to_sql("ACCIDENTS", conn, if_exists='append', index=True)
# conn.commit()
occupants_data.to_sql("OCCUPANTS", conn, if_exists='append', index=True)

conn.commit()
conn.close()

# Reflect the Tables into SQLAlchemy ORM
engine = create_engine("sqlite:///crash2.sqlite")

# Reflect an existing database into a new model:
Base = automap_base()

# Reflect the tables:
Base.prepare(engine, reflect=True)

# Save reference to the combined table:
Crash = Base.classes.CRASH_COMBINED2

# Create our session (link) from Python to the DB:
session = Session(engine)

# Import the Combined Databases Back to Python

# Perform a query to retrieve the data from the CRASH_COMBINED2 table:
results = []
results = session.query(Crash.occupant_role,
                        Crash.sex,
                        Crash.occupant_age,
                        Crash.ultimate_outcome,
                        Crash.injury_severity,
                        Crash.vehicle_year,
                        Crash.est_impact_kmh,
                        Crash.airbag_deployment,
                        Crash.front_impact,
                        Crash.seatbelt).all()

# Save the query results as a Pandas DataFrame
crash_4 = pd.DataFrame(results, columns=['occupant_role',
                                         'sex',
                                         'occupant_age',
                                         'ultimate_outcome',
                                         'injury_severity',
                                         'seatbelt',
                                         'est_impact_kmh',
                                         'airbag_deployment',
                                         'vehicle_year',
                                         'front_impact', ])

# Conduct Integer Encoding to Transform Text to Numbers

le = LabelEncoder()

crash_5 = crash_4.copy()
crash_5['occupant_role'] = le.fit_transform(crash_5['occupant_role'])
crash_5['sex'] = le.fit_transform(crash_5['sex'])
crash_5['ultimate_outcome'] = le.fit_transform(crash_5['ultimate_outcome'])
crash_5['seatbelt'] = le.fit_transform(crash_5['seatbelt'])
crash_5['est_impact_kmh'] = le.fit_transform(crash_5['est_impact_kmh'])
crash_5['airbag_deployment'] = le.fit_transform(crash_5['airbag_deployment'])
crash_5['front_impact'] = le.fit_transform(crash_5['front_impact'])

# Split the Data into Training & Testing Sets

# Separate the features (X) from the target (y):
y = crash_5['ultimate_outcome']
X = crash_5.drop(columns='ultimate_outcome')

# Split data into training & testing:
X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=1, stratify=y)
X_train.shape

# Resample the training data with the RandomOversampler:
ROS = RandomOverSampler(random_state=1)
X_resampled, y_resampled = ROS.fit_resample(X_train, y_train)

# Train the Logistic Regression model using the resampled data:
ROS_model = LogisticRegression(solver='lbfgs', random_state=1)
ROS_model.fit(X_resampled, y_resampled)

# Calculate the balanced accuracy score:
ROS_pred = ROS_model.predict(X_test)
balanced_accuracy_score(y_test, ROS_pred)
print("Random Oversampler\naccuracy is",
      balanced_accuracy_score(y_test, ROS_pred)*100)

# Print the imbalanced classification report:
print(classification_report_imbalanced(y_test, ROS_pred))
