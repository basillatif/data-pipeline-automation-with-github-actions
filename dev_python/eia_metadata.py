import datetime
import pandas as pd

def create_metadata(data, start, end, type):
  
    meta = {
        "index": None,
        "parent": data["parent"].dropna().unique()[0],
        "subba": data["subba"].dropna().unique()[0],
        "time": datetime.datetime.now(datetime.timezone.utc),
        "start": start,
        "end": end,
        "start_act": data["period"].min(),
        "end_act": data["period"].max(),
        "start_match": start == data["period"].min(),
        "end_match": end == data["period"].max(),
        "n_obs": len(data),
        "na": data["value"].isna().sum(),
        "type": type,
        "update": False,
        "success": False,
        "comments": ""
  }

    if meta["start_match"] and meta["end_match"] and type == "refresh" and meta["na"] != 0:
        meta["success"] = True
    else:
        meta["success"] = False
    
    if not meta["start_match"]:
      meta["comments"] = meta["comments"] + "The start argument does not match the actual; "
    elif not meta["end_match"]:
      meta["comments"] = meta["comments"] + "The end argument does not match the actual; "
    elif meta["na"] != 0:
      meta["comments"] = meta["comments"] + "Missing values were found; "

    return meta



def append_metadata(meta_path, meta, save = False, init = False):
  
    if not init:
        meta_archive = pd.read_csv(meta_path)
        meta_archive["time"] = pd.to_datetime(meta_archive["time"])
        meta_archive["end"] = pd.to_datetime(meta_archive["end"])
        meta_archive["start"] = pd.to_datetime(meta_archive["start"])
        meta_archive["end_act"] = pd.to_datetime(meta_archive["end_act"])
        meta_archive["start_act"] = pd.to_datetime(meta_archive["start_act"])
        meta["index"] = meta_archive["index"].max() + 1
        meta_new = meta_archive._append(meta)
    else:
       meta_new = meta
       meta_new["index"] = 1
    
    if save:
       meta_new.to_csv(meta_path)

    return meta_new

def load_metadata(path, series):
    
    class metadata:
       def __init__(output, metadata, last_index, request_meta):
          output.metadata = metadata
          output.last_index = last_index
          output.request_meta = request_meta
    
   
    meta = pd.read_csv(path)
    meta["time"] = pd.to_datetime(meta["time"])
    meta["start"] = pd.to_datetime(meta["start"])
    meta["start_act"] = pd.to_datetime(meta["start_act"])
    meta["end"] = pd.to_datetime(meta["end"])
    meta["end_act"] = pd.to_datetime(meta["end_act"])

    log_temp = {
       "parent": None,
       "subba": None,
       "end_act": None,
       "request_start": None
    }

    meta_success = meta[meta["success"] == True]
    for i in series.index:
        p = series.at[i, "parent_id"]
        s = series.at[i, "subba_id"]
        l = meta_success[(meta_success["parent"] == p) & (meta_success["subba"] == s) ]
        l = l[l["index"] == l["index"].max()]
        log = log_temp
        log["parent"] = p
        log["subba"] = s
        log["end_act"] = l["end_act"].max()
        log["request_start"] = l["end_act"].max() + datetime.timedelta(hours = 1)
        if i == series.index.start:
           request_meta = pd.DataFrame([log])
        else:
           request_meta = request_meta._append(pd.DataFrame([log]))


       
       
    output = metadata(metadata = meta,
                      last_index = meta["index"].max(),
                      request_meta = request_meta)
    
    return output


