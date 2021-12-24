/* 
Schema 定义

我们使用csv格式文件将数据导入hive中。

*/

/* movie */

create table movie
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        with serdeproperties ('quoteChar' = '\"', 'separatorChar' = ',') stored as
    inputformat 'org.apache.hadoop.mapred.TextInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    location 'hdfs://master:9000/user/hive/warehouse/movie.db/movie'
    tblproperties ('bucketing_version' = '2');

/* actor */

create table actor
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        with serdeproperties ('quoteChar' = '\"', 'separatorChar' = ',') stored as
    inputformat 'org.apache.hadoop.mapred.TextInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    location 'hdfs://master:9000/user/hive/warehouse/movie.db/actor'
    tblproperties ('bucketing_version' = '2');

/* day */

create table day
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        with serdeproperties ('quoteChar' = '\"', 'separatorChar' = ',') stored as
    inputformat 'org.apache.hadoop.mapred.TextInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    location 'hdfs://master:9000/user/hive/warehouse/movie.db/day'
    tblproperties ('bucketing_version' = '2');

/* director */

create table director
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        with serdeproperties ('quoteChar' = '\"', 'separatorChar' = ',') stored as
    inputformat 'org.apache.hadoop.mapred.TextInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    location 'hdfs://master:9000/user/hive/warehouse/movie.db/director'
    tblproperties ('bucketing_version' = '2');

/* emotion_score */
create table emotion_score
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        with serdeproperties ('quoteChar' = '\"', 'separatorChar' = ',') stored as
    inputformat 'org.apache.hadoop.mapred.TextInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    location 'hdfs://master:9000/user/hive/warehouse/movie.db/emotion_score'
    tblproperties ('bucketing_version' = '2');


/* label */

create table label
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        with serdeproperties ('quoteChar' = '\"', 'separatorChar' = ',') stored as
    inputformat 'org.apache.hadoop.mapred.TextInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    location 'hdfs://master:9000/user/hive/warehouse/movie.db/label'
    tblproperties ('bucketing_version' = '2');

/* review */

create table review
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        with serdeproperties ('quoteChar' = '\"', 'separatorChar' = ',') stored as
    inputformat 'org.apache.hadoop.mapred.TextInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    location 'hdfs://master:9000/user/hive/warehouse/movie.db/review'
    tblproperties ('bucketing_version' = '2');

/* score */

create table score
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        with serdeproperties ('quoteChar' = '\"', 'separatorChar' = ',') stored as
    inputformat 'org.apache.hadoop.mapred.TextInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    location 'hdfs://master:9000/user/hive/warehouse/movie.db/score'
    tblproperties ('bucketing_version' = '2');

/* user */

create table `user`
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        with serdeproperties ('quoteChar' = '\"', 'separatorChar' = ',') stored as
    inputformat 'org.apache.hadoop.mapred.TextInputFormat'
    outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    location 'hdfs://master:9000/user/hive/warehouse/movie.db/user'
    tblproperties ('bucketing_version' = '2');

