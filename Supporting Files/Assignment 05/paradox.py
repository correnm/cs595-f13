\begin{verbatim}
#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString
from xml.dom import minidom
from xml.dom import pulldom



# Dr. Nelson's facebook network
file = open('C:/Python27/myFiles/Assignment 5/mln.graphml', 'r')
# convert to string
data = file.read()
# close the file
file.close()

#parse the xml downloaded from Facebook
dom = parseString(data)

# initialize the output objects
graphData={}
mlnFriendCount = 0

# Initialize the dot file
friends = open('C:/Python27/myFiles/Assignment 5/paradox.txt', 'w')
# Write the header
friends.write("ID" +"," + "FRIEND.COUNT")

#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name "node":
for node in dom.getElementsByTagName("node"):
    try:
        # keep track of MLNs friends
        mlnFriendCount = mlnFriendCount + 1
        nodeData = node.getElementsByTagName('data')
        for subNode in nodeData:
            friendCount = 0
            thisKey = subNode.getAttribute("key")
            if thisKey == "friend_count":
                subNode=subNode.toxml()
                #data key="friend_count"><![CDATA[421]]></data>
                #strip off the tag (<tag>data</tag>  --->   data):
                cData=subNode.replace('<data key="friend_count">','').replace('</data>','')
                #friendCount is extracted from <![CDATA[39]]>
                friendCount = cData.replace('<![CDATA[','').replace(']]>','')
            else:
                # My friend doesn't have any Facebook friends
                friendCount = 0
            graphData[mlnFriendCount] = friendCount
    except KeyboardInterrupt:
         print ""
         print "processing terminated."
         sys.exit(0)


#graph data is: friend#, friendCount
for key,value in graphData.iteritems():
    friends.write("\n")
    friends.write(str(key) + "," + str(value))
    # debug line
    print key, value
# Close the output file
friends.close()
\end{verbatim}
