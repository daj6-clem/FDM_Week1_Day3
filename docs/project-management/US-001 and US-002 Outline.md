US-001: As a consultant, I want to understand the complaint-resolution business problem so that I can explain the users, pain points, constraints, and success measures

US-002: As a business analyst, I want to define complaint-intake stories so that the team can implement against clear acceptance criteria

TO DO:

- Create a backlog for both stories

- [https://danielajonescpsc.atlassian.net/?continue=https%3A%2F%2Fdanielajonescpsc.atlassian.net%2Fwelcome%2Fsoftware%3FprojectId%3D10000&atlOrigin=eyJpIjoiYjVkMmE2MGYzYmIzNGJmYTk0NzFkMjRiNWJlODZmNDEiLCJwIjoiamlyYS1zb2Z0d2FyZSJ9](https://danielajonescpsc.atlassian.net/?continue=https%3A%2F%2Fdanielajonescpsc.atlassian.net%2Fwelcome%2Fsoftware%3FprojectId%3D10000&atlOrigin=eyJpIjoiYjVkMmE2MGYzYmIzNGJmYTk0NzFkMjRiNWJlODZmNDEiLCJwIjoiamlyYS1zb2Z0d2FyZSJ9)

- 

Story 1: Define Complaint-Resolution Business Problem

- Users:

  - Complaint Analyst

  - Supervisor/Reviewer

  - Customer

- Pain Points:

  - Relevant policy or procedure is spread across systems and documents

  - The handling of customer complaints is difficult to audit

  - The handling of customer complaints is slow

  - The handling of customer complaints is inconsistent

  - Complaint handling depends on repeated manual checks

  - Complaint handling relies on parsing through relevant and irrelevant information

- Constraints

  - The Agent cannot make decisions

  - The agent can only reference the email, customer information, and approved policy content

  - The customer does not directly operate or interface with the Agent

  - The Agent must not change Structured Data records 

  - The Agent does not replace SQL, RAG, or the human reviewer

  - The Agent does not close tickets or act alone

- Success Measures

  - Agent will classify issues with confidence

  - Deterministically identify and gather exact customer and complaint facts directly through the email and SQL databases

  - RAG for parsing approved policy content

  - Controlled investigation workflow will organize inputs, show sources, and draft a recommendation

  - Separate verified facts from retrieved policy evidence, system generated analysis, and human decisions

  - Reviewer will be able to understand, challenge, and/or approve the proposed outcome

  - Agent will flag the case when insufficient information is presented

  - An audit trail will be created and updated with every step in the process

Story 2: Define Complaint-Intake Stories

- Define complaint-intake stories

- Clear acceptance criteria

1. As a complaint analyst, I want the AI Agent to be able to determine whether something is a complaint, so that irrelevant information is ignored.

   1. Given a field of text, AI Agent will determine whether or not a complaint is present

   2. If a complaint is present, the AI will open a complaint ticket

   3. If a complaint is not present, the AI will ignore the information

2. As a complaint analyst, I want the AI Agent to ingest complaints from phone transcripts, so that customer issues can be investigated from phone calls and voicemails.

   4. Given a phone complaint, AI Agent will identify and catalog all relevant information

   5. Agent will catalog customer narrative

   6. Agent will catalog customer information

3. As a complain analyst, I want the AI Agent to ingest complaints from web requests, so that customer issues can be investigated from messages through our website.

   7. Given a web complaint, AI agent will identify and catalog all relevant information

   8. Agent will catalog customer narrative

   9. Agent will catalog customer information

4. As a complaint analyst, I want the AI Agent to ingest complaints from emails, so that customer issues can be investigated from my inbox.

   10. Given a complaint email, AI agent will identify and catalog all relevant information

   11. Agent will catalog customer narrative

   12. Agent will catalog customer information

5. As a complaint analyst, I want the AI Agent to ingest complaints from different branches, so that customer issues can be investigated more effectively.

   13. Given a branch complaint, AI agent will identify and catalog all relevant information

   14. Agent will catalog customer narrative

   15. Agent will catalog customer information

6. As a complaint analyst, I want the AI Agent to be able to retrieve customer information from structured data, so that relevant information can be gathered.

   16. Given a complaint ticket, AI agent will be able to access SQL databases to search for customer information

   17. Agent will gather all relevant information on the customer in question

   18. Agent will not gather any information from other customers

7. As a complaint analyst, I want the AI Agent to be able to retrieve policy information, so that relevant policies can be applied.

   19. Given a complaint ticket, AI agent will be able to use RAGs to search for policy information

   20. Agent will gather all relevant policy information for the complaint in question

   21. Agent will not gather any irrelevant policy information

8. As a complaint analyst, I want the AI Agent to be able to flag missing information, so that I can review it.

   22. AI Agent will check off each field of customer information as it goes

   23. Whatever unchecked fields remain will be flagged as missing

   24. AI Agent will record this in the audit logs

9. As a complaint analyst, I want the AI Agent to be able to summarize the information, so that I can review it.

   25. AI Agent will compile policy and customer information

   26. AI Agent will write a written summary of the information on hand

10. As a complaint analyst, I want the AI Agent to be able to use the compiled information to suggest next actions, so that I can make a judgement call.

    27. AI Agent will reference the written summary and policy information to provide next steps

    28. AI Agent will inform the analyst if it does not have enough information

    29. AI Agent will record this in the audit logs

11. As a complaint analyst, I want the AI Agent to be able to categorize the urgency of complaints, so they can be escalated to a supervisor.

    30. AI Agent will compare the customer and policy information to urgency rules to present the urgency of each case

12. As a complaint analyst, I want the AI Agent to be able to escalate summaries to a supervisor, so that they can review sensitive, uncertain, high risk, or compensatory information before the action is taken.

    31. AI Agent will route the case to a supervisor if the urgency reaches a certain threshold

    32. AI Agent will record this in its audit logs

13. As a complaint analyst, I want the AI Agent to record each step in the complaint analysis process in its audit logs, so that they can be reviewed by my supervisor as necessary

    33. AI Agent will stop at each step of the analysis

    34. AI Agent will record previous action in the logs

    35. AI Agent will record analyst, supervisor, and customer information in the logs
