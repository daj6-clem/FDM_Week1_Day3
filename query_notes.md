FILTER: For the filter in question 1, I did



SELECT complaint\_id FROM complaint

WHERE status = "OPEN";

The WHERE allows me to filter all complaint IDs for statuses that are "OPEN".









DATE CONDITION: For the date condition in question 6, I did

SELECT complaint\_id FROM complaint

WHERE received\_at BETWEEN ? AND ?;

BETWEEN allows me to find any dates between the two given points, exclusive. 








NULL-HANDLING CHOICE: For handling null values in question 7 "list closed complaints where date\_closed is missing (expected zero) I did

SELECT complaint\_id FROM complaint

LEFT JOIN service\_request ON complaint.customer\_id = service\_request.customer\_id

WHERE closed\_at IS NULL;



IS NULL allows me to select the columns with null values without getting an error.

