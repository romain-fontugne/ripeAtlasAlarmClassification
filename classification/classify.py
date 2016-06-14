
import tools
from bson import objectid
import networkx as nx

def makeGraph(start, end):
    """Construct a graph from delay change and forwarding alarms.

    arguments:
    start -- first timestamp
    end -- last timestamp

    return: The constructed graph in form of a networkx graph
    """

    db = tools.connect_mongo()
    collection = db.rttChanges

    cursor = collection.find({
        "expId": objectid.ObjectId("56d9b1cbb0ab021cc2102c10"),
        # "timeBin": {"$in": timeBin},
        "$or": [{"timeBin": {"$gte": start}}, {"timeBin": {"$lte": end}}],
        "deviation": {"$gt": 3}
        })

    g = nx.Graph()
    for alarm in cursor:
        g.add_edge(alarm["ipPair"][0], alarm["ipPair"][1],{"dev":alarm["deviation"], "diff":alarm["diff"]})

    cursor = collection.find({
        "expId": objectid.ObjectId(""),
        "timeBin": timeBin,
        }) 
    #TODO add forwarding anomalies

    return g
