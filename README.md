# Install

For install `wald_analysis` perform commnds:

 1. `./setup.py sdist` or `python3 setup.py sdist`

 2.  `cd dist` and `sudo python3 -m pip install trafficstat.py-X.Y.Z.tar.gz` 

# Usage

Illustrate by example.

From catalog `wald_analysis` go to catalog with examples.

    ```cd ./examples/netflow```

## Make Statistic

 1. Make a stat-file with histograms of secondary features. 

    ```wald_make_statistic 01-ipfrag.csv -s script1.json -w 3```

 1. You can convert the stat-file into a png.

    ```wald_draw_statistic 01-ipfrag.stat```
    
## Analize

 1. Perform analize.

    ```wald_analyze 01-ipfrag.csv -n 00-normal.stat -p 01-ipfrag.stat 02-iphead.stat  -s script1.json -w 3```

 1. See result.
<pre>
$ head -3  01-ipfrag-analyzed.csv 
SrcPort,DstPort,Protocol,TCPFlags,ICMP,Octets,Packets,Pattern
0,0,56,0,0,38940,1947,[01-ipfrag:0.92;02-iphead:0.08]
0,0,1,0,770,288,6,[01-ipfrag:0.92;02-iphead:0.08]
</pre>
