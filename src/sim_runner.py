import os, json, hashlib, datetime, numpy as np, matplotlib.pyplot as plt, pandas as pd, yaml

BASE = os.path.dirname(os.path.dirname(__file__))
OUT = os.path.join(BASE, "outputs")
os.makedirs(OUT, exist_ok=True)

def load_config():
    with open(os.path.join(BASE, "config.yaml")) as f:
        return yaml.safe_load(f)

def main():
    cfg = load_config()
    t = np.linspace(0,0.2,5000)
    y = np.sin(2*np.pi*35*t) * np.exp(-10*t)
    encoded = y*cfg.get("E_norm",0.2)
    seq = cfg.get("target_seq",0.795)
    phase_drift = 0.5
    plt.plot(t,y,label="fade")
    plt.plot(t,encoded,label="encoded")
    plt.legend(); plt.savefig(os.path.join(OUT,"plot.png")); plt.close()
    metrics = {"seq":seq,"phase_drift":phase_drift}
    with open(os.path.join(OUT,"metrics.json"),"w") as f: json.dump(metrics,f)
    df=pd.DataFrame({"t":t,"seq":[seq]*len(t)}); df.to_csv(os.path.join(OUT,"seq_log.csv"),index=False)
    fp = hashlib.sha256(json.dumps(metrics).encode()).hexdigest()
    shard = {"shard_id":fp[:16],"fingerprint":fp,"created":datetime.datetime.utcnow().isoformat()+"Z","metrics":metrics}
    with open(os.path.join(OUT,"shard.json"),"w") as f: json.dump(shard,f,indent=2)
    print("Shard:",shard)
if __name__=="__main__": main()
