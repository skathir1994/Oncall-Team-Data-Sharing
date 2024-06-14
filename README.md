# Oncall-Team-Data-Sharing
Oncall Allocation Process Improvement to Reduce the Validation Timing

Problem Statement: Current work allocation process include fetching the Ticket details from the t.corp.amazon.com with only short ID and VM details, Auditors currently fetch the Ticket details by loading manually having time consumption

Proposed Solutions: To avoid the problem, the below solutions were proposed using python coding.
Step 1: From the ShortId (Sim id). I have created ticket URL.
Step 2: Using the UI Vision browser extension Ticket overview information were scraped
Step 3: Using the python code included ASIN,  marketplace ID, merchant ID details from the overview of the ticket
Step 4: With ASIN & merchant ID pricing rule URL fetched using Macro
Based on the above 4 steps. I have added the 5 extra columns( Ticket URL, ASIN, marketplace ID, merchant ID, Pricing rule URL  ) in the allocation.  

Total Time Saved: 0.4 FTE savings i.e. 3 hrs per day (180 ASINs per day processed on an average)
