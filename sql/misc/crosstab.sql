select * 
from crosstab
(
	'
	select 
		p.fips		
		,party
		,sum(p.vote) as vote
	from 
		pres_vote_party p 
	where 
		p.election = 2016
	group by 
		p.fips 
		,p.party
	order by 1
	'
)
as final_result
(
	fips text
	,dem numeric
	,other numeric
	,rep numeric
) inner join fips f on final_result.fips = f.fips; 