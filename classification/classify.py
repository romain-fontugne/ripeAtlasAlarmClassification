
from pytz import timezone
import tools
from bson import objectid
import networkx as nx
from datetime import datetime

def makeGraph(start=datetime(2015,6,10,tzinfo=timezone("UTC")),
        end=datetime(2015,6,11,tzinfo=timezone("UTC")), min_deviation=3,
        min_corr=-0.25):
    """Construct a graph from delay change and forwarding alarms.

    arguments:
    start -- first timestamp
    end -- last timestamp
    min_deviation -- minimum deviation for delay change alarms
    min_resp -- minimum responsibility (absolute value) for forwarding alarms 
    min_corr -- minimum correlation (absolute value) for forwarding alarms 

    return: The constructed graph in form of a networkx graph
    """

    db = tools.connect_mongo()
    collection = db.rttChanges

    cursor = collection.find({
        "expId": objectid.ObjectId("56d9b1cbb0ab021cc2102c10"),
        # "timeBin": {"$in": timeBin},
        "$and": [{"timeBin": {"$gte": start}}, {"timeBin": {"$lte": end}}],
        "deviation": {"$gt": 3}
        })

    g = nx.Graph()
    for alarm in cursor:
        g.add_edge(alarm["ipPair"][0], alarm["ipPair"][1],
                {   "dev":alarm["deviation"], 
                    "diff":alarm["diff"],
                    "time":alarm["timeBin"]
                })
        

    cursor = collection.find({
        "expId": objectid.ObjectId("56d9b1cbb0ab021d00224ca8"),
        "$and": [{"timeBin": {"$gte": start}}, {"timeBin": {"$lte": end}}],
        "corr": {"$lt": min_corr},
        }) 

    for alarm in cursor:
        #TODO
        pass

    

    return g
