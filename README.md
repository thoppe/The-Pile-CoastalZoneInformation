# The-Pile-PhilPapers

Download, parse, and filter the govinfo collection, [Coastal Zone Information Center Collection](https://www.govinfo.gov/app/collection/czic), data-ready for [The-Pile](https://github.com/EleutherAI/The-Pile).

> The Coastal Zone Information Center (CZIC) collection on this site provides access to nearly 5,000 coastal related documents that GPO received from the National Oceanic and Atmospheric Administration (NOAA) Central Library.

> The collection provides almost 30 years of data and information crucial to the understanding of U.S. coastal management and NOAA's mission to sustain healthy coasts. These documents were originally submitted to the NOAA Office of Ocean and Coastal Resource Management (OCRM) by state coastal zone management programs in accordance with the Coastal Zone Management Act (CZMA) of 1972. These historic documents were provided to GPO by the content originator, and digitized for public use.

Each publication was downloaded from govinfo. Text was extracted from the PDF was already high quality, however some paragraphs contained unusable text for LM due to figure legends and charts. A bigram distribution was made over the corpus and each paragraph with a KL divergence > 2.0 was discarded. This reduced to the total text by about 10% and improved the data quality significantly.

     ✔ Saved to data/GOVINFO_CZIC_KL.jsonl
     ℹ Saved 4,774 articles
     ℹ Uncompressed filesize 841,199,958
     ℹ Compressed filesize   263,059,778

Data source temporary hosted at https://drive.google.com/file/d/1qjZZTqS-m63TMKBYB1eNRc5Bh4W--SYQ/view?usp=sharing

     > sha256sum GOVINFO_CZIC_KL.jsonl.zst 
     c7a46f5af12789fc8b2105b208e22fa400c63ac720c72073e90ee91af6744f00  GOVINFO_CZIC_KL.jsonl.zst