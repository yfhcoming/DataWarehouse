

// create index and constraint
:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///movie_schema.csv' AS row
merge (m:Movie {product_id: row.product_id})
SET m.score = toInteger(row.score)
SET m.score_count = toInteger(1)
SET m.emotion_score = toInteger(row.emotion_score)
SET m.emotion_count = toInteger(1)
SET m.title = row.title
SET m.day_id = toInteger(row.day_id);


// actor_schema
:auto using periodic commit 500
load csv with headers from 'file:///actor_schema.csv' as row
match (m:Movie) where m.product_id = row.p_id
merge (a:Actor {actor: row.actor})
set a.count = toInteger(row.count)
merge (a) -[:act_movie]->(m);
// merge (m) -[:movie_act]->(a);


// director_schema
:auto using periodic commit 500
load csv with headers from 'file:///director_schema.csv' as row
match (m:Movie) where m.product_id = row.p_id
merge (d:Director {director: row.director})
set d.count = toInteger(row.count)
merge (d) -[:director_movie]->(m);
// merge (m) -[:movie_director]->(d);


// label_schema
:auto using periodic commit 500
load csv with headers from 'file:///label_schema.csv' as row
match (m:Movie) where m.product_id = row.p_id
merge (l:Label {label: row.label})
set l.count = toInteger(row.count)
merge (l) -[:label_movie]->(m);
// merge (m) -[:movie_label]->(l);

// time_schema
:auto using periodic commit 500
load csv with headers from 'file:///day_schema.csv' as row
merge (t:Time {day_id: toInteger(row.day_id)})
set t.year = toInteger(row.year)
set t.season = toInteger(row.season)
set t.month = toInteger(row.month)
set t.day = toInteger(row.day)
set t.year_count = toInteger(row.year_count)
set t.season_count = toInteger(row.season_count)
set t.month_count = toInteger(row.month_count)
set t.day_count = toInteger(row.day_count);

// movie-time
:auto using periodic commit 500
load csv with headers from 'file:///movie_schema.csv' as row
with row.product_id as product_id,toInteger(row.day_id) as day_id
match (m:Movie {product_id:product_id,day_id:day_id})
match (t:Time {day_id:day_id})
// set m.day_id = toInteger(day_id)
// merge (m) -[:movie_time]->(t)
merge (t) -[:time_movie]->(m);

//下次从这里开始

// score_schma for movie
:auto using periodic commit 500
load csv with headers from 'file:///score_schema.csv' as row
with toInteger(row.score) as score,toInteger(row.count) as r_count
match( m:Movie {score:score} )
set m.score_count = r_count;

// emotion_score_schma for movie
:auto using periodic commit 500
load csv with headers from 'file:///emotion_score_schema.csv' as row
with toInteger(row.emotion_score) as emotion_score,toInteger(row.count) as r_count
match ( m:Movie{ emotion_score: emotion_score})
set m.emotion_count = r_count;




// pre-calculate 
match (a:Actor {actor: "Fred Williamson"})-[:act_movie]->(:Movie)<-[:act_movie]-(b:Actor)
return b.actor

match (a:Actor)-[:act_movie]->(:Movie)<-[:director_movie]-(b:Director)
return a.actor

match (a:Actor)-[:act_movie]->(:Movie)<-[:director_movie]-(b:Director)
return b.director

match (a:Director)-[:director_movie]->(:Movie)<-[:director_movie]-(b:Director)
return b.director

where a.actor <> b.actor and size((b)-->(a))=0;
with size(collect(b.actor)) as r_count
merge (a)-[r:actor_actor]->(b)
set r.count = r_count
return r.count

match (a:Actor {actor: "Robert Forster"})-[am:act_movie]->(:Movie)<-[:act_movie]-(b:Actor)
return a,am,b

set r.count = toInteger(1);

match (a:Actor)-[:act_movie]->(:Movie)<-[:act_movie]-(b:Actor)
where a.actor <> b.actor and size((b)-->(a))=0
with a,b
match (a)-[r]->(b)
set r.count = r.count+1;


match (a:Actor)-[:act_movie]->(:Movie)<-[:director_movie]-(b:Director)
merge (a)-[r:actor_director]->(b)
set r.count = case when r.count > 1 then r.count+1 else toInteger(1) end;

//Test-s
match (m:Movie)
with m
Limit 120
RETURN size(collect(m.title))
//Test-s-e

//Test

merge (a:Actor)-[r:actor_director]->(b:Director)
return r.count
order by r.count DESC
//Test-End1


match (a:Director)-[:director_movie]->(:Movie)<-[:director_movie]-(b:Director)
where a.director <> b.director and size((b)-->(a))=0
merge (a)-[r:director_director]->(b)
set r.count = toInteger(1);

match (a:Director)-[:director_movie]->(:Movie)<-[:director_movie]-(b:Director)
where a.director <> b.director and size((b)-->(a))=0
with a,b
match (a)-[r]->(b)
set r.count = r.count+1;

