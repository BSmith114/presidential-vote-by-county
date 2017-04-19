create or replace view vw_pres_vote
as
	with pres_vote_party
	as 
	(
		select 
			p.election
			,f.fips
			,case
				when p.party like '%Democrat%' 
					then 'Democratic'
				when p.party like '%Republican%'
					then 'Republican'
				else 'Other'
			end as party
			,sum(p.vote) as vote
		from 
			pres_vote p 
			inner join fips f 
				on p.fips = f.fips
		group by
			election
			,f.fips 
			,case
				when p.party like '%Democrat%' 
					then 'Democratic'
				when p.party like '%Republican%'
					then 'Republican'
				else 'Other'
			end
		order by
			fips
			,election
			,party
	)
	select 
		dem.election
		,dem.fips
		,f.county
		,f.state
		,coalesce(dem.vote, 0) as dem
		,coalesce(rep.vote, 0) as rep
		,coalesce(other.vote, 0) as other
		,(coalesce(dem.vote, 0) + coalesce(rep.vote, 0) + coalesce(other.vote, 0)) as total
	from 
		pres_vote_party dem
		left join pres_vote_party rep
			on dem.election = rep.election
			and dem.fips = rep.fips
		left join pres_vote_party other
			on dem.election = other.election
			and dem.fips = other.fips
			and other.party = 'Other'
		left join fips f
			on dem.fips = f.fips
	where 
		dem.party = 'Democratic'
		and rep.party = 'Republican'
	order by
		fips 
		,election