from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class Parser:
    def __init__(self):
        self.numberOfDays = 0 # Count number of days passed
        
        self.startDate = datetime.today()
        self.endDate = datetime.today()
        
        self.fileTypeDict = {} # Contains file extension - file type information
        self.initializeFileType()

        self.fileCountDict = {} # Contains quantity per file extension
        self.initializeFileCount()

        self.catByteDict = {} # Contains bytes transferred per file category
        self.initializeCatByte()

        self.nameDict = {} # Name dictionary
        self.nameList = [] # Name list
        self.sizeDict = {} # Count dictionary
        self.nameSizeDict = {} # Name:Size dictionary.

        self.sizeList = [] # For question 12 values.

        self.uniqueBytes = 0

        self.month_counts = Counter()

        self.objectTimeDict = {} # Object names : [list of time stamps]
        self.interRefTimes = [] # Inter Ref Times Final question

    def initializeCatByte(self):
        self.catByteDict["HTML"] = 0
        self.catByteDict["Images"] = 0
        self.catByteDict["Sound"] = 0
        self.catByteDict["Video"] = 0
        self.catByteDict["Formatted"] = 0
        self.catByteDict["Dynamic"] = 0
        self.catByteDict["Others"] = 0

    def initializeFileCount(self):
        self.fileCountDict["HTML"] = 0
        self.fileCountDict["Images"] = 0
        self.fileCountDict["Sound"] = 0
        self.fileCountDict["Video"] = 0
        self.fileCountDict["Formatted"] = 0
        self.fileCountDict["Dynamic"] = 0
        self.fileCountDict["Others"] = 0
        
    def initializeFileType(self):  # Define file types for each file
        self.fileTypeDict["html"] = "HTML"
        self.fileTypeDict["htm"] = "HTML"
        self.fileTypeDict["shtml"] = "HTML"
        self.fileTypeDict["map"] = "HTML"

        self.fileTypeDict["gif"] = "Images"
        self.fileTypeDict["jpeg"] = "Images"
        self.fileTypeDict["jpg"] = "Images"
        self.fileTypeDict["xbm"] = "Images"
        self.fileTypeDict["bmp"] = "Images"
        self.fileTypeDict["rgb"] = "Images"
        self.fileTypeDict["xpm"] = "Images"

        self.fileTypeDict["au"] = "Sound"
        self.fileTypeDict["snd"] = "Sound"
        self.fileTypeDict["wav"] = "Sound"
        self.fileTypeDict["mid"] = "Sound"
        self.fileTypeDict["midi"] = "Sound"
        self.fileTypeDict["lha"] = "Sound"
        self.fileTypeDict["aif"] = "Sound"
        self.fileTypeDict["aiff"] = "Sound"

        self.fileTypeDict["mov"] = "Video"
        self.fileTypeDict["movie"] = "Video"
        self.fileTypeDict["avi"] = "Video"
        self.fileTypeDict["qt"] = "Video"
        self.fileTypeDict["mpeg"] = "Video"
        self.fileTypeDict["mpg"] = "Video"

        self.fileTypeDict["ps"] = "Formatted"
        self.fileTypeDict["eps"] = "Formatted"
        self.fileTypeDict["doc"] = "Formatted"
        self.fileTypeDict["dvi"] = "Formatted"
        self.fileTypeDict["txt"] = "Formatted"

        self.fileTypeDict["cgi"] = "Dynamic"
        self.fileTypeDict["pl"] = "Dynamic"
        self.fileTypeDict["cgi-bin"] = "Dynamic"

    def parse(self, logFile):  # Read each line from the log and process output
        index = 0

        total_bytes = 0 # Function variables for storing insights.
        successfulResp = 0
        notModifiedResp = 0
        foundResp = 0
        unsuccessfulResp = 0

        localCount = 0
        remoteCount = 0

        localBytes = 0
        remoteBytes = 0

        print("Reading log file...")
        for line in logFile:
            elements = line.split()

            # Skip to the next line if this line has an empty string
            if line is '':
                continue

            # Skip to the next line if this line contains not equal to 9 - 11 elements
            if not (9 <= len(elements) <= 11):
                continue

            # Corrects a record with a single "-"
            if (len(elements) == 9 and elements[2] != '-'):
                elements.insert(2, '-')

            sourceAddress = elements[0]
            timeStr = elements[3].replace('[', '')
            requestMethod = elements[5]
            requestFileName = elements[6].replace('"', '')
            responseCode = elements[len(elements) - 2]
            replySizeInBytes = elements[len(elements) - 1]

            ################## From Here, implement your parser ##################
            # Inside the for loop, do simple variable assignments & modifications
            # Please do not add for loop/s
            # Only the successful requests should be used from question 5 onward

            """ Replaced by case matching block
            if responseCode == "200": # If the request is a successful request, accrue total bytes.
                try:
                    total_bytes += int(replySizeInBytes) # replySizeInBytes is a string slice.
                except ValueError:
                    print(f"Error: '{replySizeInBytes}' could not be converted to an integer.")
            """

            if responseCode == "200":
                match sourceAddress:
                    case "local":
                        localCount += 1
                        localBytes += int(replySizeInBytes)
                    case "remote":
                        remoteCount += 1
                        remoteBytes += int(replySizeInBytes)
                    case _:
                        print("Host Error")

            match responseCode: # Look at the response code
                case "200": # If it's a successfull response then
                    try:    # Increment total (successful) byte count, increment sucessful quantity count
                        total_bytes += int(replySizeInBytes) # replySizeInBytes is a string slice.
                        successfulResp += 1

                        fileType = self.getFileType(requestFileName)
                        self.fileCountDict[fileType] += 1

                        self.catByteDict[fileType] += int(replySizeInBytes)

                        if requestFileName not in self.nameDict: # This loop builds a dictionary of names:occurences
                            self.nameDict[requestFileName] = 1 # Add the file name to the name dictionary.
                            self.nameSizeDict[requestFileName] = replySizeInBytes
                            self.sizeList.append(replySizeInBytes)
                        else:
                            self.nameDict[requestFileName] += 1 # If its already been added, increment the count.

                        if requestFileName not in self.sizeDict:
                            self.sizeDict[requestFileName] = int(replySizeInBytes)
                        else:
                            continue
                        
                        timestamp = datetime.strptime(timeStr, '%d/%b/%Y:%H:%M:%S')
                        if requestFileName not in self.objectTimeDict:
                            self.objectTimeDict[requestFileName] = [timestamp]
                        else:
                            self.objectTimeDict[requestFileName].append(timestamp)

                    except ValueError:
                        print(f"Error: '{replySizeInBytes}' could not be converted to an integer.")
                    #print("Successful")
                case "302":
                    foundResp += 1
                    #print("Found")
                case "304":
                    notModifiedResp += 1
                    #print("Not Modified")
                case _: # Wildcard pattern for any other status
                    unsuccessfulResp += 1
                    #print("Unsuccessful")
            
            # Prints assigned elements. Please comment print statement.
            #print('{0} , {1} , {2} , {3} , {4} , {5} '.format(sourceAddress,timeStr,requestMethod,requestFileName,responseCode, replySizeInBytes),end="")
            #print('{0}'.format(responseCode),end="") # Test print statements for attribute tests.

            # Assigns & prints format type. Please comment print statement.
            #fileType = self.getFileType(requestFileName)

            #print('Name={0}'.format(requestFileName))
            #print('Type={0}'.format(fileType))
            #print('Type={0}'.format(self.fileTypeDict[fileType]))

            # Q1: Write a condition to identify a start date and an end date.
            self.startDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
            self.endDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")

            try:
                dt = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
                month_name = dt.strftime("%B")
                self.month_counts[month_name] += 1
            except Exception:
                continue
            
        # Outside the for loop, generate statistics output
        print("\n")

        print("Generating statistics output...")
        print(f"Total Bytes: {total_bytes}")
        print(f"Total Successful: {successfulResp}")
        print(f"Total Not Modified: {notModifiedResp}")
        print(f"Total Found: {foundResp}")
        print(f"Total Unsuccessful: {unsuccessfulResp}")
        print(f"Local Hosts: {localCount}")
        print(f"Remote Hosts: {remoteCount}")
        print(f"Local Bytes: {localBytes}")
        print(f"Remote Bytes: {remoteBytes}")
        print("Completed the statistics output.\n")

        print("Printing the keys in the fileCountDict...\n")

        for key in self.fileCountDict: # For all keys in the fileCountDict
                value = self.fileCountDict[key] 
                print('Key={0}:Value={1}'.format(key, value)) # Print the key and value

        print("\n")

        for key in self.catByteDict: # For all categories in the categoryByteDictionary
            value = self.catByteDict[key]
            print('Category={0}:Bytes={1}'.format(key, value)) # Print the category and byte count

        # Prints all of the file names in the nameDictionary. Contains every fileName:Frequency
        #for name in self.nameDict: # For each name
        #    freq = self.nameDict[name]
        #    print('File Name={0}:Frequency={1}'.format(name, freq)) # Print the category and byte count

        #for name in self.nameSizeDict: # Test print for nameSizeDictionary creation
        #    size = self.nameSizeDict[name]
        #    print('Name={0}:Size={1}'.format(name, size))

        print("\n")
        print("len(nameDict)={0}".format(len(self.nameDict)))

        for name in self.nameDict: # For every file name in the name dictionary, if it is unique, add to name list.
            if self.nameDict[name] == 1:
                self.nameList.append(name)
        
        for key in self.sizeDict: # The name list contains the <name>.<extension> for each accessed-once-file.
            if key in self.nameList:
                self.uniqueBytes += self.sizeDict[key]

        print("len(nameList)={0}".format(len(self.nameList))) # Print the cardinality of the list of unique names.

        print("Unique Bytes={0}".format(self.uniqueBytes)) # Print unique bytes

        #print("len(nameSizeDict)={0}".format(len(self.nameSizeDict))) # Prints the size of the nameSizeDictionary

        #for i in self.sizeList: # Testing the creation of the sizeList and cardinality
        #    print(i)
        #print(len(self.sizeList))

        '''
        sizes = np.array(self.sizeList)
        sizes = sizes[sizes > 0]
        #sorted_sizes = np.sort(sizes)
        cdf = np.arange(1, len(sorted_sizes) + 1) / len(sorted_sizes)
        plt.figure(figsize=(8,6))
        plt.plot(sorted_sizes, cdf, marker='.', linestyle='none', color='blue')
        plt.xscale('log')
        plt.xlabel('Transfer Size (bytes, log₁₀ scale)')
        plt.ylabel('Cumulative Probability')
        plt.title('CDF of Transfer Sizes for All Distinct Objects')
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
        '''

        months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
        
        # Get counts in order, defaulting to 0 if a month is missing
        counts_ordered = [self.month_counts.get(m, 0) for m in months_order]
        total_requests = sum(counts_ordered)
        percentages = [(count / total_requests) * 100 for count in counts_ordered]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(months_order, percentages, color='skyblue', edgecolor='black')

        plt.title('Percentage of Total Requests per Month')
        plt.xlabel('Month')
        plt.ylabel('Percentage of Total Requests (%)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Add percentage labels on top of bars
        for bar, percentage in zip(bars, percentages):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{percentage:.1f}%', ha='center')

        plt.tight_layout()
        #plt.show()

        # TESTING TESTING 123
        #for key in self.objectTimeDict:
        #    print('Key={0}: List={1}'.format(key, self.objectTimeDict[key]))

    def getFileType(self, URI):
        if URI.endswith('/') or URI.endswith('.') or URI.endswith('..'):
            return 'HTML'
        filename = URI.split('/')[-1]
        if '?' in filename:
            return 'Dynamic'
        extension = filename.split('.')[-1].lower()
        if extension in self.fileTypeDict:
            return self.fileTypeDict[extension]
        return 'Others'

    def checkResCode(self, code):
        if code == '200' : return 'Successful'
        if code == '302' : return 'Found'
        if code == '304' : return 'Not Modified'   
        return None

if __name__ == '__main__': #Move logfile = open() function string parameter into local project file in auckland computer.
    logfile = open('/home/ac/Downloads/Assignment(1)/Assignment/UofC_access_log/access_log', 'r', errors='ignore')
    logParser = Parser()
    logParser.parse(logfile)
    pass
