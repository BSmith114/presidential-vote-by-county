with x as
(
	-- makes alaska one county level entity
	select '02' fips, sum(a.dem) dem, sum(a.rep) rep, sum(a.oth) other, 2004 election
	from pres_vote_2004 a 
		inner join fips f
			on a.fips = f.fips
	where f.state = 'AK'

	union

	--combines bedford city and bedford county va into one entity
	select '51019' fips, sum(dem) dem, sum(rep) rep, sum(oth) other, 2004 election
	from pres_vote_2004 
	where fips IN ('51515','51019')  

	union

	--assigns shannon county fips to oglala county
	select '46102', dem, rep, oth other, 2004 election
	from pres_vote_2004 
	where fips IN ('46113')  

	union
	
	--selects the rest removing those from above
	select a.fips, dem, rep, oth, 2004 election
	from pres_vote_2004 a 
		inner join fips f
			on a.fips = f.fips
	where f.state <> 'AK' and a.fips not in ('51515', '51019' ,'15005', '46113') 
)
--insert into pres_vote
select * from x









