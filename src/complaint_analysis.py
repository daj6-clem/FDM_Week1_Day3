import os

## try exception finally block
## raise errors
## raise exceptions
# open file
# read file
#   use readline?

# Relative Pathing:
# /../data/complaints.csv

#print("Current working directory:", os.getcwd())
#print(os.path.exists("data/complaints.csv"))

missingVals = 0

#status counts
closedCount = 0
openCount = 0
escalatedCount = 0
reviewCount = 0

#category counts, Fee dispute, service delay, transaction error,
#  online banking, card issue, customer service, fraud claim
accAccess = 0
transDispute = 0
digital = 0
fees = 0
mortgage = 0
servQuality = 0

totalCases = 0

closedByCat = {
    "Account Access": accAccess,
    "Card or Transaction Dispute": transDispute,
    "Digital Banking": digital,
    "Fees": fees,
    "Mortgage Servicing": mortgage,
    "Service Quality": servQuality
}

try:
    with open("../data/complaints.csv") as file:
        next(file)
        #result = file.read()
        #print(result)
        try:
            #file operations
            for line in file:
                fields = line.strip().split(",")
                totalCases += 1

                category = fields[3]
                status = fields[4]

                if status == "Closed":
                    closedByCat[category] = closedByCat.get(category,0) + 1
                

                for field in fields:
                    #print(field)
                    if field == "":
                        missingVals += 1
                    match field:
                        case "Open":
                            openCount += 1
                        case "Closed":
                            closedCount += 1
                        case "Escalated":
                            escalatedCount += 1
                        case "In Review":
                            reviewCount += 1

                        case "Account Access":
                            accAccess += 1
                        case "Card or Transaction Dispute":
                            transDispute += 1
                        case "Digital Banking":
                            digital += 1
                        case "Fees":
                            fees +=1
                        case "Mortgage Servicing":
                            mortgage +=1
                        case "Service Quality":
                            servQuality += 1

            #result = file.read()
            #print(result)
            pass
        finally:
            #file close
            print("Total cases:", totalCases)

            print("Missing fields:", missingVals)

            print("Closed Cases:", closedCount)
            print("Open Cases:", openCount)
            print("Escalated Cases:", escalatedCount)
            print("Cases in Review:", reviewCount)

            print("Account Access:", accAccess)
            print("Card or Transaction Dispute:", transDispute)
            print("Digital Banking:", digital)
            print("Fees:", fees)
            print("Mortgage Servicing:", mortgage)
            print("Service Quality:", servQuality)

            catCounts = {
                "Account Access": accAccess,
                "Card or Transaction Dispute": transDispute,
                "Digital Banking": digital,
                "Fees": fees,
                "Mortgage Servicing": mortgage,
                "Service Quality": servQuality
            }
            largestCat = max(catCounts, key=catCounts.get)
            largestValPercent = 100 * catCounts[largestCat] / (totalCases)
            print(f"{largestCat} is the largest category at {largestValPercent:.2f}% of total cases.")


            print("\nClosed cases by category:")
            for category, count in closedByCat.items():
                print(f"{category}: {count}")
            
            file.close()
except:
    print("Could not find file.")

with open("complaint_analysis_output.csv", "a") as file:
    file.write(f"Total cases: ,{totalCases}\n")

    file.write(f"Missing fields: ,{missingVals}\n")

    file.write(f"Closed Cases: ,{closedCount}\n")
    file.write(f"Open Cases: ,{openCount}\n")
    file.write(f"Escalated Cases: ,{escalatedCount}\n")
    file.write(f"Cases in Review: ,{reviewCount}\n\n")

    file.write(f"Account Access: ,{accAccess}\n")
    file.write(f"Card or Transaction Dispute: ,{transDispute}\n")
    file.write(f"Digital Banking: ,{digital}\n")
    file.write(f"Fees: ,{fees}\n")
    file.write(f"Mortgage Servicing: ,{mortgage}\n")
    file.write(f"Service Quality: ,{servQuality}\n")
    
    file.write(f"{largestCat} is the largest category at {largestValPercent:.2f}% of total cases.\n")


    file.write("\nClosed cases by category:\n")
    for category, count in closedByCat.items():
        file.write(f"{category}:, {count}\n")