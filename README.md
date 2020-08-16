# final_project Machine Learning

### Airbag and other influences on accident fatalities
#### Description
US data, for 1997-2002, from police-reported car crashes in which there is a harmful event (people or property), and from which at least one vehicle was towed. Data are restricted to front-seat occupants, include only a subset of the variables recorded, and are restricted in other ways also.
#### Format
A data frame with 26217 observations on the following 15 variables:
##### dvcat
* Ordered factor with levels (estimated impact speeds) 1-9km/h, 10-24, 25-39, 40-54, 55+
##### weight
* Observation weights, albeit of uncertain accuracy, designed to account for varying sampling probabilities.
##### dead
* Factor with levels alive dead
##### airbag
* Factor with levels none airbag
##### seatbelt
* Factor with levels none belted
##### frontal
* Numeric vector; 0=non-frontal, 1=frontal impact
##### sex
* Factor with levels f m
##### ageOFocc
* Age of occupant in years
##### yearacc
* Year of accident
##### yearVeh
* Year of model of vehicle; a numeric vector
##### abcat
* Did one or more (driver or passenger) airbag(s) deploy? This factor has levels deploy nodeploy unavail
##### occRole
* Factor with levels driver pass
##### deploy
* Numeric vector: 0 if an airbag was unavailable or did not deploy; 1 if one or more bags deployed.
##### injSeverity
* Numeric vector: 0=none, 1=possible injury, 2=no incapacity, 3=incapacity, 4=killed; 5=unknown, 6=prior death
##### caseid
* Created by pasting together the populations sampling unit, the case number, and the vehicle number.<br> Within each year, use this to uniquely identify the vehicle.
