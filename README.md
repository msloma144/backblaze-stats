# Backblaze SSDs vs HDDs Endurance

Backblaze stated in [this](https://www.backblaze.com/blog/are-ssds-really-more-reliable-than-hard-drives/) article that SSDs seem
to fail at quicker rate than HDDs when it comes to raw power on hours. SSD lives however are typically measured in terabytes written (TBW),
not in power on hours; Unlike HDDs where there are moving parts that wear down with use, SSDs memory cells ware down over time
with the number of writes that are performed. In this analysis, we put to the test if the SSDs in Backblaze's study likely failed
due to power on hours, or if they failed due to too many write cycles.

### Data Download
To download the data, run `data_downloader.py`. Note that this will consume approximately
16.2 GB of hard drive space. This file may take some time to run.

### Analysis
After collecting the data with `data_downloader.py`, you can then run `evaluation.ipynb` if you wish
to run the analysis yourself.

## Author
Michael Sloma

## Data Sources
* [Backblaze Data](https://www.backblaze.com/b2/hard-drive-test-data.html)

**Note:** sometimes IPython notebooks on GitHub don't work as expected, but you can always view them using [nbviewer](https://nbviewer.jupyter.org/).