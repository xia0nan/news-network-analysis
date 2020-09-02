# news-network-analysis
Intelligent News Network Analysis

## 01.09.2020
Build **Entity** and **Link** table from existing database

Entity table
 * Use refinitiv_id or guid?
   * it's the same
 * Extract permid for every news
 * No news with multiple permid?
   * Should use table *article_raw* instead of *article*
 * News with multiple entities will have *entity_count* > 1 in *article* table
    
Example: Entity table

news_id | permid
--- | ---
refinitiv_id | 1
refinitiv_id | 2
refinitiv_id | 3

Example: Link table

news_id | source | target
--- | --- | ---
refinitiv_id | 1 | 2
refinitiv_id | 1 | 3
refinitiv_id | 2 | 3
refinitiv_id | 2 | 1
refinitiv_id | 3 | 1
refinitiv_id | 3 | 2

## 02.09.2020
Extract news with multiple permids
