Document boundaries, partitions, and expected grain.

1. Use CASE for unresolved age buckets 0-7, 8-30 and 31+ days.
The buckets are inclusive. It is complaint grain, with a column to describe the age group.



2. Use a CTE to identify repeat complainants.
A repeat complainant is one with more than a single count of complaints attached to their customer_id. It is complaint grain, since it has to show multiple complaints and their statuses for each customer that has multiple complaints.



3. Use ROW_NUMBER to select latest status per complaint.
We partition by complaint_status_history.complaint_id in the first half and order by changed_at. This allows us to sort all complaint histories by the date they were changed, so that the latest status will be first. Then we select all statuses that were ranked first. This is complaint grain, as you will have one status (the latest) for each complaint. All complaints with only one status change will appear here.



4. Rank customers by complaint count.
This is customer grain, as you have a single complaint count for each customer. We do not need partitions for this. In the first half of the CTE we count the complaints per customer. In the second half, we rank them using ROW_NUMBER, and order by the number of counted complaints. This gives us a list of customers sorted and ranked from most complaints to least.